# Dedektorler Arasi Uyum

Uretim tarihi: 2026-08-12

Metin: 60 | Karar ureten dedektor: 2 | Toplam dedektor: 5

## 1. Karar uyumu ve Cohen kappa

Ayni metne iki dedektorun ayni etiketi verip vermedigi.
Kappa, tesadufen beklenen uyusma cikarildiktan sonra kalan uyumu olcer.

| dedektor cifti | metin kumesi | n | ham uyum | kappa | yorum |
|---|---|---|---|---|---|
| GPTZero - ZeroGPT | tum metinler | 60 | 0.467 | -0.085 | tesadufun altinda |
| GPTZero - ZeroGPT | ham yapay | 20 | 0.450 | -0.100 | tesadufun altinda |
| GPTZero - ZeroGPT | insanlastirilmis | 40 | 0.475 | -0.066 | tesadufun altinda |

## 2. Karar farkinin anlamliligi (McNemar, tam binom)

Ham yapay metinlerde iki dedektorun yakalama farki test edilmistir.
Yalnizca uyusmayan ciftler bilgi tasir.

| dedektor cifti | n | yalniz birinci yakaladi | yalniz ikinci yakaladi | p |
|---|---|---|---|---|
| GPTZero - ZeroGPT | 20 | 10 | 1 | 0.0117 |

## 3. Yon uyumu: insanlastirma yapaylik skorunu dusurdu mu

Her eslestirilmis cift icin skorun yonu (dustu / degismedi / yukseldi)
kaydedilmis, dedektorler bu yon uzerinden karsilastirilmistir. Esik
gerektirmedigi icin perplexity yaklasimi da bu analize dahildir.

| dedektor | dustu | degismedi | yukseldi | n |
|---|---|---|---|---|
| GPTZero | 28 | 9 | 3 | 40 |
| ZeroGPT | 10 | 20 | 10 | 40 |
| Perplexity: turkish-gpt2 | 28 | 3 | 9 | 40 |
| Perplexity: turkish-gpt2-large | 30 | 3 | 7 | 40 |
| Perplexity: gpt2-turkish-cased | 23 | 3 | 14 | 40 |

Dedektor ciftleri arasinda yon uyumu:

| dedektor cifti | ayni yon | n | oran |
|---|---|---|---|
| GPTZero - ZeroGPT | 14 | 40 | 0.350 |
| GPTZero - Perplexity: turkish-gpt2 | 26 | 40 | 0.650 |
| GPTZero - Perplexity: turkish-gpt2-large | 25 | 40 | 0.625 |
| GPTZero - Perplexity: gpt2-turkish-cased | 22 | 40 | 0.550 |
| ZeroGPT - Perplexity: turkish-gpt2 | 15 | 40 | 0.375 |
| ZeroGPT - Perplexity: turkish-gpt2-large | 15 | 40 | 0.375 |
| ZeroGPT - Perplexity: gpt2-turkish-cased | 16 | 40 | 0.400 |
| Perplexity: turkish-gpt2 - Perplexity: turkish-gpt2-large | 34 | 40 | 0.850 |
| Perplexity: turkish-gpt2 - Perplexity: gpt2-turkish-cased | 33 | 40 | 0.825 |
| Perplexity: turkish-gpt2-large - Perplexity: gpt2-turkish-cased | 31 | 40 | 0.775 |

> Not: n=60 ve alt kumelerde n=20 ile calisildigindan kappa ve
> McNemar sonuclari genis belirsizlik tasir. Sonuclar egilim olarak
> yorumlanmali, kesin nokta tahmini olarak sunulmamalidir.
