using UnityEngine;
using TMPro;

public class HoverInfo : MonoBehaviour
{
    public RectTransform infoBox;
    public Canvas canvas;

    void Update()
    {
        if (infoBox.gameObject.activeSelf)
        {
            Vector2 mousePos;
            RectTransformUtility.ScreenPointToLocalPointInRectangle(
                canvas.transform as RectTransform,
                Input.mousePosition,
                canvas.worldCamera,
                out mousePos
            );
            infoBox.localPosition = mousePos + new Vector2(10, -10); // small offset
        }
    }
}