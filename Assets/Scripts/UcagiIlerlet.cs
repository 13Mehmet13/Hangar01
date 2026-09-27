using UnityEngine;

public class UcagiIlerlet : MonoBehaviour
{
    // Yukarı/Asagi ok tuslari (veya W/S): ileri / geri
    [SerializeField] private float hiz = 5f;

    // Sag/Sol ok tuslari (veya A/D): donerek yon degistirme
    [SerializeField] private float donusHizi = 60f;

    private void Update()
    {
        float ileriGeri = Input.GetAxis("Vertical");
        float donus = Input.GetAxis("Horizontal");

        transform.Translate(Vector3.forward * ileriGeri * hiz * Time.deltaTime);
        transform.Rotate(Vector3.up * donus * donusHizi * Time.deltaTime);
    }
}
