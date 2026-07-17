# AI Metin Tespiti — KARDEP Staj Projesi

## 1. Projenin kısa amacı

Bu çalışma, ticari yapay zekâ metin dedektörlerinin **Türkçe metinlerdeki güvenilirliğini denetlemektedir**. Yeni bir dedektör geliştirilmemekte; mevcut araçların iki hata türü ölçülmektedir:

- **Yanlış pozitif:** İnsanın yazdığı metnin yapay zekâ üretimi sanılması (ana metrik)
- **Kaçırma / evasion:** Yapay zekâ üretimi metnin, özellikle insanlaştırma araçlarından geçtikten sonra yakalanamaması

Depo, projenin stajyer görev alanını kapsar: veri protokolü, özellik çıkarımı ve temel (baseline) model.

## 2. Klasör ve dosyaların açıklaması

| Klasör | İçerik |
|---|---|
| `data_raw/` | Kaynağından alındığı hâliyle ham veri. **Değiştirilmez, üzerine yazılmaz.** Sürüm takibi dışındadır. |
| `data_interim/` | Temizleme ve ara işlem çıktıları. Sürüm takibi dışındadır. |
| `data_processed/` | Analiz için hazır veri dosyaları. Sürüm takibi dışındadır. |
| `notebooks/` | Keşif ve açıklamalı deney defterleri (Jupyter). |
| `src/` | Tekrar kullanılabilir Python fonksiyonları ve betikleri. |
| `results/` | Tablo ve metrik çıktıları. |
| `figures/` | Grafik çıktıları. |
| `reports/` | LaTeX kaynakları, PDF ve raporlar. |
| `references/` | Literatür matrisi, makale özetleri ve BibTeX dosyası. |

Klasör düzeni Staj Çalışma Usul ve Esasları Bölüm 5.2'deki standarda uygundur.

## 3. Kurulum ve gerekli paketler

*(3. haftada kod yazımı başladığında doldurulacak.)*

```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

## 4. Veriye erişim ve gizlilik notu

- **Gerçek katılımcı verisi etik kurul onayı tamamlanmadan toplanmaz.** (KARDEP Bölüm 14; Usul-Esaslar Bölüm 13.3)
- Ham veri klasörleri (`data_raw/`, `data_interim/`, `data_processed/`) `.gitignore` ile sürüm takibi dışında tutulur ve **depoya yüklenmez** — depo private olsa dahi (Usul-Esaslar Bölüm 6.2).
- Metinlerden ad, öğrenci numarası ve kimlik göstergeleri temizlenir.
- Kişisel veri, erişim anahtarı ve yayımlanmamış proje dosyaları kamuya açık yapay zekâ araçlarına yüklenmez (Usul-Esaslar Bölüm 4.1).

## 5. Kodların çalıştırılma sırası

*(3. haftada kod yazımı başladığında doldurulacak.)*

Planlanan akış:
1. Yapay zekâ metinlerinin üretimi (5 sabit prompt × 2–3 model)
2. Humanizer aracından geçirme → humanized sınıfı
3. Temizleme ve özellik çıkarımı (`word_count`, `char_count`, `length_band`)
4. Dedektörlerden geçirme ve skor tablosunun oluşturulması
5. Metrik hesaplama (FPR, recall, evasion etkisi)

## 6. Üretilen çıktılar ve konumları

| Çıktı | Konum | Durum |
|---|---|---|
| Literatür matrisi | `references/Literatur_Matrisi.xlsx` | M01–M06 dolu |
| Makale özetleri | `references/*_ozet.md` | 6 makale |
| Kaynakça | `references/references.bib` | 6 kayıt |
| Veri sözlüğü | `references/` | 2. haftada |
| Analiz kodları | `src/`, `notebooks/` | 3. haftadan itibaren |
| Şekil ve tablolar | `figures/`, `results/` | 4. haftadan itibaren |

## 7. Bilinen sorunlar ve tamamlanmayan işler

- Etik kurul süreci devam ettiği için `human` sınıfı verisi henüz mevcut değil. Analiz boru hattı, veri geldiğinde çalışacak şekilde kurulmaktadır.
- Kullanılacak dil modelleri, humanizer aracı ve ticari dedektörler danışman kararıyla kesinleşecektir (KARDEP Bölüm 11 listeyi erişilebilirliğe göre açık bırakmıştır).
- "Temel model" ile kastedilenin açık kaynak/perplexity tabanlı baseline olduğu danışmanla teyit edilecektir.

## 8. Sorumlu kişi ve güncelleme tarihi

**Stajyer:** *(Harun Kayaaltı)*
**Danışman:** Dr. Öğr. Üyesi Çağrı Arısoy
**Son güncelleme:** *(2026-07-17)*
