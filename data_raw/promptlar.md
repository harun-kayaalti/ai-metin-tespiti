# Sabit Prompt Kümesi ve Yönergeler

Bu dosya, çalışmada kullanılan beş sabit promptun tam metnini ve metin
üretiminde verilen sabit yönergeleri içerir. Promptlar proje metninde
tanımlanmıştır ve çalışma boyunca değiştirilmemiştir.

`data_raw/texts.csv` içindeki `prompt_id` alanı bu dosyadaki numaralara karşılık
gelir.

---

## Beş sabit prompt

| # | tür | prompt metni |
|---|---|---|
| 1 | temel bilgi | Türkiye Cumhuriyeti hakkında temel bilgileri kendi cümlelerinizle yazınız. Cevabınızda başkent, yönetim biçimi ve cumhuriyet kavramına yer veriniz. |
| 2 | bilimsel açıklama | Maddenin temel hâllerini kendi cümlelerinizle açıklayınız. Her hâl için günlük yaşamdan en az bir örnek veriniz ve bu hâllerin birbirinden nasıl farklılaştığını kısaca belirtiniz. |
| 3 | görüş / tartışma | Teknolojinin eğitim üzerindeki olumlu ve olumsuz etkilerini kendi düşüncelerinizle tartışınız. |
| 4 | süreç anlatımı | Bir öğrencinin sınava etkili şekilde hazırlanması için izlemesi gereken adımları sırasıyla açıklayınız. |
| 5 | karşılaştırma | Yüz yüze eğitim ile uzaktan eğitimi avantaj ve dezavantajları açısından karşılaştırınız. |

---

## Yapay zekâ metinleri için sabit yönerge

Dört üretici modelin (ChatGPT, Gemini, Claude, Kumru) tamamına aynı yönerge
verilmiştir. `[SORU]` yerine yukarıdaki promptlar sırayla yerleştirilmiştir.

```
Aşağıdaki soruyu kendi cümlelerinle yanıtla. Yanıtın yaklaşık
100-120 kelime olsun. Madde işareti veya başlık kullanma,
düz paragraf olarak yaz.

Soru: [SORU]
```

### Üretim koşulları

- Her prompt için yeni ve boş bir sohbet açılmıştır. Aynı sohbette arka arkaya
  sorulması hâlinde model kendi önceki yanıtını bağlam olarak görecek ve
  bağımsızlık bozulacaktır.
- Yönerge hiçbir modelde değiştirilmemiştir.
- Her yanıt için model adı, ölçüm tarihi ve kelime sayısı kaydedilmiştir.
- Uzunluk bandı dışında kalan çıktı kırpılmamış veya düzeltilmemiş; aynı
  promptla yeniden üretilmiş, elenen kayıt gerekçesiyle belgelenmiştir.

---

## İnsan yazımı metinler için yönerge

Katılımcılara aynı beş soru çevrim içi form üzerinden yöneltilmektedir. Soru
metinleri birebir aynıdır; yalnızca uzunluk yönergesi farklıdır.

```
Yalnızca size bildirilen soru numaralarını yanıtlayınız.

Her yanıt için:
• En az 8 cümle yazınız
• Kendi cümlelerinizle yazınız, internetten kopyalamayınız
• Araştırma yapmanıza gerek yok, bildiğiniz kadarını yazın
• Yapay zekâ aracı kullanmayınız
```

**Uzunluk yönergesindeki farkın gerekçesi.** Modele kelime sayısı verilebilir;
katılımcıya kelime saydırmak yazımın doğallığını bozmakta ve metni yapay hâle
getirmektedir. Bu nedenle katılımcıya cümle sayısı ölçütü verilmiş, kelime
sayısı sonradan araştırmacı tarafından hesaplanmıştır. Bant dışında kalan
katılımcı yanıtları veri setinden çıkarılmaz; gerçek kelime sayısı kaydedilir
ve uzunluğun etkisi analizde ayrıca değerlendirilir.

---

## Prompt kümesinin kapsamı

Beş prompt tür bakımından farklılaşacak biçimde seçilmiştir: temel bilgi,
bilimsel açıklama, görüş bildirme, süreç anlatımı ve karşılaştırma. Yaratıcı
yazı, teknik metin ve kişisel anlatı türleri kapsam dışındadır; bulguların
genellenebilirliği bu tür sınırıyla birlikte yorumlanmalıdır.
