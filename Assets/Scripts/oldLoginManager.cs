using TMPro;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;  // or TMPro if using TextMeshPro

public class OldLoginManager : MonoBehaviour
{
    public TMP_InputField emailField;
    public TMP_InputField passwordField;
    public Button loginButton;
    public TMP_Text errorText;


    void Start()
    {
        loginButton.onClick.AddListener(HandleLogin);
    }

    void HandleLogin()
    {
        string email = emailField.text;
        string password = passwordField.text;

        // Simple check (for demo/hackathon)
        if (ValidateCredentials(email, password))
        {
            errorText.text = "";
            SceneManager.LoadScene("City");
        }
        else
        {
            errorText.text = "Invalid username or password.";
        }
    }

    bool ValidateCredentials(string user, string pass)
    {
        // For demo: either accept anything non-empty, or check against hardcoded
        return !string.IsNullOrEmpty(user) && !string.IsNullOrEmpty(pass);
    }
}