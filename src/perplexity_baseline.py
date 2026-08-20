# -*- coding: utf-8 -*-
"""
Perplexity tabanli acik kaynak referans yaklasimi
AI metin tespiti projesi - ucuncu dedektor tipi

NE YAPAR
  Her metin icin bir Turkce dil modeli altinda perplexity (saskinlik)
  degeri hesaplar. Dusuk perplexity metnin model icin ongorulebilir
  oldugunu gosterir. Yaklasim Mitchell vd. (2023) tarafindan
  tanimlanan sifir-atisli (zero-shot) tespit mantigina dayanir:
  ayri bir siniflandirici EGITILMEZ, hazir bir dil modelinin olasilik
  degerleri kullanilir.

NE YAPMAZ
  Model egitmez, ince ayar yapmaz, siniflandirici gelistirmez.
  Proje bir model gelistirme calismasi degildir; burada yalnizca
  acik kaynak bir referans yaklasim UYGULANMAKTADIR.

ESIK VE KALIBRASYON
  Perplexity esigi, insan yazimi metinlerin dagilimina gore
  belirlenir. Insan metinleri etik onay sureci tamamlanmadan
  toplanamayacagi icin bu asamada esik KALIBRE EDILMEMISTIR.
  Kendi degerlendirme verimizden esik turetmek veri sizintisi
  olacagindan (Staj Usul ve Esaslari s.8.3) bu yol izlenmemistir.

KULLANIM
  python perplexity_baseline.py                       (tum uygun modeller)
  python perplexity_baseline.py --model 0             (tek model)
  python perplexity_baseline.py --kalibrasyon insan.csv
  python perplexity_baseline.py --demo                (model indirmez)

GIRDI   data_raw/texts.csv
CIKTI   results/perplexity_scores.csv
        results/perplexity_model_bilgisi.txt
        results/perplexity_karsilastirma.md
"""

import argparse
import os
import platform
import sys
from datetime import datetime

import pandas as pd

# ----------------------------------------------------------------------
# SABITLER
# ----------------------------------------------------------------------
KOD_SURUMU = "2.2"
DEDEKTOR_ADI = "PerplexityBaseline"

# ----------------------------------------------------------------------
# KULLANILAN OLCUM MODELLERI
#
# Her modelin bir GOREVI vardir; rastgele secilmemislerdir.
#
#   1) ytu-ce-cosmos/turkish-gpt2        (124M)  BIRINCIL
#      Ana sonuclar bunun uzerinden raporlanir. Tek dilli Turkce
#      egitim, egitim verisi belgelenmis, akademik dayanagi var
#      (cosmosGPT, arXiv:2404.17336). Aday havuzunda yayinla
#      desteklenen tek model.
#
#   2) ytu-ce-cosmos/turkish-gpt2-large  (750M)  KAPASITE EKSENI
#      Ayni ekip, ayni veri, alti kat buyuk. Gorevi: bulgularin
#      olcum modelinin kucuklugunden kaynaklanan bir yapaylik olup
#      olmadigini sinamak.
#
#   3) redrussianarmy/gpt2-turkish-cased (124M)  BAGIMSIZ KAYNAK EKSENI
#      Farkli ekip, farkli egitim verisi, ayni boyut. Gorevi:
#      sonucun tek bir ekibin veri secimine bagli olmadigini gostermek.
#
# DAIRESELLIK KISITI: Perplexity modeli, metinleri ureten modellerden
# biri OLAMAZ. Aksi halde model kendi ciktisini dusuk perplexity ile
# odullendirir ve olcum gecersizlesir.
#
# YAPISAL SINIRLILIK: Sifir-atisli perplexity tespiti, olcen model
# ureten modele yaklastikca guclenir. Uretici modeller kapali API
# oldugundan kendi olasilik degerlerine erisilemez; olcum zorunlu
# olarak cok daha kucuk bir modelle yapilmaktadir. Baseline'in mutlak
# performansi bu kosulun tavanidir, uygulamanin eksigi degildir.
# ----------------------------------------------------------------------
MODEL_ADAYLARI = [
    "ytu-ce-cosmos/turkish-gpt2",
    "ytu-ce-cosmos/turkish-gpt2-large",
    "redrussianarmy/gpt2-turkish-cased",
]

BIRINCIL_MODEL = "ytu-ce-cosmos/turkish-gpt2"

