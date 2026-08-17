# -*- coding: utf-8 -*-
"""
Dedektorler arasi uyum ve karar farklari
23. gun - AI metin tespiti projesi

GIRDI
  data_raw/texts.csv
  data_raw/detector_scores.csv
  results/perplexity_scores.csv   (varsa)

CIKTI
  results/uyum.md
  results/uyum_ozet.csv

HESAPLANANLAR
  1. Ham uyum orani ve Cohen kappa            [karar veren dedektorler]
  2. McNemar testi (tam binom)                [karar veren dedektorler]
  3. Yon uyumu: insanlastirma skoru dusurdu mu [tum dedektor tipleri]

NOT
  Cohen kappa ve McNemar yalnizca ikili karar ureten dedektorler icin
  hesaplanabilir. Perplexity yaklasiminda esik kalibre edilmedigi icin
  ikili karar yoktur; bu yaklasim ucuncu bolumdeki yon uyumu analizine
  dahil edilmistir.

  Dis kutuphane gerektirmez.
"""

import math
import os
from itertools import combinations

import pandas as pd


# ----------------------------------------------------------------------
def cohen_kappa(a, b):
    """Iki degerlendirici arasinda Cohen kappa (ikili etiketler)."""
    n = len(a)
    if n == 0:
        return float("nan"), float("nan")
    gozlenen = sum(1 for x, y in zip(a, b) if x == y) / n
    pa1, pb1 = sum(a) / n, sum(b) / n
    beklenen = pa1 * pb1 + (1 - pa1) * (1 - pb1)
    if beklenen == 1:
        return gozlenen, float("nan")
    return gozlenen, (gozlenen - beklenen) / (1 - beklenen)


def kappa_yorum(k):
    if k != k:
        return "hesaplanamaz"
    if k < 0:     return "tesadufun altinda"
    if k < 0.20:  return "onemsiz"
    if k < 0.40:  return "zayif"
    if k < 0.60:  return "orta"
    if k < 0.80:  return "iyi"
    return "cok iyi"


def binom_kuyruk(k, n, p=0.5):
    """Iki yonlu tam binom testi (McNemar icin)."""
    if n == 0:
        return float("nan")
    def pmf(i):
        return math.comb(n, i) * p ** i * (1 - p) ** (n - i)
    gozlenen = pmf(k)
    return min(1.0, sum(pmf(i) for i in range(n + 1) if pmf(i) <= gozlenen + 1e-12))


def mcnemar(a, b):
    """
    a, b: ayni metinler icin iki dedektorun ikili kararlari.
    Uyusmayan cift sayilariyla tam binom testi uygulanir.
    Doner: (b01, b10, p)
      b01 = a dogru/pozitif, b negatif ; b10 = tersi
    """
    b01 = sum(1 for x, y in zip(a, b) if x == 1 and y == 0)
    b10 = sum(1 for x, y in zip(a, b) if x == 0 and y == 1)
    return b01, b10, binom_kuyruk(min(b01, b10), b01 + b10)


# ----------------------------------------------------------------------
def veri_yukle():
    texts = pd.read_csv("data_raw/texts.csv")
    sc = pd.read_csv("data_raw/detector_scores.csv")
    ort = texts[["text_id", "label", "model", "prompt_id", "humanizer"]]

    tic = sc[["text_id", "detector_name", "score", "binary_label"]].merge(ort, on="text_id")
    tic = tic.rename(columns={"detector_name": "dedektor"})
    tic["yapaylik"] = tic["score"]
    tic["karar_var"] = True
    parcalar = [tic[["text_id", "dedektor", "yapaylik", "binary_label", "karar_var",
                     "label", "model", "prompt_id", "humanizer"]]]

    yol = "results/perplexity_scores.csv"
    if os.path.exists(yol):
        pp = pd.read_csv(yol)
        if "perplexity" in pp.columns:
            pp = pp[["text_id", "dil_modeli", "perplexity"]].merge(ort, on="text_id")
            pp["dedektor"] = "Perplexity: " + pp["dil_modeli"].str.split("/").str[-1]
            pp["yapaylik"] = -pp["perplexity"]     # dusuk ppl = daha makine benzeri
            pp["binary_label"] = None
            pp["karar_var"] = False
            parcalar.append(pp[["text_id", "dedektor", "yapaylik", "binary_label",
                                "karar_var", "label", "model", "prompt_id", "humanizer"]])

    return texts, pd.concat(parcalar, ignore_index=True)


