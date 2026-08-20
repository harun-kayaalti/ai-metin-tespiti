# Veri Kalite Kontrol Raporu

Uretim tarihi: 2026-08-20

Bu rapor `veri_kalite_kontrol.py` tarafindan otomatik uretilmistir. 
Betik hicbir kaydi silmez veya degistirmez; yalnizca veri setinin 
beklenen yapiya uygunlugunu denetler.

## 1. Tam sayim

| kontrol | sonuc | ayrinti |
|---|---|---|
| Toplam metin sayisi | GECTI | 60 / beklenen 60 |
| Toplam olcum sayisi | GECTI | 120 / beklenen 120 |
| Yinelenen text_id yok | GECTI | 0 yinelenen kayit |
| Tasarim hucreleri eksiksiz | GECTI | 60 hucrenin tamami dolu |
| Her metin tum dedektorlerden gecti | GECTI | her metin 2 dedektorden olculdu |
| Metni olmayan skor kaydi yok | GECTI | yok |

## 2. Uzunluk bandi (yalnizca yapay zeka metinleri)

| kontrol | sonuc | ayrinti |
|---|---|---|
| Ham metinler 100-120 kelime bandinda | GECTI | kelime araligi 101-119 |

Model bazinda ham metin uzunlugu (kelime):

| model | en kisa | ortalama | en uzun |
|---|---|---|---|
| ChatGPT | 111 | 112.4 | 113 |
| Gemini | 111 | 112.8 | 115 |
| Claude | 113 | 114.0 | 115 |
| Kumru | 101 | 107.8 | 119 |

Not: Uzunluk bandi proje metni geregi yalnizca yapay zeka metinleri icin 
gecerlidir. Insanlastirilmis metinlerde bant sarti aranmaz, yalnizca 
cikti uzunlugu kaydedilir.

## 3. Yapay zeka metadata tablosu

Metadata kaydi: 60 satir.

| alan | durum |
|---|---|
| model_tool | dolu |
| model_version | kaydedilmedi (uretim sirasinda alinmamistir) |
| uretim_ayarlari | dolu |
| uretim_tarihi | kaydedilmedi |
| source_text_id | insanlastirilmis kayitlarda dolu |

Tum insanlastirilmis kayitlarda kaynak metin baglantisi mevcuttur.

## 4. Taban ve tavan etkisi

Ham metnin skoru 0 ise kacirma etkisi olculemez (taban etkisi); 
skoru 1 ise insanlastirmanin skoru artirma payi yoktur (tavan etkisi).

| dedektor | taban (skor=0) | tavan (skor=1) | 20 ham metin uzerinden |
|---|---|---|---|
| GPTZero | 0 | 6 | 20 |
| ZeroGPT | 4 | 6 | 20 |

Taban etkisi gozlenen hucreler: ChatGPT/P2/ZeroGPT, Gemini/P2/ZeroGPT, Claude/P2/ZeroGPT, Kumru/P2/ZeroGPT

Bu hucrelerde 8 kacirma olcumu 'OLCULEMEZ' olarak isaretlenmistir.

## 5. Skor gecerliligi

| kontrol | sonuc | ayrinti |
|---|---|---|
| Skorlar 0-1 araliginda | GECTI | min 0.0, max 1.0 |
| binary_label esikle (0.5) tutarli | GECTI | tum kayitlar tutarli |
| Eksik skor yok | GECTI | 0 bos deger |

Dedektor surum ve tarama modu kaydi:

| dedektor | surum | tarama modu | olcum |
|---|---|---|---|
| GPTZero | Model 4.1m | Advanced | 60 |
| ZeroGPT | web arayuz | Detect Text | 60 |

## 6. Sonuc

Tum kontroller gecti. Veri seti analiz asamasi icin kapatilmistir.

Metin: 60 | Olcum: 120 | Model: 4 | Prompt: 5 | Insanlastirma araci: 2 | Dedektor: 2