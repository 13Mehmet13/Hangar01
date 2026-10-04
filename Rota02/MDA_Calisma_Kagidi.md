# MDA Çalışma Kâğıdı — Hafta 02

**BMU1421 · Dijital Oyun Tasarımı** — Mehmet Altıok · 23080410319

| Soru | Cevabım |
|---|---|
| **Oyunun adı ve bağlantısı** | **2048** (Gabriele Cirulli) — https://play2048.co/ (tarayıcıda, ücretsiz, kısa tur). Föydeki itch.io listesi Cloudflare doğrulaması yüzünden açılmadı, bu yüzden aynı türden kısa bir tarayıcı oyunu seçtim. Bir turda ~110 hamle oynadım: skor **504**, en yüksek karo **64**. |
| **Mekanik** — oyuncu hangi eylemleri yapabiliyor, kurallar ne? | Tek eylem var: dört yönden birine kaydırmak (ok tuşları). Kurallar: (1) tüm karolar seçilen yönde sonuna kadar kayar, (2) aynı değerli iki karo çarpışırsa toplanıp tek karo olur ve skor o kadar artar, (3) her hamleden sonra boş bir hücreye rastgele 2 (ya da nadiren 4) gelir, (4) tahta dolup hiçbir hamle birleşme yapamıyorsa oyun biter. Geri alma ve karıştırma gibi sınırlı yardımcılar da var. |
| **Dinamik** — oynarken hangi davranış ortaya çıktı? (kural kitabında yazmayan) | Kural kitabında olmayan **köşe stratejisi** kendiliğinden ortaya çıktı: en büyük karoyu bir köşede tutmak için sürekli aynı iki yönü (Sol–Aşağı) tekrarladım, üçüncü bir yönü (Sağ) yalnızca tahta kilitlenince "acil çıkış" olarak kullandım. Tahta sol-alta sıkışıp skor hiç artmayınca (ilk 25 hamlede skor 28'de takıldı) stratejimin kırılganlığını gördüm. Ayrıca küçük karoları büyüğün **yanında sıralı** (yılan düzeni) tutmaya başladım; bu oyunun hiçbir yerinde yazmıyor. |
| **Estetik** — hangi duyguyu yaşattı? Hangi iki eğlence türü? | Baskın duygu: "bir hamle daha" gerilimi ve tahta dolarken artan kaygı, sonra büyük bir birleşmenin (32+32→64) verdiği rahatlama. Eğlence türleri: **Meydan okuma** (tahtayı kilitlemeden en yüksek karoya ulaşma) ve **Gevşeme/kapılma** (basit, ritmik kaydırma hareketi; düşünmeden de oynanabilmesi). Küçük bir **keşif** tadı da var (hangi sıralama işe yarıyor?). |
| **Hangi tek mekaniği değiştirsen estetik de değişirdi?** | Her hamlede **rastgele karo gelmesi** kuralını kaldırıp karoların sadece birleşme olduğunda gelmesini sağlasam oyun şansa bağlı bir gerilim oyunundan **saf bir bulmacaya** dönüşürdü: tahta kendiliğinden dolmadığı için baskı ve kaygı kaybolur, yerine sakin bir planlama duygusu gelirdi (meydan okuma → gevşeme/zekâ oyunu). Tersine 4×4 yerine 3×3 tahta yapsam aynı kural çok daha stresli bir "hayatta kalma" oyununa dönüşürdü. |
| **Bartle'ın hangi tipini memnun ediyor, hangisini ihmal ediyor?** | **Başarıcı (Achiever)** tipini çok memnun ediyor: skor, en yüksek karo ve "en iyi skor" sayacı tek hedef. **Kaşif** tipini az ölçüde (düzen stratejileri keşfetmek). **Sosyalleşen** tipi tamamen ihmal ediliyor (rekabet, sohbet ya da iş birliği yok) ve **Öldürücü/Rakip** tipi için de doğrudan oyuncu karşılaştırması yok (yalnızca kendi rekorunla yarışıyorsun). |

## Gözlem özeti

Bir mekanik değişikliğinin estetiği nasıl değiştirdiğini 2048 üzerinde gördüm: şansa bağlı karo üretimi gerilimi yaratıyor, onu çıkarırsak oyun sakin bir bulmacaya dönüşüyor. Mekanik (kaydırma + birleştirme + rastgele karo) → Dinamik (köşe/yılan stratejisi, tıkanınca acil çıkış) → Estetik (meydan okuma + kapılma) zinciri bu oyunda çok net izlenebiliyor.

## Takım arkadaşıyla karşılaştırma

> _Buraya takım arkadaşının en az bir satırlık cevabıyla kendi cevabın arasındaki farkı yaz (föyün son maddesi)._
