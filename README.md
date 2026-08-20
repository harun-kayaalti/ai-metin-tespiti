# Türkçe Metinlerde Yapay Zekâ Dedektörlerinin Denetlenmesi

Yozgat Bozok Üniversitesi — KARDEP Projesi
**Kontrollü Mobil Veri Toplama Altyapısı ile Türkçe Metinlerde Ticari Yapay
Zekâ Dedektörlerinin Yanlış Pozitif ve Kaçırma Davranışının Denetlenmesi**

Stajyer: Harun Kayaaltı · Danışman: Dr. Öğr. Üyesi Çağrı Arısoy
Son güncelleme: 20 Ağustos 2026

---

## 1. Projenin amacı

Ticari yapay zekâ metin dedektörlerinin Türkçe metinlerdeki davranışını
denetlemek. İki soru sorulmaktadır:

1. **Kaçırma:** Yapay zekâ tarafından üretilmiş bir metin, insanlaştırma
   araçlarından geçirildiğinde dedektörler bunu kaçırıyor mu?
2. **Yanlış pozitif:** Gerçekten insan tarafından yazılmış bir metin yanlışlıkla
   yapay olarak işaretleniyor mu?

Bu staj çalışması **birinci soruyu** ele alır. İkinci soru, gerçek katılımcı
metni gerektirdiğinden etik onay süreci tamamlanmadan yanıtlanamaz; altyapı
buna hazır bırakılmıştır (bkz. §7).

Çalışma bir dedektör geliştirme veya model eğitme çalışması **değildir**.
Mevcut araçlar denetlenmekte, açık kaynak bir referans yaklaşım
uygulanmaktadır.

---

## 2. Deney tasarımı

```
4 üretici model  ×  5 sabit prompt  =  20 ham yapay metin
                                    ×  2 insanlaştırma aracı
                                    =  40 insanlaştırılmış metin
                                    ─────────────────────────────
                                       60 metin
```

Her metin üç dedektör tipiyle ölçülmüştür:

| tip | araç | ölçüm |
|---|---|---|
| çok dilli ticari | GPTZero (Model 4.1m, Advanced) | 60 |
| İngilizce odaklı ticari/hibrit | ZeroGPT (web arayüzü, Detect Text) | 60 |
| açık kaynak referans | Perplexity — 3 Türkçe dil modeli | 180 |

**Toplam 300 ölçüm.**

Üretici modeller: ChatGPT, Gemini, Claude, Kumru
İnsanlaştırma araçları: Aithor, Rephraser.co

---

## 3. Klasör yapısı

```
proje/
├── README.md                  bu dosya
├── DEVIR_NOTU.md              çalışmanın konumu, gizlilik durumu, devir adımları
├── ISLER_LISTESI.md           tamamlanan / tamamlanamayan / devam edecek işler
├── requirements.txt           paket sürümleri
├── veri_sozlugu.md            değişken tanımları
├── data_raw/                  veri tabloları — DEĞİŞTİRİLMEZ
│   ├── texts.csv              metin tablosu (60 satır)
│   ├── ai_metadata.csv        yapay zekâ metadata tablosu (60 satır)
│   ├── detector_scores.csv    dedektör skor tablosu (120 satır)
│   └── promptlar.md           beş sabit prompt ve üretim yönergeleri
├── src/                       betikler
│   ├── build_data.py          veri dosyalarını üretir (tek doğruluk kaynağı)
│   ├── veri_kalite_kontrol.py veri seti denetimi
│   ├── perplexity_baseline.py açık kaynak referans yaklaşım
│   ├── metrikler.py           FPR, recall, evasion etkisi, alt grup
│   ├── uyum.py                Cohen kappa, McNemar
│   └── sekiller.py            şekiller
├── results/                   üretilen tablolar
├── figures/                   üretilen şekiller
└── reports/                   LaTeX raporu, haftalık kayıtlar, sunum
```

`data_raw/` içindeki dosyalar elle düzenlenmez. Tüm veri değişiklikleri
`src/build_data.py` içinden yapılır ve dosyalar yeniden üretilir.

Usul ve esaslardaki klasör şablonunda yer alan `data_interim/`,
`data_processed/` ve `notebooks/` klasörleri bu projede kullanılmamaktadır.
Ara işlem adımı bulunmadığından `build_data.py` doğrudan son veri dosyalarını
üretmekte, analizler Jupyter defteri yerine `src/` altındaki betiklerle
yürütülmektedir.

### Çalışmanın diğer parçaları

Depo kod, veri ve sonuçları içerir. Raporun kaynak dosyaları ve staj kayıtları
başka ortamlarda tutulmaktadır:

