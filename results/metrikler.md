# KARDEP Bolum 13 -- Metrikler

Metin: 60 | Olcum: 120 | Dedektor: 2

Bu dosya yalnizca proje metninin 13. bolumunde tanimlanan metrikleri icerir.


## 1. Yanlis pozitif orani (FPR)

Projenin ana metrigidir. Insan yazimi metin sinifi bu asamada olusturulamadigindan hesaplanamamistir. Katilimci metinleri etik kurul onayina baglidir.


## 2. Recall / yakalama orani -- ham yapay zeka metinleri

Ham yapay zeka metinlerinin dedektorler tarafindan yakalanma orani.

| Dedektor | Yakalanan | n | Recall | Wilson %95 |
|---|---|---|---|---|
| GPTZero | 19 | 20 | 0,950 | [0,764 ; 0,991] |
| ZeroGPT | 10 | 20 | 0,500 | [0,299 ; 0,701] |

### Uretici model bazinda

| Dedektor | Model | Yakalanan | n | Recall | Wilson %95 |
|---|---|---|---|---|---|
| GPTZero | ChatGPT | 5 | 5 | 1,000 | [0,566 ; 1,000] |
| GPTZero | Claude | 5 | 5 | 1,000 | [0,566 ; 1,000] |
| GPTZero | Gemini | 5 | 5 | 1,000 | [0,566 ; 1,000] |
| GPTZero | Kumru | 4 | 5 | 0,800 | [0,376 ; 0,964] |
| ZeroGPT | ChatGPT | 4 | 5 | 0,800 | [0,376 ; 0,964] |
| ZeroGPT | Claude | 2 | 5 | 0,400 | [0,118 ; 0,769] |
| ZeroGPT | Gemini | 1 | 5 | 0,200 | [0,036 ; 0,624] |
| ZeroGPT | Kumru | 3 | 5 | 0,600 | [0,231 ; 0,882] |

## 3. Recall / yakalama orani -- insanlastirilmis metinler

| Dedektor | Insanlastirma araci | Yakalanan | n | Recall | Wilson %95 |
|---|---|---|---|---|---|
| GPTZero | Aithor | 16 | 20 | 0,800 | [0,584 ; 0,919] |
| GPTZero | Rephraser | 10 | 20 | 0,500 | [0,299 ; 0,701] |
| ZeroGPT | Aithor | 8 | 20 | 0,400 | [0,219 ; 0,613] |
| ZeroGPT | Rephraser | 13 | 20 | 0,650 | [0,433 ; 0,819] |

## 4. Evasion etkisi

KARDEP tanimi: ham yapay zeka recall degeri ile humanized recall degeri arasindaki dusus.

`Evasion etkisi = Recall(ham) - Recall(insanlastirilmis)`

Pozitif deger dususu, negatif deger insanlastirmanin metni daha yakalanabilir hale getirdigini gosterir.

| Dedektor | Insanlastirma araci | Recall(ham) | Recall(ins.) | Evasion etkisi |
|---|---|---|---|---|
| GPTZero | Aithor | 0,950 | 0,800 | +0,150 |
| GPTZero | Rephraser | 0,950 | 0,500 | +0,450 |
| ZeroGPT | Aithor | 0,500 | 0,400 | +0,100 |
| ZeroGPT | Rephraser | 0,500 | 0,650 | -0,150 |

### Insanlastirma araci ayrimi yapilmadan

| Dedektor | Recall(ham) | Recall(ins.) | Evasion etkisi |
|---|---|---|---|
| GPTZero | 0,950 | 0,650 | +0,300 |
| ZeroGPT | 0,500 | 0,525 | -0,025 |

## 5. Alt grup analizi -- metin uzunlugu

Tum metinlerin kelime sayisi medyani: 112,5 kelime.

Ham yapay zeka metinleri tasarim geregi 100-120 kelime bandindadir; bant ici / bant disi ayrimi bu sinif icin islevsizdir. Bu nedenle kirilim medyan bolmesiyle yapilmistir.

| Dedektor | Sinif | Uzunluk | Yakalanan | n | Recall | Wilson %95 |
|---|---|---|---|---|---|---|
| GPTZero | ham | medyan alti | 8 | 9 | 0,889 | [0,565 ; 0,980] |
| GPTZero | ham | medyan ustu | 11 | 11 | 1,000 | [0,741 ; 1,000] |
| GPTZero | insanlastirilmis | medyan alti | 13 | 21 | 0,619 | [0,409 ; 0,792] |
| GPTZero | insanlastirilmis | medyan ustu | 13 | 19 | 0,684 | [0,460 ; 0,846] |
| ZeroGPT | ham | medyan alti | 4 | 9 | 0,444 | [0,189 ; 0,733] |
| ZeroGPT | ham | medyan ustu | 6 | 11 | 0,545 | [0,280 ; 0,787] |
| ZeroGPT | insanlastirilmis | medyan alti | 11 | 21 | 0,524 | [0,324 ; 0,717] |
| ZeroGPT | insanlastirilmis | medyan ustu | 10 | 19 | 0,526 | [0,317 ; 0,727] |

## 6. Bu asamada hesaplanamayan Bolum 13 metrikleri

| Metrik | Gerekce |
|---|---|
| Yanlis pozitif orani (FPR) | Insan yazimi metin sinifi yok. |
| Karma-etkili lojistik regresyon | Katilimci duzeyinde kumelenme gerektirir; katilimci verisi yok. |
| Sirali egilim analizi | Egitim seviyesi / unvan degiskeni katilimci verisiyle gelir. |
| Alt grup: fakulte, yazma sikligi | Katilimci verisiyle gelir. |