# ----------------------------------------------------------------------
# DEGERLENDIRILIP ELENEN ADAYLAR
#
# Bu modeller aday havuzunda yer almis, denenmis ve asagidaki
# gerekcelerle elenmistir. Kayittan silinmemeleri bilincli bir
# tercihtir: Staj Usul ve Esaslari s.4.1 "cikarilan kayitlarin
# gerekcesi yazilir" ilkesi geregi, elenen adayin adi ve gerekcesi
# cikti dosyalarinda gorunur.
#
# Eleme gerekceleri SONUCLARDAN BAGIMSIZDIR; model kartindaki
# beyana ve olculen token sayilarina dayanir.
# ----------------------------------------------------------------------
ELENEN_MODELLER = {
    "cenkersisman/gpt2-turkish-128-token": (
        "Model karti egitim baglam penceresini 128 token olarak bildirmektedir; "
        "calisma metinleri bu modelin sozcuk parcalayicisiyla 294-376 token "
        "uzunlugundadir (ortalama 331). Model, hic egitilmedigi uzunlukta "
        "calistirilmis olur. Ayrica ayni metinleri diger adaylardan iki kattan "
        "fazla parcaya bolmektedir (331'e karsi ~144 token); perplexity token "
        "basina hesaplandigindan degerler diger modellerle karsilastirilamaz. "
        "Bu iki gerekceyle elenmistir."
    ),
}

ESIK_ARALIGI = [20, 30, 40, 50, 60, 80, 100]


# ----------------------------------------------------------------------
# MODEL YUKLEME VE UYGUNLUK DENETIMI
# ----------------------------------------------------------------------
def baglam_siniri(mod):
    """Modelin mimari baglam penceresini config'ten okur."""
    cfg = mod.config
    for alan in ("n_positions", "max_position_embeddings", "n_ctx"):
        v = getattr(cfg, alan, None)
        if isinstance(v, int) and v > 0:
            return v, alan
    return None, None


def model_yukle(model_adi):
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tok = AutoTokenizer.from_pretrained(model_adi)
    mod = AutoModelForCausalLM.from_pretrained(model_adi)
    mod.eval()
    rev = getattr(getattr(mod, "config", None), "_commit_hash", None)
    return tok, mod, rev


def mimari_denetimi(tok, mod, metinler):
    """
    Ek guvence: modelin MIMARI baglam penceresi metinlerden kisaysa eler.

    Not: Bu denetim yalnizca mimariden okunabilen siniri gorur. Egitim
    sirasinda kullanilan pencere config'te yer almadigindan, egitim
    kaynakli kisitlar bu denetimle yakalanmaz; onlar ELENEN_MODELLER
    sozlugunde elle beyan edilir.
    """
    sinir, alan = baglam_siniri(mod)
    uzunluklar = [len(tok(str(m))["input_ids"]) for m in metinler]
    en_uzun = max(uzunluklar)
    ort = sum(uzunluklar) / len(uzunluklar)
    if sinir is None:
        return True, en_uzun, ort, None, "baglam siniri okunamadi"
    if en_uzun > sinir:
        return (False, en_uzun, ort, sinir,
                f"en uzun metin {en_uzun} token, mimari baglam penceresi "
                f"{sinir} token ({alan}).")
    return True, en_uzun, ort, sinir, ""


# ----------------------------------------------------------------------
# PERPLEXITY
# ----------------------------------------------------------------------
def perplexity_hesapla(metin, tok, mod, maks_token):
    """
    perplexity = exp(ortalama capraz entropi kaybi)
    torch.no_grad() zorunludur; gradyan hesabina ihtiyac yoktur.
    """
    import torch

    kod = tok(metin, return_tensors="pt", truncation=True, max_length=maks_token)
    ntok = int(kod["input_ids"].shape[1])
    with torch.no_grad():
        ppl = float(torch.exp(mod(**kod, labels=kod["input_ids"]).loss).detach())
    return ppl, ntok, ntok >= maks_token


def skora_cevir(ppl, esik, olcek=10.0):
    import math
    return 1.0 / (1.0 + math.exp((ppl - esik) / olcek))


def esik_hesapla(insan_ppl, yapay_ppl):
    """YALNIZCA etik onayli insan metinleri mevcutken cagrilir."""
    return float((pd.Series(insan_ppl).median() + pd.Series(yapay_ppl).median()) / 2)


