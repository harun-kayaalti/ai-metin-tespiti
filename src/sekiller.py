# -*- coding: utf-8 -*-
"""
Sonuc sekilleri - AI metin tespiti projesi
23. gun

GIRDI   data_raw/texts.csv, data_raw/detector_scores.csv
        results/perplexity_scores.csv (varsa)
CIKTI   figures/sekil1..5 (.png, 300 dpi)

GEREKSINIM
  pip install matplotlib

Sekiller gri tonlamada da okunabilecek bicimde, tek sutuna sigacak
oranlarda uretilir. Her sekil basligi ve eksen etiketleri Turkcedir.
"""

import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

Z = 1.959963985
CIK = "figures"
RENK = {"GPTZero": "#1F3864", "ZeroGPT": "#8C7B4A", "Perplexity": "#5B7C5B"}


def wilson(k, n, z=Z):
    if n == 0:
        return float("nan"), 0, 0
    p = k / n
    payda = 1 + z * z / n
    m = (p + z * z / (2 * n)) / payda
    y = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / payda
    return p, max(0.0, m - y), min(1.0, m + y)


def kaydet(fig, ad):
    os.makedirs(CIK, exist_ok=True)
    yol = os.path.join(CIK, ad)
    fig.savefig(yol, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print("->", yol)


# ----------------------------------------------------------------------
texts = pd.read_csv("data_raw/texts.csv")
sc = pd.read_csv("data_raw/detector_scores.csv")
meta = pd.read_csv("data_raw/ai_metadata.csv")
# KARDEP Bolum 12: model/arac bilgisi ayri metadata tablosundadir.
_m = dict(zip(meta.text_id, meta.model_tool))
_src = dict(zip(meta.text_id, meta.source_text_id))
texts["model"] = texts.apply(
    lambda r: _m.get(r["text_id"], "") if r["label"] == "ai"
    else _m.get(_src.get(r["text_id"]), ""), axis=1)
texts["humanizer"] = texts.apply(
    lambda r: _m.get(r["text_id"], "") if r["label"] == "humanized" else "", axis=1)
ort = texts[["text_id", "label", "model", "prompt_id", "humanizer"]]
d = sc.merge(ort, on="text_id")

MODELLER = ["ChatGPT", "Gemini", "Claude", "Kumru"]
ARACLAR = ["Aithor", "Rephraser"]
DEDEKTORLER = sorted(d.detector_name.unique())


# ---------------- Sekil 1: ham metinlerde yakalama ----------------
ai = d[d.label == "ai"]
fig, ax = plt.subplots(figsize=(7, 4))
gen, x0 = 0.38, range(len(MODELLER))
for i, det in enumerate(DEDEKTORLER):
    p, lo, hi = [], [], []
    for m in MODELLER:
        a = ai[(ai.detector_name == det) & (ai.model == m)]
        pp, l, h = wilson(int(a.binary_label.sum()), len(a))
        p.append(pp); lo.append(pp - l); hi.append(h - pp)
    ax.bar([x + (i - 0.5) * gen for x in x0], p, gen,
           yerr=[lo, hi], capsize=3, label=det,
           color=RENK.get(det, "#777777"), edgecolor="black", linewidth=0.5)
ax.set_xticks(list(x0)); ax.set_xticklabels(MODELLER)
ax.set_ylim(0, 1.05); ax.set_ylabel("Yakalama oranı")
ax.set_title("Ham yapay zekâ metinlerinde yakalama oranı\n(%95 Wilson güven aralığı, n=5)")
ax.axhline(0.5, ls="--", lw=0.8, color="gray")
ax.legend(frameon=False)
kaydet(fig, "sekil1_ham_yakalama.png")


# ---------------- Sekil 2: evasion etkisi (KARDEP Bolum 13) ----------------
# Evasion etkisi = Recall(ham) - Recall(insanlastirilmis)
fig, ax = plt.subplots(figsize=(7, 4))
x0 = range(len(ARACLAR))
for i, det in enumerate(DEDEKTORLER):
    alt = d[d.detector_name == det]
    r_ham = alt[alt.label == "ai"].binary_label.mean()
    etki = []
    for arac in ARACLAR:
        h = alt[(alt.label == "humanized") & (alt.humanizer == arac)]
        etki.append(r_ham - h.binary_label.mean())
    ax.bar([x + (i - 0.5) * gen for x in x0], etki, gen,
           label=det, color=RENK.get(det, "#777777"),
           edgecolor="black", linewidth=0.5)
ax.axhline(0, lw=0.8, color="black")
ax.set_xticks(list(x0)); ax.set_xticklabels(ARACLAR)
ax.set_ylabel("Evasion etkisi (recall düşüşü)")
ax.set_title("İnsanlaştırmanın yakalama oranı üzerindeki etkisi\n"
             "Recall(ham) − Recall(insanlaştırılmış)")
ax.legend(frameon=False)
kaydet(fig, "sekil2_evasion_etkisi.png")


# ---------------- Sekil 3: iki dedektor ayni metinde ne diyor ----------------
p = d.pivot_table(index="text_id", columns="detector_name", values="score").join(
    texts.set_index("text_id")[["label"]])
if len(DEDEKTORLER) >= 2:
    a, b = DEDEKTORLER[0], DEDEKTORLER[1]
    fig, ax = plt.subplots(figsize=(5.2, 5))
    for lab, mrk, col in [("ai", "o", "#1F3864"), ("humanized", "^", "#B06B2C")]:
        alt = p[p.label == lab]
        ax.scatter(alt[a], alt[b], marker=mrk, s=45, alpha=0.75,
                   edgecolor="black", linewidth=0.4, color=col,
                   label="ham yapay" if lab == "ai" else "insanlaştırılmış")
    ax.axhline(0.5, ls="--", lw=0.8, color="gray")
    ax.axvline(0.5, ls="--", lw=0.8, color="gray")
    ax.set_xlim(-0.05, 1.05); ax.set_ylim(-0.05, 1.05)
    ax.set_xlabel(f"{a} skoru"); ax.set_ylabel(f"{b} skoru")
    ax.set_title("Aynı metne iki dedektörün verdiği skor\n(çeyrekler zıt kararları gösterir)")
    ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.13), ncol=2)
    kaydet(fig, "sekil3_dedektor_uyumu.png")


