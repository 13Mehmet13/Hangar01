using UnityEngine;

public class UcagiIlerlet : MonoBehaviour
{
    // Inspector'dan degistirilebilir: metre / saniye
    [SerializeField] private float hiz = 3f;

    private void Update()
    {
        transform.Translate(Vector3.forward * hiz * Time.deltaTime);
    }
}
