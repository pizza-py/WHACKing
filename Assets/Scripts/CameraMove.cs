using UnityEngine;

public class CameraMove : MonoBehaviour
{
    public float panSpeed = 5f;
    public float dragSpeed = 0.5f;
    public Vector2 panLimitMin = new Vector2(-50, -50);
    public Vector2 panLimitMax = new Vector2(50, 50);
    public float inertiaDamping = 5f; //Higher = stops faster
    
    public float zoomSpeed = 5f;
    public float minZoom = 3f;
    public float maxZoom = 15f;

    private Vector3 dragOrigin;
    private Vector3 dragVelocity; //stores movement after releasing drag

    void Update()
    {
        KeyboardPan();
        MouseDrag();
        Zoom();
        ApplyInertia();
    }
    void KeyboardPan()
    {
        //Read input axes. Unity's built-in Horizontal/Vertical handle WASD + Arrow keys by default.
        float moveX = Input.GetAxisRaw("Horizontal");
        float moveY = Input.GetAxisRaw("Vertical");

        //Combine into a movement vector
        Vector3 move = new Vector3(moveX, moveY, 0);

        //Normalize so diagonal movement isn't faster
        if (move.sqrMagnitude > 1)
            move.Normalize();

        //Move camera in world space, scaled by speed and frame time
        transform.position += move * panSpeed * Time.deltaTime;
        ClampPosition();
    }
    void MouseDrag()
    {
        //Start drag when right mouse button pressed
        if (Input.GetMouseButtonDown(1))
        {
            dragOrigin = Camera.main.ScreenToWorldPoint(Input.mousePosition);
            dragVelocity = Vector3.zero; //stop previous inertia
        }

        //While holding right mouse button
        if (Input.GetMouseButton(1))
        {
            Vector3 difference = dragOrigin - Camera.main.ScreenToWorldPoint(Input.mousePosition);
            transform.position += difference;
            ClampPosition();

            dragVelocity = difference / Time.deltaTime; //store velocity for inertia
            dragOrigin = Camera.main.ScreenToWorldPoint(Input.mousePosition);
        }
    }
    void Zoom()
    {
        //Scroll wheel input: positive when scrolling up
        float scroll = Input.GetAxis("Mouse ScrollWheel");
        if (Mathf.Abs(scroll) > 0.01f)
        {
            Camera cam = Camera.main;
            float newSize = cam.orthographicSize - scroll * zoomSpeed;
            cam.orthographicSize = Mathf.Clamp(newSize, minZoom, maxZoom);
        }
    }
    void ApplyInertia()
    {
        if (dragVelocity.sqrMagnitude > 0.01f && !Input.GetMouseButton(1))
        {
            transform.position += dragVelocity * Time.deltaTime;
            ClampPosition();
            //Gradually slow down
            dragVelocity = Vector3.Lerp(dragVelocity, Vector3.zero, inertiaDamping * Time.deltaTime);
        }
    }
    void ClampPosition()
    {
        Vector3 pos = transform.position;
        pos.x = Mathf.Clamp(pos.x, panLimitMin.x, panLimitMax.x);
        pos.y = Mathf.Clamp(pos.y, panLimitMin.y, panLimitMax.y);
        transform.position = pos;
    }
}
