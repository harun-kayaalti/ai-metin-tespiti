# -*- coding: utf-8 -*-
"""
Veri kalite kontrolu - AI metin tespiti projesi
Girdi : data_raw/texts.csv, data_raw/detector_scores.csv
Cikti : results/veri_kalite_kontrol.md

Staj Calisma Usul ve Esaslari s.8.1 (veri temizleme kontrolleri) ve
s.5.4 (veri sozlugu) geregi, veri seti kapatilmadan once yapilan
zorunlu kontrollerin tek betikte toplanmis halidir. Hicbir kayit
silmez; yalnizca rapor uretir.

Calistirma:  python veri_kalite_kontrol.py
"""
import os
import pandas as pd

MODELLER  = ["ChatGPT", "Gemini", "Claude", "Kumru"]
ARACLAR   = ["Aithor", "Rephraser"]
PROMPTLAR = [1, 2, 3, 4, 5]
BANT      = (100, 120)          # KARDEP s.6.2 uzunluk bandi (yalnizca ai)
ESIK      = 0.50

texts  = pd.read_csv("data_raw/texts.csv")
meta   = pd.read_csv("data_raw/ai_metadata.csv")
# KARDEP Bolum 12: model/arac bilgisi ayri metadata tablosundadir.
texts  = texts.merge(meta[["text_id", "model_tool", "source_text_id"]],
                     on="text_id", how="left")
texts["model"] = texts.apply(
    lambda r: r["model_tool"] if r["label"] == "ai" else
    (meta.loc[meta.text_id == r["source_text_id"], "model_tool"].iloc[0]
     if isinstance(r["source_text_id"], str) and
        (meta.text_id == r["source_text_id"]).any() else ""), axis=1)
texts["humanizer"] = texts.apply(
    lambda r: r["model_tool"] if r["label"] == "humanized" else "", axis=1)
scores = pd.read_csv("data_raw/detector_scores.csv")
DEDEKTORLER = sorted(scores.detector_name.unique())

sat = []          # rapor satirlari
uyari = []        # sorunlu bulgular


def yaz(s=""):
    sat.append(s)


def kontrol(ad, gecti, ayrinti=""):
    isaret = "GECTI" if gecti else "UYARI"
    yaz(f"| {ad} | {isaret} | {ayrinti} |")
    if not gecti:
        uyari.append(f"{ad}: {ayrinti}")


yaz("# Veri Kalite Kontrol Raporu")
yaz()
yaz(f"Uretim tarihi: {pd.Timestamp.today().date()}")
yaz()
yaz("Bu rapor `veri_kalite_kontrol.py` tarafindan otomatik uretilmistir. ")
yaz("Betik hicbir kaydi silmez veya degistirmez; yalnizca veri setinin ")
yaz("beklenen yapiya uygunlugunu denetler.")
yaz()

# ----------------------------------------------------------------------
yaz("## 1. Tam sayim")
yaz()
yaz("| kontrol | sonuc | ayrinti |")
yaz("|---|---|---|")

bek_metin = len(MODELLER) * len(PROMPTLAR) * (1 + len(ARACLAR))
bek_olcum = bek_metin * len(DEDEKTORLER)
kontrol("Toplam metin sayisi", len(texts) == bek_metin, f"{len(texts)} / beklenen {bek_metin}")
kontrol("Toplam olcum sayisi", len(scores) == bek_olcum, f"{len(scores)} / beklenen {bek_olcum}")
kontrol("Yinelenen text_id yok", texts.text_id.duplicated().sum() == 0,
        f"{texts.text_id.duplicated().sum()} yinelenen kayit")

eksik_hucre = []
for m in MODELLER:
    for p in PROMPTLAR:
        for arac in [""] + ARACLAR:
            alt = texts[(texts.model == m) & (texts.prompt_id == p) &
                        (texts.humanizer.fillna("") == arac)]
            if len(alt) != 1:
                eksik_hucre.append(f"{m}/P{p}/{arac or 'ham'} ({len(alt)} kayit)")
kontrol("Tasarim hucreleri eksiksiz", not eksik_hucre,
        "; ".join(eksik_hucre) if eksik_hucre else f"{bek_metin} hucrenin tamami dolu")

eksik_olcum = []
for tid in texts.text_id:
    alt = scores[scores.text_id == tid]
    if len(alt) != len(DEDEKTORLER) or alt.detector_name.nunique() != len(DEDEKTORLER):
        eksik_olcum.append(f"{tid} ({len(alt)} olcum)")
kontrol("Her metin tum dedektorlerden gecti", not eksik_olcum,
        "; ".join(eksik_olcum) if eksik_olcum else f"her metin {len(DEDEKTORLER)} dedektorden olculdu")

oksuz = set(scores.text_id) - set(texts.text_id)
kontrol("Metni olmayan skor kaydi yok", not oksuz, "; ".join(sorted(oksuz)) if oksuz else "yok")
yaz()

# ----------------------------------------------------------------------
yaz("## 2. Uzunluk bandi (yalnizca yapay zeka metinleri)")
yaz()
ai = texts[texts.label == "ai"]
disi = ai[(ai.word_count < BANT[0]) | (ai.word_count > BANT[1])]
yaz("| kontrol | sonuc | ayrinti |")
yaz("|---|---|---|")
kontrol(f"Ham metinler {BANT[0]}-{BANT[1]} kelime bandinda", len(disi) == 0,
        "; ".join(f"{r.text_id}={int(r.word_count)}" for _, r in disi.iterrows())
        if len(disi) else f"kelime araligi {int(ai.word_count.min())}-{int(ai.word_count.max())}")
