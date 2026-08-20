# -*- coding: utf-8 -*-
"""
KARDEP Bolum 13 -- Metrikler ve Istatistiksel Analiz

Bu betik yalnizca proje metninin 13. bolumunde tanimlanan metrikleri hesaplar.
Proje metninde yer almayan hicbir olcut eklenmemistir.

Bolum 13 listesi ve bu betikteki karsiliklari:

  Yanlis pozitif orani (FPR)      -> Bolum 1  (insan sinifi yok, hesaplanamiyor)
  Recall / yakalama orani         -> Bolum 2
  Evasion etkisi                  -> Bolum 4
  Wilson %95 guven araligi        -> tum oranlarda
  Karma-etkili lojistik regresyon -> katilimci verisi gerektirir, kapsam disi
  Sirali egilim analizi           -> katilimci verisi gerektirir, kapsam disi
  McNemar testi                   -> uyum.py
  Cohen/Fleiss kappa              -> uyum.py
  Alt grup analizleri             -> Bolum 5 (uzunluk kirilimi)

Cikti: results/metrikler.md , results/metrikler_ozet.csv
"""

import csv, math, os
from collections import defaultdict

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEXTS = os.path.join(KOK, "data_raw", "texts.csv")
SCORES = os.path.join(KOK, "data_raw", "detector_scores.csv")
META   = os.path.join(KOK, "data_raw", "ai_metadata.csv")
CIKTI_MD = os.path.join(KOK, "results", "metrikler.md")
CIKTI_CSV = os.path.join(KOK, "results", "metrikler_ozet.csv")

Z = 1.959963984540054  # %95


# ----------------------------------------------------------------------
# Wilson %95 guven araligi  (KARDEP Bolum 13)
# ----------------------------------------------------------------------
def wilson(k, n, z=Z):
    if n == 0:
        return (None, None, None)
    p = k / n
    payda = 1 + z * z / n
    merkez = (p + z * z / (2 * n)) / payda
    yari = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / payda
    return (p, max(0.0, merkez - yari), min(1.0, merkez + yari))


def o(x, b=3):
    return "-" if x is None else f"{x:.{b}f}".replace(".", ",")


def yuzde(x):
    return "-" if x is None else f"%{x*100:.1f}".replace(".", ",")


# ----------------------------------------------------------------------
def veri_yukle():
    # KARDEP Bolum 12: uretici model ve arac bilgisi ayri metadata tablosundadir.
    meta = {r["text_id"]: r for r in csv.DictReader(open(META, encoding="utf-8-sig"))}

    metinler = {}
    for r in csv.DictReader(open(TEXTS, encoding="utf-8-sig")):
        r["word_count"] = int(r["word_count"])
        m = meta.get(r["text_id"], {})
        if r["label"] == "ai":
            r["model"], r["humanizer"] = m.get("model_tool", ""), ""
        elif r["label"] == "humanized":
            kaynak = m.get("source_text_id", "")
            r["model"] = meta.get(kaynak, {}).get("model_tool", "")
            r["humanizer"] = m.get("model_tool", "")
        else:
            r["model"] = r["humanizer"] = ""
        metinler[r["text_id"]] = r

    olcumler = []
    for r in csv.DictReader(open(SCORES, encoding="utf-8-sig")):
        m = metinler.get(r["text_id"])
        if m is None:
            continue
        olcumler.append({
            "text_id": r["text_id"],
            "detector": r["detector_name"],
            "binary": int(r["binary_label"]),
            "label": m["label"],
            "model": m["model"],
            "humanizer": m["humanizer"],
            "prompt_id": m["prompt_id"],
            "word_count": m["word_count"],
        })
    return metinler, olcumler


def oran(kayitlar):
    n = len(kayitlar)
    k = sum(x["binary"] for x in kayitlar)
    return k, n, wilson(k, n)