# ----------------------------------------------------------------------
def main():
    texts, d = veri_yukle()
    os.makedirs("results", exist_ok=True)
    sat, ozet = [], []

    kararli = sorted(d[d.karar_var].dedektor.unique())
    tumu = list(dict.fromkeys(d.dedektor.tolist()))

    sat += ["# Dedektorler Arasi Uyum", "",
            f"Uretim tarihi: {pd.Timestamp.today().date()}", "",
            f"Metin: {len(texts)} | Karar ureten dedektor: {len(kararli)} | "
            f"Toplam dedektor: {len(tumu)}", ""]

    # ---------------- 1. Kappa ----------------
    sat += ["## 1. Karar uyumu ve Cohen kappa", "",
            "Ayni metne iki dedektorun ayni etiketi verip vermedigi.",
            "Kappa, tesadufen beklenen uyusma cikarildiktan sonra kalan uyumu olcer.", "",
            "| dedektor cifti | metin kumesi | n | ham uyum | kappa | yorum |",
            "|---|---|---|---|---|---|"]
    kumeler = [("tum metinler", None), ("ham yapay", "ai"), ("insanlastirilmis", "humanized")]
    for d1, d2 in combinations(kararli, 2):
        for ad, lab in kumeler:
            a1 = d[(d.dedektor == d1)]
            a2 = d[(d.dedektor == d2)]
            if lab:
                a1, a2 = a1[a1.label == lab], a2[a2.label == lab]
            ort = a1.set_index("text_id").binary_label.astype(int).to_dict()
            ikinci = a2.set_index("text_id").binary_label.astype(int).to_dict()
            ortak = sorted(set(ort) & set(ikinci))
            x = [ort[t] for t in ortak]
            y = [ikinci[t] for t in ortak]
            u, k = cohen_kappa(x, y)
            sat.append(f"| {d1} - {d2} | {ad} | {len(ortak)} | {u:.3f} | {k:.3f} | {kappa_yorum(k)} |")
            ozet.append(dict(bolum="kappa", karsilastirma=f"{d1}-{d2}", kume=ad,
                             n=len(ortak), ham_uyum=round(u, 4), kappa=round(k, 4)))
    sat.append("")

    # ---------------- 2. McNemar ----------------
    sat += ["## 2. Karar farkinin anlamliligi (McNemar, tam binom)", "",
            "Ham yapay metinlerde iki dedektorun yakalama farki test edilmistir.",
            "Yalnizca uyusmayan ciftler bilgi tasir.", "",
            "| dedektor cifti | n | yalniz birinci yakaladi | yalniz ikinci yakaladi | p |",
            "|---|---|---|---|---|"]
    for d1, d2 in combinations(kararli, 2):
        a1 = d[(d.dedektor == d1) & (d.label == "ai")].set_index("text_id").binary_label.astype(int)
        a2 = d[(d.dedektor == d2) & (d.label == "ai")].set_index("text_id").binary_label.astype(int)
        ortak = sorted(set(a1.index) & set(a2.index))
        x = [int(a1.loc[t]) for t in ortak]
        y = [int(a2.loc[t]) for t in ortak]
        b01, b10, p = mcnemar(x, y)
        sat.append(f"| {d1} - {d2} | {len(ortak)} | {b01} | {b10} | {p:.4f} |")
        ozet.append(dict(bolum="mcnemar", karsilastirma=f"{d1}-{d2}", kume="ham yapay",
                         n=len(ortak), ham_uyum=None, kappa=None, b01=b01, b10=b10, p=round(p, 5)))
    sat.append("")

    # ---------------- 3. Yon uyumu ----------------
    sat += ["## 3. Yon uyumu: insanlastirma yapaylik skorunu dusurdu mu", "",
            "Her eslestirilmis cift icin skorun yonu (dustu / degismedi / yukseldi)",
            "kaydedilmis, dedektorler bu yon uzerinden karsilastirilmistir. Esik",
            "gerektirmedigi icin perplexity yaklasimi da bu analize dahildir.", "",
            "| dedektor | dustu | degismedi | yukseldi | n |",
            "|---|---|---|---|---|"]
    yonler = {}
    for det in tumu:
        alt = d[d.dedektor == det]
        ham = alt[alt.label == "ai"].set_index(["model", "prompt_id"]).yapaylik
        y = {}
        for _, r in alt[alt.label == "humanized"].iterrows():
            anahtar = (r["model"], r["prompt_id"])
            if anahtar not in ham.index:
                continue
            fark = r["yapaylik"] - float(ham.loc[anahtar])
            y[r["text_id"]] = -1 if fark < 0 else (1 if fark > 0 else 0)
        yonler[det] = y
        sat.append(f"| {det} | {sum(1 for v in y.values() if v == -1)} | "
                   f"{sum(1 for v in y.values() if v == 0)} | "
                   f"{sum(1 for v in y.values() if v == 1)} | {len(y)} |")
        ozet.append(dict(bolum="yon", karsilastirma=det, kume="insanlastirilmis",
                         n=len(y),
                         dustu=sum(1 for v in y.values() if v == -1),
                         yukseldi=sum(1 for v in y.values() if v == 1)))
    sat.append("")

    sat += ["Dedektor ciftleri arasinda yon uyumu:", "",
            "| dedektor cifti | ayni yon | n | oran |", "|---|---|---|---|"]
    for d1, d2 in combinations(tumu, 2):
        ortak = sorted(set(yonler[d1]) & set(yonler[d2]))
        if not ortak:
            continue
        ayni = sum(1 for t in ortak if yonler[d1][t] == yonler[d2][t])
        sat.append(f"| {d1} - {d2} | {ayni} | {len(ortak)} | {ayni / len(ortak):.3f} |")
        ozet.append(dict(bolum="yon_uyumu", karsilastirma=f"{d1}-{d2}",
                         kume="insanlastirilmis", n=len(ortak),
                         ham_uyum=round(ayni / len(ortak), 4)))
    sat += ["", "> Not: n=60 ve alt kumelerde n=20 ile calisildigindan kappa ve",
            "> McNemar sonuclari genis belirsizlik tasir. Sonuclar egilim olarak",
            "> yorumlanmali, kesin nokta tahmini olarak sunulmamalidir.", ""]

    with open("results/uyum.md", "w", encoding="utf-8") as f:
        f.write("\n".join(sat))
    pd.DataFrame(ozet).to_csv("results/uyum_ozet.csv", index=False, encoding="utf-8-sig")

    print("\n".join(sat))
    print()
    print("-> results/uyum.md")
    print("-> results/uyum_ozet.csv")


if __name__ == "__main__":
    main()
