# Metrik Sonuclari

Uretim tarihi: 2026-08-12

Metin: 60 | Dedektor: 5 | Toplam olcum: 300

Guven araliklari Wilson skor yontemiyle, %95 duzeyinde hesaplanmistir.

## 1. Ham yapay metinlerde yakalama orani

Yalnizca ticari dedektorler icin hesaplanabilir; perplexity
yaklasiminda karar esigi kalibre edilmemistir.

| dedektor | uretici model | yakalanan | n | oran | %95 GA |
|---|---|---|---|---|---|
| GPTZero | TUMU | 19 | 20 | 0.950 | [0.764, 0.991] |
| GPTZero | ChatGPT | 5 | 5 | 1.000 | [0.566, 1.000] |
| GPTZero | Claude | 5 | 5 | 1.000 | [0.566, 1.000] |
| GPTZero | Gemini | 5 | 5 | 1.000 | [0.566, 1.000] |
| GPTZero | Kumru | 4 | 5 | 0.800 | [0.376, 0.964] |
| ZeroGPT | TUMU | 10 | 20 | 0.500 | [0.299, 0.701] |
| ZeroGPT | ChatGPT | 4 | 5 | 0.800 | [0.376, 0.964] |
| ZeroGPT | Claude | 2 | 5 | 0.400 | [0.118, 0.769] |
| ZeroGPT | Gemini | 1 | 5 | 0.200 | [0.036, 0.624] |
| ZeroGPT | Kumru | 3 | 5 | 0.600 | [0.231, 0.882] |

## 2. Ayirt etme gucu (AUC)

Ham yapay metinler ile insanlastirilmis metinlerin ayrilabilirligi.
0,50 = hic ayirt edemiyor, 1,00 = kusursuz ayiriyor. Esik
gerektirmedigi icin ucuncu dedektor tipi de ayni olcute girer.

| dedektor | karsilastirma | n(ham) | n(insanlastirilmis) | AUC |
|---|---|---|---|---|
| GPTZero | TUMU | 20 | 40 | 0.746 |
| GPTZero | Aithor | 20 | 20 | 0.605 |
| GPTZero | Rephraser | 20 | 20 | 0.887 |
| ZeroGPT | TUMU | 20 | 40 | 0.522 |
| ZeroGPT | Aithor | 20 | 20 | 0.575 |
| ZeroGPT | Rephraser | 20 | 20 | 0.470 |
| Perplexity: turkish-gpt2 | TUMU | 20 | 40 | 0.622 |
| Perplexity: turkish-gpt2 | Aithor | 20 | 20 | 0.596 |
| Perplexity: turkish-gpt2 | Rephraser | 20 | 20 | 0.647 |
| Perplexity: turkish-gpt2-large | TUMU | 20 | 40 | 0.633 |
| Perplexity: turkish-gpt2-large | Aithor | 20 | 20 | 0.599 |
| Perplexity: turkish-gpt2-large | Rephraser | 20 | 20 | 0.667 |
| Perplexity: gpt2-turkish-cased | TUMU | 20 | 40 | 0.607 |
| Perplexity: gpt2-turkish-cased | Aithor | 20 | 20 | 0.604 |
| Perplexity: gpt2-turkish-cased | Rephraser | 20 | 20 | 0.610 |

> Not: Insanlastirilmis metinler ham metinlerden turetildiginden
> iki grup bagimsiz degildir. AUC burada mutlak bir siniflandirma
> performansi degil, esikten bagimsiz bir ayrilabilirlik olcusu
> olarak yorumlanmalidir.

## 3. Esik gecisi (kacirma)

Ham hali yapay olarak isaretlenmis metinlerin, insanlastirma
sonrasi kacinin insan tarafina gectigi.

| dedektor | arac | kacan | n | oran | %95 GA |
|---|---|---|---|---|---|
| GPTZero | Aithor | 3 | 19 | 0.158 | [0.055, 0.376] |
| GPTZero | Rephraser | 9 | 19 | 0.474 | [0.273, 0.683] |
| ZeroGPT | Aithor | 2 | 10 | 0.200 | [0.057, 0.510] |
| ZeroGPT | Rephraser | 2 | 10 | 0.200 | [0.057, 0.510] |

## 4. Insanlastirmanin etkisi (Wilcoxon isaretli sira testi)

Ayni prompt icin ham ve insanlastirilmis metin eslestirilmistir.
Fark = insanlastirilmis - ham (yapaylik skoru uzerinden).
Negatif ortalama fark, insanlastirmanin metni daha az yapay
gosterdigini isaret eder.

| dedektor | arac | n | ortalama fark | medyan fark | z | p | |
|---|---|---|---|---|---|---|---|
| GPTZero | Aithor | 11 | -0.117 | +0.000 | -1.82 | 0.0682 | a.d. |
| GPTZero | Rephraser | 20 | -0.422 | -0.340 | -3.90 | 0.0001 | *** |
| ZeroGPT | Aithor | 8 | -0.089 | +0.000 | -1.47 | 0.1415 | a.d. |
| ZeroGPT | Rephraser | 12 | +0.068 | +0.000 | -1.06 | 0.2896 | a.d. |
| Perplexity: turkish-gpt2 | Aithor | 17 | -4.318 | -2.580 | -2.70 | 0.0070 | ** |
| Perplexity: turkish-gpt2 | Rephraser | 20 | -6.963 | -5.913 | -2.59 | 0.0095 | ** |
| Perplexity: turkish-gpt2-large | Aithor | 17 | -2.913 | -1.884 | -3.12 | 0.0018 | ** |
| Perplexity: turkish-gpt2-large | Rephraser | 20 | -6.055 | -2.862 | -3.08 | 0.0021 | ** |
| Perplexity: gpt2-turkish-cased | Aithor | 17 | -11.132 | -2.885 | -2.27 | 0.0231 | * |
| Perplexity: gpt2-turkish-cased | Rephraser | 20 | -11.644 | -5.862 | -2.15 | 0.0318 | * |

Anlamlilik: *** p<0,001  ** p<0,01  * p<0,05  a.d. = anlamli degil

> Not: n=20 ile calisan testlerde guc dusuktur; anlamsiz sonuc
> etkinin yoklugunu degil, mevcut orneklemle gosterilemedigini
> ifade eder.