# ----------------------------------------------------------------------
def demo():
    print("DEMO: Model indirilmez; yalnizca skor donusumu test edilir.\n")
    ornek = [("T001", "ai", 22.0), ("T002", "ai", 25.5),
             ("T003", "humanized", 41.0), ("T004", "humanized", 55.2),
             ("T005", "human", 68.0)]
    esik = 41.0
    print(f"{'text_id':<10}{'label':<14}{'ppl':>8}{'skor':>9}{'karar':>9}")
    for tid, lab, ppl in ornek:
        s = skora_cevir(ppl, esik)
        print(f"{tid:<10}{lab:<14}{ppl:>8.1f}{s:>9.3f}{('YZ' if s >= 0.5 else 'insan'):>9}")
    print(f"\nVarsayimsal esik = {esik}. Gercek calistirmada esik yalnizca")
    print("--kalibrasyon dosyasi verildiginde hesaplanir.")


# ----------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="Perplexity tabanli referans yaklasim")
    ap.add_argument("--girdi", default="data_raw/texts.csv")
    ap.add_argument("--model", type=int, default=None, help="Tek model (0,1,2)")
    ap.add_argument("--kalibrasyon", default=None, help="Insan metinleri CSV")
    ap.add_argument("--demo", action="store_true")
    a = ap.parse_args()

    if a.demo:
        demo()
        return
    if not os.path.exists(a.girdi):
        sys.exit(f"HATA: {a.girdi} bulunamadi. Once build_data.py calistirilmali.")

    texts = pd.read_csv(a.girdi)
    # KARDEP Bolum 12: uretici model ve arac bilgisi ayri metadata tablosundadir.
    _mp = os.path.join(os.path.dirname(a.girdi), "ai_metadata.csv")
    if os.path.exists(_mp) and "model" not in texts.columns:
        _md = pd.read_csv(_mp)
        _m = dict(zip(_md.text_id, _md.model_tool))
        _src = dict(zip(_md.text_id, _md.source_text_id))
        texts["model"] = texts.apply(
            lambda r: _m.get(r["text_id"], "") if r["label"] == "ai"
            else _m.get(_src.get(r["text_id"]), ""), axis=1)
        texts["humanizer"] = texts.apply(
            lambda r: _m.get(r["text_id"], "") if r["label"] == "humanized" else "",
            axis=1)
    modeller = MODEL_ADAYLARI if a.model is None else [MODEL_ADAYLARI[a.model]]

    import torch
    import transformers

    os.makedirs("results", exist_ok=True)
    satirlar, bilgi = [], []
    elenen = [(m, g, "beyan edilmis eleme") for m, g in ELENEN_MODELLER.items()]

    bilgi.append("PERPLEXITY REFERANS YAKLASIMI - CALISTIRMA KAYDI")
    bilgi.append("=" * 62)
    bilgi.append(f"Calistirma tarihi   : {datetime.now():%Y-%m-%d %H:%M}")
    bilgi.append(f"Kod surumu          : {KOD_SURUMU}")
    bilgi.append(f"Dedektor adi        : {DEDEKTOR_ADI}")
    bilgi.append(f"Girdi dosyasi       : {a.girdi} ({len(texts)} metin)")
    bilgi.append(f"Birincil model      : {BIRINCIL_MODEL}")
    bilgi.append(f"Python              : {platform.python_version()}")
    bilgi.append(f"torch               : {torch.__version__}")
    bilgi.append(f"transformers        : {transformers.__version__}")
    bilgi.append("")
    bilgi.append("-" * 62)
    bilgi.append("DEGERLENDIRILIP ELENEN ADAYLAR")
    bilgi.append("-" * 62)
    if ELENEN_MODELLER:
        for m, g in ELENEN_MODELLER.items():
            bilgi.append(f"{m}")
            for satir in [g[i:i + 66] for i in range(0, len(g), 66)]:
                bilgi.append(f"    {satir}")
            bilgi.append("")
    else:
        bilgi.append("(yok)")
        bilgi.append("")
    bilgi.append("Eleme gerekceleri sonuclardan bagimsizdir; model kartindaki")
    bilgi.append("beyana ve olculen token sayilarina dayanir.")
    bilgi.append("")
    bilgi.append("-" * 62)
    bilgi.append("KULLANILAN MODELLER")
    bilgi.append("-" * 62)

    for model_adi in modeller:
        if model_adi in ELENEN_MODELLER:
            print(f"\n>>> {model_adi}\n    ATLANDI (beyan edilmis eleme)")
            continue

        print(f"\n>>> {model_adi}")
        try:
            tok, mod, rev = model_yukle(model_adi)
        except Exception as e:
            print(f"    YUKLENEMEDI: {e}")
            bilgi.append(f"{model_adi}  -> YUKLENEMEDI ({e})")
            bilgi.append("")
            elenen.append((model_adi, f"yuklenemedi: {e}", "teknik hata"))
            continue

        uygun, en_uzun, ort_tok, sinir, not_ = mimari_denetimi(
            tok, mod, texts["raw_text"].tolist())

        bilgi.append(f"{model_adi}")
        bilgi.append(f"    revizyon          : {rev or 'kayit yok'}")
        bilgi.append(f"    baglam penceresi  : {sinir if sinir else 'okunamadi'} token")
        bilgi.append(f"    metin uzunlugu    : ortalama {ort_tok:.1f}, en uzun {en_uzun} token")

        if not uygun:
            print(f"    ELENDI: {not_}")
            bilgi.append(f"    DURUM             : ELENDI - {not_}")
            bilgi.append("")
            elenen.append((model_adi, not_, "mimari denetim"))
            continue

        bilgi.append(f"    DURUM             : kullanildi")

        kirpilan = 0
        for i, r in texts.iterrows():
            ppl, ntok, kirp = perplexity_hesapla(str(r["raw_text"]), tok, mod, sinir or 1024)
            kirpilan += int(kirp)
            satirlar.append(dict(
                text_id=r["text_id"], label=r["label"], model=r["model"],
                prompt_id=r["prompt_id"], humanizer=r.get("humanizer", ""),
                dil_modeli=model_adi,
                birincil="evet" if model_adi == BIRINCIL_MODEL else "hayir",
                perplexity=round(ppl, 3), token_sayisi=ntok,
                kirpildi="evet" if kirp else "hayir"))
            if (i + 1) % 20 == 0:
                print(f"    {i + 1}/{len(texts)}")
        bilgi.append(f"    kirpilan metin    : {kirpilan}")
        bilgi.append("")

    if not satirlar:
        sys.exit("HATA: Uygun bulunan hicbir dil modeli calistirilamadi.")

    df = pd.DataFrame(satirlar)

    # ---------------- esik / kalibrasyon ----------------
    if a.kalibrasyon:
        ins = pd.read_csv(a.kalibrasyon)
        print(f"\n>>> Kalibrasyon: {len(ins)} insan metni")
        tok, mod, _ = model_yukle(BIRINCIL_MODEL)
        sinir, _ = baglam_siniri(mod)
        ins_ppl = [perplexity_hesapla(str(r["raw_text"]), tok, mod, sinir or 1024)[0]
                   for _, r in ins.iterrows()]
        esik = esik_hesapla(ins_ppl, df[df.dil_modeli == BIRINCIL_MODEL].perplexity)
        df["esik"] = round(esik, 3)
        df["score"] = df.perplexity.apply(lambda p: round(skora_cevir(p, esik), 4))
        df["binary_label"] = (df.score >= 0.50).astype(int)
        bilgi.append(f"Esik ayari          : {esik:.3f}  (KALIBRE EDILMIS)")
        bilgi.append(f"    kaynak            : {a.kalibrasyon} ({len(ins)} insan metni)")
        bilgi.append(f"    referans model    : {BIRINCIL_MODEL}")
        bilgi.append(f"    yontem            : insan ve yapay medyanlarinin orta noktasi")
    else:
        df["esik"] = None
        df["score"] = None
        df["binary_label"] = None
        bilgi.append("Esik ayari          : KALIBRE EDILMEMIS")
        bilgi.append("    gerekce           : Insan yazimi metinler etik onay sureci")
        bilgi.append("                        tamamlanmadan toplanamamaktadir. Esigin")
        bilgi.append("                        degerlendirme verisinden turetilmesi veri")
        bilgi.append("                        sizintisi olusturacagindan yapilmamistir.")
        bilgi.append("    sonraki adim      : --kalibrasyon <insan_metinleri.csv>")
    bilgi.append("")

    df.to_csv("results/perplexity_scores.csv", index=False, encoding="utf-8-sig")

    # ---------------- rapor ----------------
    sat = ["# Perplexity Referans Yaklasimi - Sonuclar", "",
           f"Uretim tarihi: {datetime.now():%Y-%m-%d}", "",
           "Perplexity, metnin dil modeli tarafindan ne kadar ongorulebilir",
           "oldugunu gosterir. Dusuk deger daha ongorulebilir metni isaret eder.",
           "", f"Birincil olcum modeli: `{BIRINCIL_MODEL}`. Diger modeller",
           "sonuclarin olcum modeli secimine duyarliligini sinamak icindir.", ""]

    sat += ["## 0. Degerlendirilip elenen aday modeller", ""]
    if elenen:
        sat += ["| model | eleme turu | gerekce |", "|---|---|---|"]
        for m, g, tur in elenen:
            sat.append(f"| `{m}` | {tur} | {g} |")
        sat += ["", "Eleme gerekceleri sonuclardan bagimsizdir; model kartindaki",
                "beyana ve olculen token sayilarina dayanir. Elenen adaylar",
                "kayittan silinmemis, gerekceleriyle birlikte belgelenmistir.", ""]
    else:
        sat += ["Elenen aday bulunmamaktadir.", ""]

    sat += ["## 1. Sinif bazinda perplexity", "",
            "| dil modeli | sinif | metin | ortalama | medyan | en dusuk | en yuksek |",
            "|---|---|---|---|---|---|---|"]
    for (dm, lab), g in df.groupby(["dil_modeli", "label"]):
        sat.append(f"| {dm.split('/')[-1]} | {lab} | {len(g)} | {g.perplexity.mean():.1f} | "
                   f"{g.perplexity.median():.1f} | {g.perplexity.min():.1f} | {g.perplexity.max():.1f} |")
    sat.append("")

    sat += ["## 2. Insanlastirma perplexity'yi degistiriyor mu", "",
            "Ayni promptun ham ve insanlastirilmis hali eslestirilerek",
            "karsilastirilmistir. Pozitif fark, insanlastirmanin metni dil",
            "modeli icin daha ongorulemez hale getirdigini gosterir.", "",
            "| dil modeli | arac | eslesme | ortalama fark | artan | azalan |",
            "|---|---|---|---|---|---|"]
    for dm, g in df.groupby("dil_modeli"):
        ham = g[g.label == "ai"].set_index(["model", "prompt_id"]).perplexity
        for arac, h in g[g.label == "humanized"].groupby("humanizer"):
            f = [r["perplexity"] - float(ham.loc[(r["model"], r["prompt_id"])])
                 for _, r in h.iterrows() if (r["model"], r["prompt_id"]) in ham.index]
            if f:
                s = pd.Series(f)
                sat.append(f"| {dm.split('/')[-1]} | {arac} | {len(s)} | {s.mean():+.1f} | "
                           f"{(s > 0).sum()} | {(s < 0).sum()} |")
    sat.append("")

    sat += ["## 3. Uretici model bazinda ham metin perplexity", "",
            "| dil modeli | uretici model | ortalama | medyan |", "|---|---|---|---|"]
    for (dm, um), g in df[df.label == "ai"].groupby(["dil_modeli", "model"]):
        sat.append(f"| {dm.split('/')[-1]} | {um} | {g.perplexity.mean():.1f} | {g.perplexity.median():.1f} |")
    sat += ["", "> Uyari: Turkce icin egitilmis bir uretici modelin ciktilari, olcum",
            "> icin kullanilan Turkce dil modeliyle benzer derlemelerden beslenmis",
            "> olabilir. Bu durumda dusuk perplexity metnin yapay olmasindan degil,",
            "> ayni dil dagilimini paylasmasindan kaynaklanabilir.", "",
            "> Yapisal sinirlilik: Uretici modeller kapali API oldugundan kendi",
            "> olasilik degerlerine erisilemez. Olcum, uretici modellerden cok daha",
            "> kucuk acik modellerle yapilmaktadir; baseline'in mutlak performansi",
            "> bu kosulun tavanidir.", ""]

    if not a.kalibrasyon:
        sat += ["## 4. Esik duyarlilik analizi", "",
                "Esik kalibre edilmedigi icin, farkli esik degerlerinde kac metnin",
                "esigin altinda kalacagi bilgi amacli verilmistir. Bu bir tespit",
                "performansi degildir; insan sinifi bulunmadigindan duyarlilik ve",
                "yanlis pozitif orani hesaplanamaz.", "",
                "| dil modeli | " + " | ".join(f"esik {e}" for e in ESIK_ARALIGI) + " |",
                "|---" * (len(ESIK_ARALIGI) + 1) + "|"]
        for dm, g in df.groupby("dil_modeli"):
            sat.append(f"| {dm.split('/')[-1]} | " +
                       " | ".join(f"{(g.perplexity < e).mean() * 100:.0f}%" for e in ESIK_ARALIGI) + " |")
        sat.append("")

    with open("results/perplexity_karsilastirma.md", "w", encoding="utf-8") as f:
        f.write("\n".join(sat))
    with open("results/perplexity_model_bilgisi.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(bilgi))

    print(f"\nKullanilan model: {df.dil_modeli.nunique()} | Toplam olcum: {len(df)}")
    print(f"Elenen aday     : {len(elenen)}")
    print("-> results/perplexity_scores.csv")
    print("-> results/perplexity_model_bilgisi.txt")
    print("-> results/perplexity_karsilastirma.md")


if __name__ == "__main__":
    main()
