# Devir Notu

**Proje:** AI Metin Tespiti — Türkçe metinlerde ticari yapay zekâ dedektörlerinin
yanlış pozitif ve kaçırma davranışının denetlenmesi (KARDEP)

**Devreden:** Harun Kayaaltı — stajyer öğrenci
**Devralan:** Dr. Öğr. Üyesi Çağrı Arısoy — proje yürütücüsü
**Tarih:** ____________

---

## 1. Çalışma nerede duruyor

| içerik | konum | erişim durumu |
|---|---|---|
| Kod, veri, sonuçlar, şekiller, kaynakça | Git deposu `harun-kayaalti/ai-metin-tespiti` | depo sahibi stajyerdir; devirde yürütücüye aktarılacaktır |
| LaTeX kaynak dosyaları | Overleaf projesi `Overleaf_Staj_Raporu` | proje sahibi stajyerdir; yürütücüye paylaşım bağlantısı verilecektir |
| Derlenmiş rapor | `reports/Staj_Raporu.pdf` | depoda |
| Günlük ve haftalık staj kayıtları | Google Drive staj klasörü | danışmanla paylaşımlı |
| Seçim gerekçesi belgeleri | Google Drive staj klasörü | danışmanla paylaşımlı |
| Etik başvuru belgeleri | Google Drive staj klasörü | danışmanla paylaşımlı |

Overleaf ve Drive erişimi stajyerin kişisel hesaplarına bağlıdır. Devir sırasında
her ikisinin de yürütücüye aktarılması veya bir kopyasının teslim edilmesi gerekir.

---

## 2. Gizlilik durumu

**Bu aşamada projede kişisel veri bulunmamaktadır.**

Veri setindeki 60 metnin tamamı dil modelleri tarafından üretilmiştir. İnsan
kaynaklı metin, katılımcı kaydı, kimlik bilgisi veya iletişim bilgisi yoktur.
Bu nedenle depo ve rapor kısıtsız paylaşılabilir; erişim sınırlaması gerektiren
bir dosya bulunmamaktadır.

### Katılımcı verisi toplandığında geçerli olacak kurallar

Yanlış pozitif ölçümü için insan yazımı metin toplanması etik kurul onayına
bağlıdır. Onay alındıktan sonra aşağıdaki kurallar uygulanır:

- Ham form indirmesi şifrelenmiş bir dizinde tutulur; **sürüm denetimine
  alınmaz ve paylaşılmaz.**
- Depoya yalnızca kimliksizleştirilmiş metinler girer.
- Katılımcılara kimlik bilgisi taşımayan kod verilir (K01, K02, ...);
  kod-kimlik eşleştirme tablosu tutulmaz.
- Erişim yetkisi proje yürütücüsü ve araştırmacıyla sınırlıdır.

Ayrıntılı kurallar `Veri_Toplama_Anonimlestirme_Saklama_Protokolu_v1.docx`
belgesinde tanımlıdır.

---

## 3. Kullanılan hesaplar ve araçlar

| araç | kullanım biçimi | devredilecek kimlik bilgisi |
|---|---|---|
| GPTZero | web arayüzü, hesapsız | yok |
| ZeroGPT | web arayüzü, hesapsız | yok |
| Aithor | ücretsiz sürüm | yok |
| Rephraser.co | ücretsiz sürüm | yok |
| Hugging Face | açık model indirme, hesapsız | yok |
| ChatGPT / Gemini / Claude / Kumru | metin üretimi, web arayüzü | yok |

**Devredilecek parola, API anahtarı veya ücretli abonelik bulunmamaktadır.**
Perplexity ölçümleri yerel bilgisayarda çalıştırılmıştır; bulut hizmeti
kullanılmamıştır.

---

## 4. Çalışmayı sürdürecek kişi için

### Kurulum

```bash
git clone https://github.com/harun-kayaalti/ai-metin-tespiti.git
cd ai-metin-tespiti
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Tüm sonuçları yeniden üretme

```bash
python src/build_data.py            # metin, metadata ve skor tablolarini uretir
python src/veri_kalite_kontrol.py   # veri seti denetimi (0 uyari beklenir)
python src/perplexity_baseline.py   # acik kaynak referans olcumleri
python src/metrikler.py             # FPR, recall, evasion etkisi, alt grup
python src/uyum.py                  # Cohen kappa, McNemar
python src/sekiller.py              # sekiller
```

Sıra değiştirilmemelidir. `perplexity_baseline.py` ilk çalıştırmada yaklaşık
4 GB model indirir.

### Veri ekleme

Yeni metin veya ölçüm eklenecekse `src/build_data.py` içindeki `METINLER` ve
`SKORLAR` listeleri güncellenir, betik yeniden çalıştırılır. `data_raw/`
altındaki dosyalar **elle düzenlenmez**; bunlar betiğin çıktısıdır.

### Etik onay geldikten sonra

İnsan metinleri toplandığında perplexity karar eşiği tek komutla kalibre edilir:

```bash
python src/perplexity_baseline.py --kalibrasyon insan_metinleri.csv
```

---

## 5. Devir sırasında yapılması gerekenler

1. Git deposunun sahipliği veya bir kopyası yürütücüye aktarılır.
2. Overleaf projesi yürütücüyle paylaşılır; ayrıca kaynak dosyaların ZIP
   yedeği teslim edilir.
3. Drive'daki staj klasörünün yürütücü erişimi kalıcı hâle getirilir.
4. `ISLER_LISTESI.md` dosyası birlikte okunur; devam edilecek işler üzerinde
   mutabık kalınır.
