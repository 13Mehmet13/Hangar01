# Hangar 01 — Nu.D36 Biplane

BMU1421 — Dijital Oyun Tasarımı (2026-2027 Güz)
Hafta 01 laboratuvar ödevi: Blender'da 1930'lardan bir çift kanatlı eğitim uçağını
(Nu.D36'dan esinlenerek) gerçek ölçekte modelleyip Unity'de pervanesini döndürmek.

## İçerik

| Dosya | Açıklama |
|---|---|
| `Assets/Models/Nu_D36.fbx` | Blender'da üretilen, Unity'ye aktarılan uçak modeli |
| `Assets/Scripts/PervaneDondur.cs` | Pervaneyi sürekli döndüren betik (`Pervane` nesnesine bağlı) |
| `Assets/Scripts/UcagiIlerlet.cs` | Uçağı ileri doğru hareket ettiren bonus betik (`Nu_D36` kök nesnesine bağlı) |
| `Assets/Materials/` | Gövde (kırmızı), kanat (krem), motor/pervane (gri), pilot (deri), atkı (sarı) malzemeleri |
| `Assets/Scenes/SampleScene.unity` | Modelin yerleştirilip test edildiği sahne |

Modelin kendisi `generate_nu_d36.py` adlı bir Blender Python betiği ile **kod üzerinden
üretildi**: gövde, çift kanat (staggerlı), kuyruk, iniş takımı, motor ve pervane gerçek
ölçülerinde (~6.4 m gövde, 9.74 m üst kanat açıklığı, ~2.44 m yükseklik) otomatik
oluşturulup renklendirildi, pervane hariç her şey `Nu_D36` adıyla birleştirildi ve doğru
FBX dışa aktarım ayarlarıyla (`-Z Forward`, `Y Up`, Apply Scale/Transform) kaydedildi.

## Bonus görevler

- ✅ **Pilot + atkı** — arka kokpitte basit bir pilot başı ve rüzgârda uçuşan atkı
- ✅ **Yıldız motor** — motorun önünde çember şeklinde 9 silindir
- ✅ **Uçağı ilerlet** — `UcagiIlerlet.cs`, `Nu_D36` üzerinde aktif

## Nasıl açılır

1. Unity Hub → **Unity 6.3 LTS (6000.3.25f1)** ile bu klasörü proje olarak aç.
2. `Assets/Scenes/SampleScene.unity` sahnesini aç (otomatik açılır).
3. Play'e bas: pervane döner, uçak ileri hareket eder.

## Ekran görüntüsü

`oyun_ekran_goruntusu.png` — Game görünümünden, pervane dönerken alınmış yakın çekim.

---
Dr. Öğr. Üyesi Davut ARI — [davut.tech/courses/2026-2027/fall/BMU1421](https://davut.tech/courses/2026-2027/fall/BMU1421)