# ---------------- Sekil 4: perplexity dagilimi ----------------
yol = "results/perplexity_scores.csv"
if os.path.exists(yol):
    try:
        pp = pd.read_csv(yol)
    except Exception:
        pp = pd.DataFrame()
    if "perplexity" in pp.columns and "dil_modeli" in pp.columns:
        pp = pp.merge(ort, on="text_id", suffixes=("", "_x"))
        lmler = sorted(pp.dil_modeli.unique())
        fig, ax = plt.subplots(figsize=(7.5, 4))
        konum, etiket = [], []
        for i, lm in enumerate(lmler):
            for j, lab in enumerate(["ai", "humanized"]):
                v = pp[(pp.dil_modeli == lm) & (pp.label == lab)].perplexity.tolist()
                x = i * 2.6 + j
                ax.boxplot(v, positions=[x], widths=0.7, showfliers=False,
                           medianprops=dict(color="black"))
                ax.scatter([x + (k % 5 - 2) * 0.035 for k in range(len(v))], v,
                           s=14, alpha=0.55, color="#1F3864" if lab == "ai" else "#B06B2C",
                           edgecolor="none")
                konum.append(x)
                etiket.append("ham" if lab == "ai" else "insanl.")
            ax.text(i * 2.6 + 0.5, -0.06, lm.split("/")[-1],
                    ha="center", va="top", transform=ax.get_xaxis_transform(), fontsize=8)
        ax.set_xticks(konum); ax.set_xticklabels(etiket, fontsize=8)
        ax.set_ylabel("Perplexity")
        ax.set_title("Ham ve insanlaştırılmış metinlerde perplexity dağılımı")
        kaydet(fig, "sekil4_perplexity_dagilim.png")

print("\nTum sekiller figures/ klasorune yazildi.")