# ----------------------------------------------------------------------
def main():
    metinler, olcumler = veri_yukle()
    dedektorler = sorted({x["detector"] for x in olcumler})
    humanizerlar = sorted({x["humanizer"] for x in olcumler if x["humanizer"]})
    modeller = sorted({x["model"] for x in olcumler if x["label"] == "ai"})

    L = []
    ozet = [["bolum", "dedektor", "kirilim", "k", "n", "oran", "alt_sinir", "ust_sinir"]]

    L.append("# KARDEP Bolum 13 -- Metrikler\n")
    L.append(f"Metin: {len(metinler)} | Olcum: {len(olcumler)} | "
             f"Dedektor: {len(dedektorler)}\n")
    L.append("Bu dosya yalnizca proje metninin 13. bolumunde tanimlanan "
             "metrikleri icerir.\n")

    # ---------------- 1. Yanlis pozitif orani (ana metrik) -------------
    L.append("\n## 1. Yanlis pozitif orani (FPR)\n")
    insan = [x for x in olcumler if x["label"] == "human"]
    if insan:
        L.append("| Dedektor | Yanlis pozitif | n | FPR | Wilson %95 |")
        L.append("|---|---|---|---|---|")
        for d in dedektorler:
            k, n, (p, a, b) = oran([x for x in insan if x["detector"] == d])
            L.append(f"| {d} | {k} | {n} | {o(p)} | [{o(a)} ; {o(b)}] |")
            ozet.append(["FPR", d, "insan", k, n, o(p), o(a), o(b)])
    else:
        L.append("Projenin ana metrigidir. Insan yazimi metin sinifi bu asamada "
                 "olusturulamadigindan hesaplanamamistir. Katilimci metinleri "
                 "etik kurul onayina baglidir.\n")
        ozet.append(["FPR", "-", "insan sinifi yok", 0, 0, "-", "-", "-"])

    # ---------------- 2. Recall / yakalama orani -----------------------
    L.append("\n## 2. Recall / yakalama orani -- ham yapay zeka metinleri\n")
    L.append("Ham yapay zeka metinlerinin dedektorler tarafindan yakalanma orani.\n")
    ham = [x for x in olcumler if x["label"] == "ai"]
    ham_recall = {}
    L.append("| Dedektor | Yakalanan | n | Recall | Wilson %95 |")
    L.append("|---|---|---|---|---|")
    for d in dedektorler:
        k, n, (p, a, b) = oran([x for x in ham if x["detector"] == d])
        ham_recall[d] = p
        L.append(f"| {d} | {k} | {n} | {o(p)} | [{o(a)} ; {o(b)}] |")
        ozet.append(["recall_ham", d, "tum", k, n, o(p), o(a), o(b)])

    L.append("\n### Uretici model bazinda\n")
    L.append("| Dedektor | Model | Yakalanan | n | Recall | Wilson %95 |")
    L.append("|---|---|---|---|---|---|")
    for d in dedektorler:
        for m in modeller:
            k, n, (p, a, b) = oran([x for x in ham
                                    if x["detector"] == d and x["model"] == m])
            L.append(f"| {d} | {m} | {k} | {n} | {o(p)} | [{o(a)} ; {o(b)}] |")
            ozet.append(["recall_ham", d, m, k, n, o(p), o(a), o(b)])

    # ---------------- 3. Recall -- insanlastirilmis ---------------------
    L.append("\n## 3. Recall / yakalama orani -- insanlastirilmis metinler\n")
    ins = [x for x in olcumler if x["label"] == "humanized"]
    hum_recall = {}
    L.append("| Dedektor | Insanlastirma araci | Yakalanan | n | Recall | Wilson %95 |")
    L.append("|---|---|---|---|---|---|")
    for d in dedektorler:
        for h in humanizerlar:
            k, n, (p, a, b) = oran([x for x in ins
                                    if x["detector"] == d and x["humanizer"] == h])
            hum_recall[(d, h)] = p
            L.append(f"| {d} | {h} | {k} | {n} | {o(p)} | [{o(a)} ; {o(b)}] |")
            ozet.append(["recall_humanized", d, h, k, n, o(p), o(a), o(b)])

    # ---------------- 4. Evasion etkisi ---------------------------------
    L.append("\n## 4. Evasion etkisi\n")
    L.append("KARDEP tanimi: ham yapay zeka recall degeri ile humanized recall "
             "degeri arasindaki dusus.\n")
    L.append("`Evasion etkisi = Recall(ham) - Recall(insanlastirilmis)`\n")
    L.append("Pozitif deger dususu, negatif deger insanlastirmanin metni daha "
             "yakalanabilir hale getirdigini gosterir.\n")
    L.append("| Dedektor | Insanlastirma araci | Recall(ham) | Recall(ins.) | Evasion etkisi |")
    L.append("|---|---|---|---|---|")
    for d in dedektorler:
        for h in humanizerlar:
            rh, ri = ham_recall[d], hum_recall[(d, h)]
            fark = None if (rh is None or ri is None) else rh - ri
            isaret = "" if fark is None else ("+" if fark > 0 else "")
            L.append(f"| {d} | {h} | {o(rh)} | {o(ri)} | {isaret}{o(fark)} |")
            ozet.append(["evasion_etkisi", d, h, "", "",
                         f"{isaret}{o(fark)}", "", ""])

    L.append("\n### Insanlastirma araci ayrimi yapilmadan\n")
    L.append("| Dedektor | Recall(ham) | Recall(ins.) | Evasion etkisi |")
    L.append("|---|---|---|---|")
    for d in dedektorler:
        k, n, (ri, _, _) = oran([x for x in ins if x["detector"] == d])
        rh = ham_recall[d]
        fark = None if (rh is None or ri is None) else rh - ri
        isaret = "" if fark is None else ("+" if fark > 0 else "")
        L.append(f"| {d} | {o(rh)} | {o(ri)} | {isaret}{o(fark)} |")
        ozet.append(["evasion_etkisi", d, "tum araclar", "", "",
                     f"{isaret}{o(fark)}", "", ""])

    # ---------------- 5. Alt grup analizi: uzunluk ----------------------
    L.append("\n## 5. Alt grup analizi -- metin uzunlugu\n")
    kelimeler = sorted(m["word_count"] for m in metinler.values())
    n2 = len(kelimeler)
    medyan = (kelimeler[n2 // 2] if n2 % 2 else
              (kelimeler[n2 // 2 - 1] + kelimeler[n2 // 2]) / 2)
    L.append(f"Tum metinlerin kelime sayisi medyani: {medyan:.1f}".replace(".", ",")
             + " kelime.\n")
    L.append("Ham yapay zeka metinleri tasarim geregi 100-120 kelime bandindadir; "
             "bant ici / bant disi ayrimi bu sinif icin islevsizdir. Bu nedenle "
             "kirilim medyan bolmesiyle yapilmistir.\n")
    L.append("| Dedektor | Sinif | Uzunluk | Yakalanan | n | Recall | Wilson %95 |")
    L.append("|---|---|---|---|---|---|---|")
    for d in dedektorler:
        for sinif, kume in (("ham", ham), ("insanlastirilmis", ins)):
            for ad, kosul in (("medyan alti", lambda w: w <= medyan),
                              ("medyan ustu", lambda w: w > medyan)):
                secim = [x for x in kume
                         if x["detector"] == d and kosul(x["word_count"])]
                if not secim:
                    continue
                k, n, (p, a, b) = oran(secim)
                L.append(f"| {d} | {sinif} | {ad} | {k} | {n} | {o(p)} | "
                         f"[{o(a)} ; {o(b)}] |")
                ozet.append([f"altgrup_uzunluk_{sinif}", d, ad, k, n,
                             o(p), o(a), o(b)])

    # ---------------- 6. Kapsam disi kalan metrikler --------------------
    L.append("\n## 6. Bu asamada hesaplanamayan Bolum 13 metrikleri\n")
    L.append("| Metrik | Gerekce |")
    L.append("|---|---|")
    L.append("| Yanlis pozitif orani (FPR) | Insan yazimi metin sinifi yok. |")
    L.append("| Karma-etkili lojistik regresyon | Katilimci duzeyinde kumelenme "
             "gerektirir; katilimci verisi yok. |")
    L.append("| Sirali egilim analizi | Egitim seviyesi / unvan degiskeni "
             "katilimci verisiyle gelir. |")
    L.append("| Alt grup: fakulte, yazma sikligi | Katilimci verisiyle gelir. |")

    os.makedirs(os.path.dirname(CIKTI_MD), exist_ok=True)
    open(CIKTI_MD, "w", encoding="utf-8").write("\n".join(L) + "\n")
    with open(CIKTI_CSV, "w", encoding="utf-8", newline="") as f:
        csv.writer(f).writerows(ozet)

    print("yazildi:", CIKTI_MD)
    print("yazildi:", CIKTI_CSV)
    for d in dedektorler:
        print(f"  {d}: recall(ham) = {o(ham_recall[d])}")


if __name__ == "__main__":
    main()