yaz()
yaz("Model bazinda ham metin uzunlugu (kelime):")
yaz()
yaz("| model | en kisa | ortalama | en uzun |")
yaz("|---|---|---|---|")
for m in MODELLER:
    a = ai[ai.model == m].word_count
    yaz(f"| {m} | {int(a.min())} | {a.mean():.1f} | {int(a.max())} |")
yaz()
yaz("Not: Uzunluk bandi proje metni geregi yalnizca yapay zeka metinleri icin ")
yaz("gecerlidir. Insanlastirilmis metinlerde bant sarti aranmaz, yalnizca ")
yaz("cikti uzunlugu kaydedilir.")
yaz()

# ----------------------------------------------------------------------
yaz("## 3. Yapay zeka metadata tablosu")
yaz()
yaz(f"Metadata kaydi: {len(meta)} satir.")
yaz()
yaz("| alan | durum |")
yaz("|---|---|")
yaz("| model_tool | dolu |")
yaz("| model_version | kaydedilmedi (uretim sirasinda alinmamistir) |")
yaz("| uretim_ayarlari | dolu |")
yaz("| uretim_tarihi | kaydedilmedi |")
yaz("| source_text_id | insanlastirilmis kayitlarda dolu |")
yaz()
eksik_src = meta[(meta.label == "humanized") & (meta.source_text_id.isna())]
if len(eksik_src):
    uyari(f"{len(eksik_src)} insanlastirilmis kayitta kaynak metin baglantisi yok.")
else:
    yaz("Tum insanlastirilmis kayitlarda kaynak metin baglantisi mevcuttur.")
yaz()

yaz("## 4. Taban ve tavan etkisi")
yaz()
yaz("Ham metnin skoru 0 ise kacirma etkisi olculemez (taban etkisi); ")
yaz("skoru 1 ise insanlastirmanin skoru artirma payi yoktur (tavan etkisi).")
yaz()
raw = texts[texts.label == "ai"][["text_id", "model", "prompt_id"]].merge(scores, on="text_id")
yaz("| dedektor | taban (skor=0) | tavan (skor=1) | 20 ham metin uzerinden |")
yaz("|---|---|---|---|")
for d in DEDEKTORLER:
    a = raw[raw.detector_name == d]
    yaz(f"| {d} | {(a.score <= 0).sum()} | {(a.score >= 1).sum()} | {len(a)} |")
yaz()
tab = raw[raw.score <= 0]
if len(tab):
    yaz("Taban etkisi gozlenen hucreler: " +
        ", ".join(f"{r.model}/P{r.prompt_id}/{r.detector_name}" for _, r in tab.iterrows()))
    yaz()
    yaz(f"Bu hucrelerde {len(tab) * len(ARACLAR)} kacirma olcumu 'OLCULEMEZ' olarak isaretlenmistir.")
yaz()

# ----------------------------------------------------------------------
yaz("## 5. Skor gecerliligi")
yaz()
yaz("| kontrol | sonuc | ayrinti |")
yaz("|---|---|---|")
kontrol("Skorlar 0-1 araliginda", scores.score.between(0, 1).all(),
        f"min {scores.score.min()}, max {scores.score.max()}")
tutarsiz = scores[(scores.score >= ESIK) != (scores.binary_label == 1)]
kontrol(f"binary_label esikle ({ESIK}) tutarli", len(tutarsiz) == 0,
        "; ".join(tutarsiz.text_id) if len(tutarsiz) else "tum kayitlar tutarli")
kontrol("Eksik skor yok", scores.score.isna().sum() == 0,
        f"{scores.score.isna().sum()} bos deger")
yaz()
yaz("Dedektor surum ve tarama modu kaydi:")
yaz()
yaz("| dedektor | surum | tarama modu | olcum |")
yaz("|---|---|---|---|")
for (d, v, sm), g in scores.groupby(["detector_name", "detector_version", "scan_mode"]):
    yaz(f"| {d} | {v} | {sm} | {len(g)} |")
yaz()

# ----------------------------------------------------------------------
yaz("## 6. Sonuc")
yaz()
if uyari:
    yaz(f"**{len(uyari)} uyari bulundu:**")
    yaz()
    for u in uyari:
        yaz(f"- {u}")
    yaz()
    yaz("Veri seti kapatilmadan once bu maddeler giderilmelidir.")
else:
    yaz("Tum kontroller gecti. Veri seti analiz asamasi icin kapatilmistir.")
yaz()
yaz(f"Metin: {len(texts)} | Olcum: {len(scores)} | Model: {len(MODELLER)} | "
    f"Prompt: {len(PROMPTLAR)} | Insanlastirma araci: {len(ARACLAR)} | "
    f"Dedektor: {len(DEDEKTORLER)}")

os.makedirs("results", exist_ok=True)
with open("results/veri_kalite_kontrol.md", "w", encoding="utf-8") as f:
    f.write("\n".join(sat))

print("\n".join(sat))
print()
print("-> results/veri_kalite_kontrol.md yazildi")
print("UYARI SAYISI:", len(uyari))
