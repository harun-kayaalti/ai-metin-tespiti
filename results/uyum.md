# Dedektorler Arasi Uyum

Uretim tarihi: 2026-08-20

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


> Not: n=60 ve alt kumelerde n=20 ile calisildigindan kappa ve
> McNemar sonuclari genis belirsizlik tasir. Sonuclar egilim olarak
> yorumlanmali, kesin nokta tahmini olarak sunulmamalidir.
