# Veri Sözlüğü

Yozgat Bozok Üniversitesi — KARDEP Projesi
Kontrollü Mobil Veri Toplama Altyapısı ile Türkçe Metinlerde Ticari Yapay Zekâ
Dedektörlerinin Yanlış Pozitif ve Kaçırma Davranışının Denetlenmesi

Hazırlayan: Harun Kayaaltı · Danışman: Dr. Öğr. Üyesi Çağrı Arısoy
Son güncelleme: 14 Ağustos 2026

Bu belge, Staj Çalışma Usul ve Esasları §5.4 uyarınca veri setindeki her
değişkenin anlamını, veri türünü, geçerli değerlerini ve üretim yöntemini
açıklar. Amaç, veri setinin başka bir araştırmacı tarafından doğru
yorumlanabilmesidir.

---

## 1. Sınıf tanımları

| sınıf | tanım | proje kapsamı |
|---|---|---|
| `human` | Gerçek kişi tarafından yazılmış metin | **Toplanmadı.** Etik onay süreci tamamlanmadan katılımcı metni toplanamaz (Usul ve Esaslar §13.3). |
| `ai` | Üretici bir dil modelinin sabit prompta verdiği ham yanıt | 20 metin |
| `humanized` | Bir `ai` metnin ticari insanlaştırma aracından geçirilmiş hâli | 40 metin |

Bu ayrım proje metnindeki sınıf tanımlarına uyar. `human` sınıfının
bulunmaması, yanlış pozitif oranının bu aşamada ölçülememesinin nedenidir.

---

## 2. `data_raw/texts.csv` — metin tablosu (60 satır)

Alanlar proje metninin 12. bölümünde tanımlanan metin tablosu şemasıyla
birebir aynıdır. Şemada yer almayan alan eklenmemiştir.

| değişken | açıklama | tür | geçerli değerler | üretim yöntemi |
|---|---|---|---|---|
| `text_id` | Metnin tekil kimliği | metin | T001–T060 | elle atanır, tekrar kullanılmaz |
| `label` | Metnin sınıfı | kategorik | `ai`, `humanized`, `human` | üretim aşamasında belirlenir |
| `participant_id` | Anonim katılımcı kimliği | metin | boş | yalnızca `label=human` satırlarında dolar; bu aşamada human metni yoktur |
| `prompt_id` | Kullanılan sabit promptun numarası | tam sayı | 1–5 | `data_raw/promptlar.md` |
| `raw_text` | Metnin tam hâli | metin | — | araçtan alındığı gibi, düzeltilmeden |
| `word_count` | Kelime sayısı | tam sayı | 97–132 | `raw_text` boşluklara bölünerek |
| `char_count` | Karakter sayısı | tam sayı | — | `len(raw_text)` |
| `length_band` | Uzunluk bandına uygunluk | kategorik | `uygun`, `bant disi`, `uygulanmaz` | 100–120 kelime bandı; yalnızca `label=ai` için uygulanır |

**Eksik değer gösterimi:** boş hücre. `participant_id` alanı yapay zekâ ve
insanlaştırılmış metinlerde tanım gereği boştur; bu bir veri eksikliği değildir.

**Uzunluk bandı notu:** 100–120 kelime bandı proje metni gereği katılımcı
yanıtları ve yapay zekâ metinleri için geçerlidir. İnsanlaştırılmış
metinlerde bant şartı aranmaz, yalnızca çıktı uzunluğu kaydedilir.

**Üretici model bilgisi burada tutulmaz.** Model, insanlaştırma aracı ve kaynak
metin bağlantısı proje metni gereği ayrı bir tabloda (`ai_metadata.csv`)
saklanır.

---

## 2b. `data_raw/ai_metadata.csv` — yapay zekâ metadata tablosu (60 satır)

Proje metninin 12. bölümünde tanımlanan üçüncü tablodur.

| değişken | açıklama | tür | geçerli değerler |
|---|---|---|---|
| `text_id` | İlgili metin | metin | T001–T060 |
| `label` | Metnin sınıfı | kategorik | `ai`, `humanized` |
| `model_tool` | Metni üreten model veya araç | kategorik | `ChatGPT`, `Gemini`, `Claude`, `Kumru`, `Aithor`, `Rephraser` |
| `model_version` | Model/araç sürümü | metin | `kaydedilmedi` |
| `uretim_ayarlari` | Üretim ayarları | metin | sabit yönerge veya ücretsiz sürüm notu |
| `uretim_tarihi` | Üretim tarihi | metin | `kaydedilmedi` |
| `source_text_id` | İnsanlaştırmanın uygulandığı kaynak metin | metin | T001–T060, boş |

