using UnityEngine;

public class CameraMove : MonoBehaviour
{
    public float panSpeed = 5f;      // How fast the camera moves

    void Update()
    {
        // Read input axes. Unity's built-in Horizontal/Vertical handle WASD + Arrow keys by default.
        float moveX = Input.GetAxisRaw("Horizontal");
        float moveY = Input.GetAxisRaw("Vertical");

        // Combine into a movement vector
        Vector3 move = new Vector3(moveX, moveY, 0);

        // Normalize so diagonal movement isn't faster
        if (move.sqrMagnitude > 1)
            move.Normalize();

        // Move camera in world space, scaled by speed and frame time
        transform.position += move * panSpeed * Time.deltaTime;
    }
}
