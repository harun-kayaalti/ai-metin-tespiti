# -*- coding: utf-8 -*-
"""
Metrik hesaplari - AI metin tespiti projesi
22. gun: ayirt etme gucu, esik gecisi, istatistiksel anlamlilik

GIRDI
  data_raw/texts.csv
  data_raw/detector_scores.csv
  results/perplexity_scores.csv        (varsa)

CIKTI
  results/metrikler.md
  results/metrikler_ozet.csv

HESAPLANANLAR
  1. Yakalama orani (recall) + Wilson %95 guven araligi   [ticari dedektorler]
  2. AUC: ham yapay metni insanlastirilmistan ayirt etme  [tum dedektor tipleri]
  3. Esik gecisi (kacirma) orani + Wilson %95 GA          [ticari dedektorler]
  4. Wilcoxon isaretli sira testi (eslestirilmis)         [tum dedektor tipleri]

NOTLAR
  - Dis kutuphane gerektirmez (scipy/sklearn yok). AUC Mann-Whitney U
    siralamasiyla, Wilcoxon normal yaklasimla hesaplanir.
  - Perplexity icin "yapaylik skoru" = -perplexity alinir; cunku dusuk
    perplexity daha ongorulebilir (daha makine benzeri) metni gosterir.
  - Perplexity icin yakalama orani hesaplanmaz: karar esigi insan yazimi
    metinler olmadan kalibre edilemez.
"""

import math
import os

import pandas as pd

Z = 1.959963985            # %95 icin normal z degeri
ESIK = 0.50


