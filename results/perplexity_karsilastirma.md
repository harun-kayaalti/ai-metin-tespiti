# Perplexity Referans Yaklasimi - Sonuclar

Uretim tarihi: 2026-08-11

Perplexity, metnin dil modeli tarafindan ne kadar ongorulebilir
oldugunu gosterir. Dusuk deger daha ongorulebilir metni isaret eder.

Birincil olcum modeli: `ytu-ce-cosmos/turkish-gpt2`. Diger modeller
sonuclarin olcum modeli secimine duyarliligini sinamak icindir.

## 0. Degerlendirilip elenen aday modeller

| model | eleme turu | gerekce |
|---|---|---|
| `cenkersisman/gpt2-turkish-128-token` | beyan edilmis eleme | Model karti egitim baglam penceresini 128 token olarak bildirmektedir; calisma metinleri bu modelin sozcuk parcalayicisiyla 294-376 token uzunlugundadir (ortalama 331). Model, hic egitilmedigi uzunlukta calistirilmis olur. Ayrica ayni metinleri diger adaylardan iki kattan fazla parcaya bolmektedir (331'e karsi ~144 token); perplexity token basina hesaplandigindan degerler diger modellerle karsilastirilamaz. Bu iki gerekceyle elenmistir. |

Eleme gerekceleri sonuclardan bagimsizdir; model kartindaki
beyana ve olculen token sayilarina dayanir. Elenen adaylar
kayittan silinmemis, gerekceleriyle birlikte belgelenmistir.

## 1. Sinif bazinda perplexity

| dil modeli | sinif | metin | ortalama | medyan | en dusuk | en yuksek |
|---|---|---|---|---|---|---|
| gpt2-turkish-cased | ai | 20 | 68.3 | 66.1 | 23.6 | 123.4 |
| gpt2-turkish-cased | humanized | 40 | 79.7 | 82.2 | 24.4 | 149.0 |
| turkish-gpt2 | ai | 20 | 28.2 | 26.6 | 12.6 | 51.3 |
| turkish-gpt2 | humanized | 40 | 33.9 | 34.4 | 13.1 | 71.6 |
| turkish-gpt2-large | ai | 20 | 19.0 | 17.9 | 8.5 | 31.6 |
| turkish-gpt2-large | humanized | 40 | 23.5 | 22.4 | 9.4 | 62.4 |

## 2. Insanlastirma perplexity'yi degistiriyor mu

Ayni promptun ham ve insanlastirilmis hali eslestirilerek
karsilastirilmistir. Pozitif fark, insanlastirmanin metni dil
modeli icin daha ongorulemez hale getirdigini gosterir.

| dil modeli | arac | eslesme | ortalama fark | artan | azalan |
|---|---|---|---|---|---|
| gpt2-turkish-cased | Aithor | 20 | +11.1 | 11 | 6 |
| gpt2-turkish-cased | Rephraser | 20 | +11.6 | 12 | 8 |
| turkish-gpt2 | Aithor | 20 | +4.3 | 12 | 5 |
| turkish-gpt2 | Rephraser | 20 | +7.0 | 16 | 4 |
| turkish-gpt2-large | Aithor | 20 | +2.9 | 15 | 2 |
| turkish-gpt2-large | Rephraser | 20 | +6.1 | 15 | 5 |

## 3. Uretici model bazinda ham metin perplexity

| dil modeli | uretici model | ortalama | medyan |
|---|---|---|---|
| gpt2-turkish-cased | ChatGPT | 47.1 | 48.6 |
| gpt2-turkish-cased | Claude | 92.1 | 103.7 |
| gpt2-turkish-cased | Gemini | 79.8 | 81.7 |
| gpt2-turkish-cased | Kumru | 54.1 | 61.5 |
| turkish-gpt2 | ChatGPT | 21.3 | 22.7 |
| turkish-gpt2 | Claude | 36.1 | 37.8 |
| turkish-gpt2 | Gemini | 34.1 | 34.7 |
| turkish-gpt2 | Kumru | 21.5 | 23.6 |
| turkish-gpt2-large | ChatGPT | 15.6 | 17.2 |
| turkish-gpt2-large | Claude | 22.7 | 25.2 |
| turkish-gpt2-large | Gemini | 24.2 | 24.0 |
| turkish-gpt2-large | Kumru | 13.7 | 13.5 |

> Uyari: Turkce icin egitilmis bir uretici modelin ciktilari, olcum
> icin kullanilan Turkce dil modeliyle benzer derlemelerden beslenmis
> olabilir. Bu durumda dusuk perplexity metnin yapay olmasindan degil,
> ayni dil dagilimini paylasmasindan kaynaklanabilir.

> Yapisal sinirlilik: Uretici modeller kapali API oldugundan kendi
> olasilik degerlerine erisilemez. Olcum, uretici modellerden cok daha
> kucuk acik modellerle yapilmaktadir; baseline'in mutlak performansi
> bu kosulun tavanidir.

## 4. Esik duyarlilik analizi

Esik kalibre edilmedigi icin, farkli esik degerlerinde kac metnin
esigin altinda kalacagi bilgi amacli verilmistir. Bu bir tespit
performansi degildir; insan sinifi bulunmadigindan duyarlilik ve
yanlis pozitif orani hesaplanamaz.

| dil modeli | esik 20 | esik 30 | esik 40 | esik 50 | esik 60 | esik 80 | esik 100 |
|---|---|---|---|---|---|---|---|
| gpt2-turkish-cased | 0% | 5% | 13% | 28% | 32% | 55% | 73% |
| turkish-gpt2 | 20% | 47% | 78% | 92% | 95% | 100% | 100% |
| turkish-gpt2-large | 48% | 83% | 97% | 98% | 98% | 100% | 100% |
