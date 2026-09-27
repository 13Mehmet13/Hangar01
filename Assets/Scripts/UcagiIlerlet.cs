using UnityEngine;
using UnityEngine.InputSystem;

public class UcagiIlerlet : MonoBehaviour
{
    // Yukarı/Asagi ok tuslari (veya W/S): ileri / geri
    [SerializeField] private float hiz = 5f;

    // Sag/Sol ok tuslari (veya A/D): donerek yon degistirme
    [SerializeField] private float donusHizi = 60f;

    private void Update()
    {
        var kb = Keyboard.current;
        if (kb == null) return;

        float ileriGeri = 0f;
        if (kb.upArrowKey.isPressed || kb.wKey.isPressed) ileriGeri = 1f;
        else if (kb.downArrowKey.isPressed || kb.sKey.isPressed) ileriGeri = -1f;

        float donus = 0f;
        if (kb.rightArrowKey.isPressed || kb.dKey.isPressed) donus = 1f;
        else if (kb.leftArrowKey.isPressed || kb.aKey.isPressed) donus = -1f;

        transform.Translate(Vector3.forward * ileriGeri * hiz * Time.deltaTime);
        transform.Rotate(Vector3.up * donus * donusHizi * Time.deltaTime);
    }
}