# ----------------------------------------------------------------------
# ISTATISTIK YARDIMCILARI
# ----------------------------------------------------------------------
def normal_cdf(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def wilson(k, n, z=Z):
    """Binom oran icin Wilson skor guven araligi."""
    if n == 0:
        return (float("nan"),) * 3
    p = k / n
    payda = 1 + z * z / n
    merkez = (p + z * z / (2 * n)) / payda
    yari = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / payda
    return p, max(0.0, merkez - yari), min(1.0, merkez + yari)


def siralar(x):
    """Baglari ortalamayla cozen sira (rank) vektoru."""
    n = len(x)
    idx = sorted(range(n), key=lambda i: x[i])
    r = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and x[idx[j + 1]] == x[idx[i]]:
            j += 1
        ort = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            r[idx[k]] = ort
        i = j + 1
    return r


def auc(pozitif, negatif):
    """
    Mann-Whitney U uzerinden AUC.
    AUC = P(pozitif skoru > negatif skoru) + 0.5 * P(esit)
    0.5 = ayirt edemiyor, 1.0 = kusursuz ayiriyor.
    """
    n1, n2 = len(pozitif), len(negatif)
    if n1 == 0 or n2 == 0:
        return float("nan")
    r = siralar(list(pozitif) + list(negatif))
    return (sum(r[:n1]) - n1 * (n1 + 1) / 2.0) / (n1 * n2)


def wilcoxon(farklar):
    """
    Wilcoxon isaretli sira testi (normal yaklasim, bag duzeltmeli).
    Sifir farklar cikarilir. Kucuk n'de yaklasim kabadir; n<10 ise
    sonuc yorumlanirken dikkatli olunmalidir.
    Doner: (n_kullanilan, W, z, iki_yonlu_p)
    """
    d = [f for f in farklar if f != 0]
    n = len(d)
    if n < 5:
        return n, float("nan"), float("nan"), float("nan")
    r = siralar([abs(x) for x in d])
    w_arti = sum(r[i] for i in range(n) if d[i] > 0)
    w_eksi = sum(r[i] for i in range(n) if d[i] < 0)
    W = min(w_arti, w_eksi)
    ort = n * (n + 1) / 4.0
    # bag duzeltmesi
    from collections import Counter
    baglar = Counter(r)
    duzeltme = sum(t ** 3 - t for t in baglar.values()) / 48.0
    var = n * (n + 1) * (2 * n + 1) / 24.0 - duzeltme
    if var <= 0:
        return n, W, float("nan"), float("nan")
    z = (W - ort + 0.5) / math.sqrt(var)      # surekliluk duzeltmesi
    p = 2 * normal_cdf(-abs(z))
    return n, W, z, min(1.0, p)


def yildiz(p):
    if p != p:
        return "-"
    return "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else "a.d."


# ----------------------------------------------------------------------
# VERIYI TEK TABLOYA TOPLA
# ----------------------------------------------------------------------
def veri_yukle():
    texts = pd.read_csv("data_raw/texts.csv")
    sc = pd.read_csv("data_raw/detector_scores.csv")

    ort = texts[["text_id", "label", "model", "prompt_id", "humanizer", "source_text_id"]]
    tic = sc[["text_id", "detector_name", "score", "binary_label"]].merge(ort, on="text_id")
    tic = tic.rename(columns={"detector_name": "dedektor"})
    tic["yapaylik"] = tic["score"]
    tic["tip"] = "ticari"

    parcalar = [tic]

    yol = "results/perplexity_scores.csv"
    if os.path.exists(yol):
        pp = pd.read_csv(yol)
        if "perplexity" in pp.columns:
            pp = pp[["text_id", "dil_modeli", "perplexity"]].merge(ort, on="text_id")
            pp["dedektor"] = "Perplexity: " + pp["dil_modeli"].str.split("/").str[-1]
            # Dusuk perplexity = daha makine benzeri -> yapaylik skoru isaret ters
            pp["yapaylik"] = -pp["perplexity"]
            pp["score"] = pp["perplexity"]
            pp["binary_label"] = None
            pp["tip"] = "baseline"
            parcalar.append(pp[["text_id", "dedektor", "score", "binary_label",
                                "label", "model", "prompt_id", "humanizer",
                                "source_text_id", "yapaylik", "tip"]])

    return texts, pd.concat(parcalar, ignore_index=True)


# ----------------------------------------------------------------------
def main():
    texts, d = veri_yukle()
    os.makedirs("results", exist_ok=True)
    sat, ozet = [], []

    dedektorler = list(dict.fromkeys(d.dedektor.tolist()))
    araclar = sorted(x for x in texts.humanizer.dropna().unique() if x)

    sat += ["# Metrik Sonuclari", "",
            f"Uretim tarihi: {pd.Timestamp.today().date()}", "",
            f"Metin: {len(texts)} | Dedektor: {len(dedektorler)} | "
            f"Toplam olcum: {len(d)}", "",
            "Guven araliklari Wilson skor yontemiyle, %95 duzeyinde hesaplanmistir.", ""]

    # ---------------- 1. Yakalama orani ----------------
    sat += ["## 1. Ham yapay metinlerde yakalama orani", "",
            "Yalnizca ticari dedektorler icin hesaplanabilir; perplexity",
            "yaklasiminda karar esigi kalibre edilmemistir.", "",
            "| dedektor | uretici model | yakalanan | n | oran | %95 GA |",
            "|---|---|---|---|---|---|"]
    for det in dedektorler:
        alt = d[(d.dedektor == det) & (d.label == "ai")]
        if alt.binary_label.isna().all():
            continue
        for mdl in ["TUMU"] + sorted(alt.model.unique()):
            a = alt if mdl == "TUMU" else alt[alt.model == mdl]
            k, n = int(a.binary_label.sum()), len(a)
            p, lo, hi = wilson(k, n)
            sat.append(f"| {det} | {mdl} | {k} | {n} | {p:.3f} | [{lo:.3f}, {hi:.3f}] |")
            ozet.append(dict(bolum="yakalama", dedektor=det, grup=mdl,
                             deger=round(p, 4), alt=round(lo, 4), ust=round(hi, 4), n=n))
    sat.append("")

    # ---------------- 2. AUC ----------------
    sat += ["## 2. Ayirt etme gucu (AUC)", "",
            "Ham yapay metinler ile insanlastirilmis metinlerin ayrilabilirligi.",
            "0,50 = hic ayirt edemiyor, 1,00 = kusursuz ayiriyor. Esik",
            "gerektirmedigi icin ucuncu dedektor tipi de ayni olcute girer.", "",
            "| dedektor | karsilastirma | n(ham) | n(insanlastirilmis) | AUC |",
            "|---|---|---|---|---|"]
    for det in dedektorler:
        alt = d[d.dedektor == det]
        ham = alt[alt.label == "ai"].yapaylik.tolist()
        for arac in ["TUMU"] + araclar:
            h = alt[alt.label == "humanized"]
            if arac != "TUMU":
                h = h[h.humanizer == arac]
            deger = auc(ham, h.yapaylik.tolist())
            sat.append(f"| {det} | {arac} | {len(ham)} | {len(h)} | {deger:.3f} |")
            ozet.append(dict(bolum="auc", dedektor=det, grup=arac,
                             deger=round(deger, 4), alt=None, ust=None, n=len(h)))
    sat += ["", "> Not: Insanlastirilmis metinler ham metinlerden turetildiginden",
            "> iki grup bagimsiz degildir. AUC burada mutlak bir siniflandirma",
            "> performansi degil, esikten bagimsiz bir ayrilabilirlik olcusu",
            "> olarak yorumlanmalidir.", ""]

    # ---------------- 3. Esik gecisi ----------------
    sat += ["## 3. Esik gecisi (kacirma)", "",
            "Ham hali yapay olarak isaretlenmis metinlerin, insanlastirma",
            "sonrasi kacinin insan tarafina gectigi.", "",
            "| dedektor | arac | kacan | n | oran | %95 GA |",
            "|---|---|---|---|---|---|"]
    for det in dedektorler:
        alt = d[d.dedektor == det]
        if alt.binary_label.isna().all():
            continue
        ham = alt[alt.label == "ai"].set_index(["model", "prompt_id"]).binary_label
        for arac in araclar:
            h = alt[(alt.label == "humanized") & (alt.humanizer == arac)]
            k = n = 0
            for _, r in h.iterrows():
                anahtar = (r["model"], r["prompt_id"])
                if anahtar in ham.index and float(ham.loc[anahtar]) == 1:
                    n += 1
                    k += int(float(r["binary_label"]) == 0)
            if n:
                p, lo, hi = wilson(k, n)
                sat.append(f"| {det} | {arac} | {k} | {n} | {p:.3f} | [{lo:.3f}, {hi:.3f}] |")
                ozet.append(dict(bolum="esik_gecisi", dedektor=det, grup=arac,
                                 deger=round(p, 4), alt=round(lo, 4), ust=round(hi, 4), n=n))
    sat.append("")

    # ---------------- 4. Wilcoxon ----------------
    sat += ["## 4. Insanlastirmanin etkisi (Wilcoxon isaretli sira testi)", "",
            "Ayni prompt icin ham ve insanlastirilmis metin eslestirilmistir.",
            "Fark = insanlastirilmis - ham (yapaylik skoru uzerinden).",
            "Negatif ortalama fark, insanlastirmanin metni daha az yapay",
            "gosterdigini isaret eder.", "",
            "| dedektor | arac | n | ortalama fark | medyan fark | z | p | |",
            "|---|---|---|---|---|---|---|---|"]
    for det in dedektorler:
        alt = d[d.dedektor == det]
        ham = alt[alt.label == "ai"].set_index(["model", "prompt_id"]).yapaylik
        for arac in araclar:
            h = alt[(alt.label == "humanized") & (alt.humanizer == arac)]
            farklar = [r["yapaylik"] - float(ham.loc[(r["model"], r["prompt_id"])])
                       for _, r in h.iterrows()
                       if (r["model"], r["prompt_id"]) in ham.index]
            if not farklar:
                continue
            s = pd.Series(farklar)
            n, W, z, p = wilcoxon(farklar)
            sat.append(f"| {det} | {arac} | {n} | {s.mean():+.3f} | {s.median():+.3f} | "
                       f"{z:.2f} | {p:.4f} | {yildiz(p)} |")
            ozet.append(dict(bolum="wilcoxon", dedektor=det, grup=arac,
                             deger=round(s.mean(), 4), alt=round(z, 4) if z == z else None,
                             ust=round(p, 5) if p == p else None, n=n))
    sat += ["", "Anlamlilik: *** p<0,001  ** p<0,01  * p<0,05  a.d. = anlamli degil", "",
            "> Not: n=20 ile calisan testlerde guc dusuktur; anlamsiz sonuc",
            "> etkinin yoklugunu degil, mevcut orneklemle gosterilemedigini",
            "> ifade eder.", ""]

    # ---------------- kaydet ----------------
    with open("results/metrikler.md", "w", encoding="utf-8") as f:
        f.write("\n".join(sat))
    pd.DataFrame(ozet).to_csv("results/metrikler_ozet.csv", index=False, encoding="utf-8-sig")

    print("\n".join(sat))
    print()
    print("-> results/metrikler.md")
    print("-> results/metrikler_ozet.csv")


if __name__ == "__main__":
    main()