| içerik | konum |
|---|---|
| LaTeX kaynak dosyaları | Overleaf projesi `Overleaf_Staj_Raporu` |
| Derlenmiş rapor | `reports/Staj_Raporu.pdf` |
| Günlük ve haftalık staj kayıtları | Google Drive staj klasörü |
| Seçim gerekçesi belgeleri, etik belgeleri | Google Drive staj klasörü |

Ayrıntı için `DEVIR_NOTU.md`.

---

## 4. Kurulum

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

Gerekli paketler: `pandas`, `torch`, `transformers`, `matplotlib`.
Perplexity ölçümü ilk çalıştırmada yaklaşık 4 GB model indirir.

---

## 5. Çalıştırma sırası

Betikler proje kök klasöründen, bu sırayla çalıştırılır:

```bash
python src/build_data.py            # 1. veri dosyalarını üret
python src/veri_kalite_kontrol.py   # 2. veri setini denetle (0 uyarı bekleniyor)
python src/perplexity_baseline.py   # 3. açık kaynak referans ölçümleri
python src/metrikler.py             # 4. metrikler
python src/uyum.py                  # 5. dedektörler arası uyum
python src/sekiller.py              # 6. şekiller
```

Her adım bir öncekinin çıktısına bağımlıdır; sıra değiştirilmemelidir.

---

## 6. Üretilen çıktılar

| dosya | içerik |
|---|---|
| `data_raw/texts.csv` | metin tablosu, 60 satır |
| `data_raw/ai_metadata.csv` | yapay zekâ metadata tablosu, 60 satır |
| `data_raw/detector_scores.csv` | dedektör skor tablosu, 120 satır |
| `results/veri_kalite_kontrol.md` | veri seti denetim raporu |
| `results/perplexity_scores.csv` | 180 perplexity ölçümü |
| `results/perplexity_model_bilgisi.txt` | kod sürümü, dil modelleri, eşik durumu |
| `results/perplexity_karsilastirma.md` | perplexity sonuçları |
| `results/metrikler.md` | FPR, recall, evasion etkisi, alt grup analizi |
| `results/uyum.md` | Cohen kappa, McNemar |
| `figures/sekil1..4.png` | sonuç şekilleri |

---

## 7. Veriye erişim ve gizlilik

Veri setinde **kişisel veri bulunmamaktadır.** Tüm metinler dil modelleri
tarafından üretilmiştir. Depo herkese açık biçimde paylaşılabilir.

Etik onay sonrasında katılımcı metni toplanması hâlinde:

- kimlik tablosu ayrı ve yetkili erişimli tutulacak,
- analiz dosyalarında yalnızca kodlanmış veri kullanılacak,
- katılımcı metinleri depoya yüklenmeyecektir.

---

## 8. Bilinen sorunlar ve tamamlanmayan işler

1. **Yanlış pozitif oranı ölçülememiştir.** `human` sınıfı için gerçek
   katılımcı metni gerekir; etik onay süreci staj dönemi içinde
   tamamlanamamıştır.
2. **Perplexity karar eşiği kalibre edilmemiştir.** Aynı nedenle. Betiğe
   kalibrasyon seçeneği eklenmiştir:
   `python src/perplexity_baseline.py --kalibrasyon insan_metinleri.csv`
3. **Örneklem küçüktür** (model başına 5 prompt). Güven aralıkları geniştir;
   sonuçlar eğilim olarak yorumlanmalıdır.
4. **Aday dil modellerinden biri elenmiştir.** `cenkersisman/gpt2-turkish-128-token`
   eğitim bağlam penceresi yetersiz olduğu için kapsam dışıdır; gerekçe
   `results/perplexity_model_bilgisi.txt` içinde kayıtlıdır.
5. **Ticari araçlar zamanla değişir.** Dedektör sürümleri ve ölçüm tarihleri
   kaydedilmiştir; ileride tekrarlanan ölçümler farklı sonuç verebilir.
6. **Üretici model sürümü ve üretim tarihi kaydedilmemiştir.**
   `ai_metadata.csv` içinde bu alanlar `kaydedilmedi` olarak işaretlidir ve
   geriye dönük elde edilemez.
7. **Karma-etkili lojistik regresyon ve sıralı eğilim analizi
   uygulanamamıştır.** Proje metninin 13. bölümünde tanımlıdırlar; katılımcı
   düzeyinde kümelenme ve unvan değişkeni gerektirirler.

---

## 9. Sorumlu

Harun Kayaaltı — stajyer öğrenci
Dr. Öğr. Üyesi Çağrı Arısoy — danışman
