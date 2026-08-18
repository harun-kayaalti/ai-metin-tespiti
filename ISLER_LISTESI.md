# Tamamlanan, Tamamlanamayan ve Devam Edilmesi Gereken İşler

**Proje:** AI Metin Tespiti (KARDEP) · **Stajyer:** Harun Kayaaltı
**Son güncelleme:** ____________

---

## 1. Tamamlanan işler

### Veri toplama

- Beş sabit prompt belirlendi; tür bakımından farklılaşacak biçimde seçildi.
- Dört üretici modelden (ChatGPT, Gemini, Claude, Kumru) 20 ham yapay metin
  üretildi. Tamamı 100–120 kelime bandındadır.
- İki insanlaştırma aracından (Aithor, Rephraser.co) 40 metin türetildi.
- Toplam 60 metin, iki ticari dedektörle ölçüldü (120 ölçüm).
- Üç Türkçe dil modeliyle perplexity ölçümü yapıldı (180 ölçüm).
- **Toplam 300 ölçüm.**

### Veri düzeni ve denetim

- Tüm veri dosyaları tek bir üretim betiğinden (`build_data.py`) oluşturulmakta,
  elle düzenlenmemektedir.
- Otomatik kalite denetimi yazıldı; tasarım hücreleri, ölçüm eksiği, uzunluk
  bandı, skor aralığı ve eşik tutarlılığı sınanmaktadır. **0 uyarı ile geçmiştir.**
- Her değişkenin tanımı, türü ve üretim yöntemi veri sözlüğünde belgelenmiştir.
- Uzunluk bandını aşan bir çıktı kırpılmadan yeniden üretilmiş, elenen kayıt
  gerekçesiyle kaydedilmiştir.

### Analiz

- Yakalama oranları ve Wilson %95 güven aralıkları
- Eşik geçişi (kaçırma) oranları, araç–dedektör çifti bazında
- Ayrılabilirlik (AUC), üç dedektör tipi için ortak ölçütle
- Eşleştirilmiş Wilcoxon işaretli sıra testi, Benjamini–Hochberg düzeltmesiyle
- Cohen κ, McNemar tam binom testi, yön uyumu analizi
- Beş sonuç şekli (300 dpi)
- Analizler dış istatistik kütüphanesi kullanılmadan yazıldı; betikler depoda.

### Belgeler

- Model, insanlaştırma aracı, dedektör ve baseline dil modeli için dört ayrı
  seçim gerekçesi belgesi
- README, veri sözlüğü, requirements, Git deposu
- 23 sayfalık LaTeX staj raporu, 26 kaynaklı kaynakça
- Katılımcı bilgilendirilmiş gönüllü olur formu
- Veri toplama, anonimleştirme ve saklama protokolü
- Devir notu ve bu liste

---

## 2. Tamamlanamayan işler

| iş | gerekçe |
|---|---|
| **Yanlış pozitif oranının ölçülmesi** | İnsan yazımı metin sınıfı gerçek katılımcı verisi gerektirmektedir. Etik kurul süreci staj dönemi içinde sonuçlanmamıştır. Çalışmanın en önemli sınırlılığıdır. |
| **Perplexity karar eşiğinin kalibre edilmesi** | Eşik, insan metinlerinin dağılımından türetilir. İnsan sınıfı bulunmadığından kalibrasyon yapılamamıştır; eşiğin değerlendirme verisinden türetilmesi veri sızıntısı oluştururdu. |
| **Etik kurul başvuru formlarının doldurulması** | Form 1, 3, 4 ve 5 danışmanın unvan, bölüm ve iletişim bilgisi ile proje numarasını gerektirmektedir. Bu bilgiler alınamamıştır. Form 2 ve veri protokolü tamamlanmıştır. |
| **Üçüncü ticari dedektörün eklenmesi** | Copyleaks'in Türkçe desteği bulunduğu, veri toplama tamamlandıktan sonra tespit edilmiştir. Yeniden ölçüm için süre kalmamıştır. |
| **Ölçüm tekrarlanabilirliğinin sınanması** | Her metin bir kez ölçülmüştür. Ticari araçların kararlılığı sınanamamıştır. |
| **Final sunumu** | Staj takvimine göre 29. güne planlanmıştır. |

---

## 3. Devam edilmesi gereken işler

Öncelik sırasına göre:

1. **Yanlış pozitif ölçümü.** Etik onay alındıktan sonra insan yazımı metinler
   toplanmalı, iki ticari dedektör ve açık kaynak referanstan geçirilmeli,
   yanlış pozitif oranı Wilson güven aralığıyla raporlanmalıdır. Aynı veriyle
   perplexity karar eşiği kalibre edilmelidir.
   *Altyapı hazırdır; kalibrasyon tek komutla yapılmaktadır.*

2. **Metin sınıflarının tamamlanması.** Proje notlarında dört sınıf öngörülmektedir:
   insan (öğrenci), insan (akademisyen), yapay zekâ ve insanlaştırılmış. Şu anda
   ilk iki sınıf boştur.

3. **Dil kontrolü.** Aynı beş prompt İngilizceye çevrilerek aynı ölçüm hattından
   geçirilmeli; bulguların Türkçeye özgü olup olmadığı doğrudan sınanmalıdır.
   Şu anda literatürle karşılaştırma dolaylı yapılmaktadır.

4. **Üçüncü ticari dedektör.** Türkçe desteği belgelenmiş bir çok dilli ticari
   dedektör (Copyleaks) eklenerek dedektörler arası uyum analizi
   güçlendirilmelidir. İki araçla hesaplanan κ değeri üçüncü bir araçla
   doğrulanmalıdır.

5. **Prompt düzeyinde kaçınma.** Metin üretildikten sonra araçla dönüştürmek ile
   üretim aşamasında modele kaçınma talimatı vermek karşılaştırılmalıdır.

6. **Ölçüm tekrarlanabilirliği.** Metinlerin bir alt kümesi farklı zamanlarda
   yeniden ölçülerek ticari dedektörlerin kararlılığı değerlendirilmelidir.

7. **Yöntemin güçlü varyantı.** Bozulma tabanlı sıfır-atışlı yaklaşım veya
   düşük olasılıklı simgeleri öne çıkaran belirsizlik tabanlı ölçütler
   uygulanmalıdır. Şu anda ham perplexity kullanılmaktadır.

---

## 4. Devam edecek kişinin bilmesi gerekenler

- **Ticari araçlar zamanla değişir.** Dedektör sürümleri ve ölçüm tarihleri
  kaydedilmiştir; ileride tekrarlanan ölçümler farklı sonuç verebilir. Yeni
  ölçüm yapılacaksa sürüm bilgisi yeniden kaydedilmelidir.
- **Ölçüm modeli üretici modellerden biri olamaz.** Aksi hâlde model kendi
  çıktısını düşük perplexity ile ödüllendirir. Bu nedenle Kumru ölçüm modeli
  olarak kullanılmamıştır.
- **Perplexity değerleri modeller arasında karşılaştırılamaz.** Aynı metinlerin
  ortalaması kullanılan dil modeline göre 19,0 ile 68,3 arasında değişmektedir;
  yalnızca aynı model içindeki karşılaştırmalar geçerlidir.
- **Bir aday dil modeli elenmiştir.** Gerekçesi
  `results/perplexity_model_bilgisi.txt` içinde saklıdır; sonuçlardan bağımsız
  bir ölçüte dayanmaktadır.