**Sürüm ve tarih alanları neden boş:** Bu alanlar üretim sırasında
kaydedilmemiştir ve geriye dönük olarak elde edilemez. Alanlar silinmemiş,
`kaydedilmedi` değeriyle açıkça işaretlenmiştir. Bu, çalışmanın
sınırlılıklarından biridir.

---

## 3. `data_raw/detector_scores.csv` — dedektör ölçüm tablosu (120 satır)

| değişken | açıklama | tür | geçerli değerler | üretim yöntemi |
|---|---|---|---|---|
| `text_id` | Ölçülen metin | metin | T001–T060 | `texts.csv` ile eşleşir |
| `detector_name` | Dedektör | kategorik | `GPTZero`, `ZeroGPT` | — |
| `detector_version` | Dedektör sürümü / arayüz bilgisi | metin | `Model 4.1m`, `web arayuz` | ölçüm anında ekrandan okunur |
| `scan_mode` | Tarama modu | metin | `Advanced`, `Detect Text` | ölçüm anında seçilen mod |
| `score` | Yapaylık skoru | ondalık | 0,000–1,000 | dedektörün verdiği yüzde, yüze bölünerek |
| `binary_label` | İkili karar | tam sayı | 0 = insan, 1 = yapay | `score >= threshold` |
| `threshold` | Karar eşiği | ondalık | 0,50 | sabit, tüm ölçümlerde aynı |
| `confidence` | Dedektörün yazılı güven ifadesi | metin | örn. `highly confident` | ekrandan okunur |
| `mixed_pct` | GPTZero'nun "Mixed" yüzdesi | ondalık | 0,00–0,95 / boş | üç sınıflı çıktı veren dedektörlerde |
| `kisa_metin_uyarisi` | Dedektörün kısa metin uyarısı verip vermediği | kategorik | `evet`, `hayir` | ekrandan okunur |
| `run_date` | Ölçüm tarihi | tarih | YYYY-AA-GG | ölçümün yapıldığı gün |

**Ölçüm kuralı:** Her metin bir kez üretilir, dosyaya kaydedilir ve tüm
dedektörlere aynı kayıt verilir. Aynı metnin farklı dedektörlere farklı
hâlleri verilmez.

**`score` yorumu:** Skor her zaman *yapay olma* yüzdesidir. GPTZero üç
sınıflı çıktı verdiğinde (AI / Mixed / Human) skor AI yüzdesi olarak
alınır, Mixed bilgisi `mixed_pct` alanında ayrıca saklanır.

---

## 4. `results/perplexity_scores.csv` — açık kaynak referans ölçümleri (180 satır)

| değişken | açıklama | tür | geçerli değerler |
|---|---|---|---|
| `text_id` | Ölçülen metin | metin | T001–T060 |
| `label`, `model`, `prompt_id`, `humanizer` | `texts.csv`'den taşınan alanlar | — | — |
| `dil_modeli` | Ölçümde kullanılan Türkçe dil modeli | metin | üç model adı |
| `birincil` | Ana sonuçların raporlandığı model mi | kategorik | `evet`, `hayir` |
| `perplexity` | Dil modeli altındaki perplexity değeri | ondalık | > 0, üst sınır yok |
| `token_sayisi` | Metnin token sayısı | tam sayı | — |
| `kirpildi` | Bağlam sınırı nedeniyle kırpma yapıldı mı | kategorik | `evet`, `hayir` |
| `esik` | Karar eşiği | ondalık | **boş** — kalibre edilmemiştir |
| `score` | 0–1 arası yapaylık skoru | ondalık | **boş** — eşik olmadan üretilemez |
| `binary_label` | İkili karar | tam sayı | **boş** — eşik olmadan üretilemez |

**Perplexity yorumu:** Düşük perplexity, metnin dil modeli için daha
öngörülebilir olduğunu gösterir. Analizlerde ticari dedektörlerle aynı
yönde karşılaştırma yapılabilmesi için yapaylık göstergesi olarak
`-perplexity` kullanılır.

**Eşik neden boş:** Karar eşiği insan yazımı metinlerin dağılımına göre
belirlenir. `human` sınıfı bulunmadığından eşik kalibre edilmemiştir.
Eşiğin değerlendirme verisinden türetilmesi veri sızıntısı oluşturur
(Usul ve Esaslar §8.3). Betikte kalibrasyon seçeneği hazır bırakılmıştır.

---


## 5. Kişisel veri ve gizlilik

Veri setinde kişisel veri bulunmamaktadır. Tüm metinler dil modelleri
tarafından üretilmiştir; gerçek kişilere ait yazı, ad, öğrenci numarası
veya kimlik göstergesi içermez. Etik onay sonrasında katılımcı metni
toplanması hâlinde kimlik tablosu ayrı ve yetkili erişimli tutulacak,
analiz dosyalarında yalnızca kodlanmış veri kullanılacaktır
(Usul ve Esaslar §4.1).
