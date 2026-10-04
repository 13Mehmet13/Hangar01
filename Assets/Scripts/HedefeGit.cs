using UnityEngine;

// Uçağı hedefe doğru döndürür ve sabit hızla ilerletir.
public class HedefeGit : MonoBehaviour
{
    [SerializeField] private Transform hedef;
    [SerializeField] private float hiz = 14f;          // metre / saniye
    [SerializeField] private float donusHizi = 60f;    // derece / saniye
    [SerializeField] private float varisMesafesi = 8f;

    private void Update()
    {
        if (hedef == null) return;

        // 1) Çıkarma: hedefe giden vektör
        Vector3 fark = hedef.position - transform.position;

        // 2) Uzunluk: hedefe olan uzaklık
        float mesafe = fark.magnitude;
        if (mesafe < varisMesafesi) return;

        // 3) Normalize: yalnızca yön kalsın
        Vector3 yon = fark.normalized;

        // 6) Dış çarpımın yukarı bileşeni: pozitifse hedef sağda
        float yan = Vector3.Cross(transform.forward, yon).y;

        // 4) Burnu hedefe çevir (kuaterniyonla yumuşak dönüş).
        // Kanat yatışı Rotate ile her karede eklenirse birikip takla attırır;
        // bu yüzden hedef dönüşe doğrudan atanır (en çok 45 derece).
        Quaternion hedefDonusu = Quaternion.LookRotation(yon)
                               * Quaternion.AngleAxis(-yan * 45f, Vector3.forward);
        transform.rotation = Quaternion.RotateTowards(
            transform.rotation, hedefDonusu, donusHizi * Time.deltaTime);

        // 5) Skalerle çarpma: burnu yönünde ilerle
        transform.position += transform.forward * hiz * Time.deltaTime;
    }
}
