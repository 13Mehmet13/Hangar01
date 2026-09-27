using UnityEngine;
using UnityEngine.InputSystem;

public class UcagiIlerlet : MonoBehaviour
{
    // Play'e basilir basilmaz otomatik olarak bu hizda ileri gider
    // (klavye/focus sorunlarindan bagimsiz, ekran kaydinda hareket her zaman garanti gorunur)
    [SerializeField] private float hiz = 5f;

    // Ok tuslari / WASD ile ekstra kontrol (calisirsa bonus, calismasa da sorun degil)
    [SerializeField] private float donusHizi = 60f;

    private void Update()
    {
        float ileriGeri = 1f;
        float donus = 0f;

        var kb = Keyboard.current;
        if (kb != null)
        {
            if (kb.downArrowKey.isPressed || kb.sKey.isPressed) ileriGeri = -1f;
            if (kb.rightArrowKey.isPressed || kb.dKey.isPressed) donus = 1f;
            else if (kb.leftArrowKey.isPressed || kb.aKey.isPressed) donus = -1f;
        }

        transform.Translate(Vector3.forward * ileriGeri * hiz * Time.deltaTime);
        transform.Rotate(Vector3.up * donus * donusHizi * Time.deltaTime);
    }
}
