using UnityEngine;

public class PervaneDondur : MonoBehaviour
{
    // Inspector'dan degistirilebilir: derece / saniye
    [SerializeField] private float donusHizi = 1200f;

    // Yerel Z ekseni: ucagin burun yonu
    [SerializeField] private Vector3 donusEkseni = Vector3.forward;

    private void Update()
    {
        // Time.deltaTime ile donus kare hizindan bagimsiz olur.
        transform.Rotate(donusEkseni, donusHizi * Time.deltaTime);
    }
}
