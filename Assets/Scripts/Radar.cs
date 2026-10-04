using UnityEngine;

// Hedef görüş konisinin içinde mi, sağda mı solda mı?
public class Radar : MonoBehaviour
{
    [SerializeField] private Transform hedef;
    [SerializeField] private float yarimAci = 35f;   // koninin yarı açısı, derece
    [SerializeField] private float menzil = 120f;

    // [field: SerializeField] otomatik özelliği Inspector'da görünür kılar
    [field: SerializeField] public bool Goruyor { get; private set; }
    [field: SerializeField] public float YanTaraf { get; private set; }

    private void Update()
    {
        if (hedef == null) return;

        Vector3 fark = hedef.position - transform.position;
        Vector3 yon = fark.normalized;

        // İç çarpım: 1 tam önümde, 0 yanımda, negatif arkamda
        float onde = Vector3.Dot(transform.forward, yon);
        float esik = Mathf.Cos(yarimAci * Mathf.Deg2Rad);
        Goruyor = onde > esik && fark.magnitude < menzil;

        // Dış çarpım: yukarı bileşen pozitifse hedef sağda
        YanTaraf = Vector3.Cross(transform.forward, yon).y;
    }

    private void OnDrawGizmos()
    {
        // İleri yön: her zaman mavi
        Gizmos.color = Color.cyan;
        Gizmos.DrawRay(transform.position, transform.forward * 30f);

        if (hedef == null) return;

        // Hedefe giden vektör: görüyorsa yeşil, görmüyorsa kırmızı
        Gizmos.color = Goruyor ? Color.green : Color.red;
        Gizmos.DrawLine(transform.position, hedef.position);
        Gizmos.DrawWireSphere(hedef.position, 4f);
    }
}
