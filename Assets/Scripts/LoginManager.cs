using TMPro;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;
using System.Diagnostics;
using System.IO;

public class LoginManager : MonoBehaviour
{
    public TMP_InputField emailField;
    public TMP_InputField passwordField;
    public Button loginButton;
    public TMP_Text errorText;

    // --- Configuration for Python Script ---
    // The path to your Python executable (e.g., python.exe or python)
    private const string PythonPath = "python"; 
    // The name of the Python script file
    private const string ScriptFileName = "ai_login.py";

    void Start()
    {
        loginButton.onClick.AddListener(HandleLogin);
    }

    void HandleLogin()
    {
        string email = emailField.text;
        string password = passwordField.text;

        // 1. Basic C# Validation
        if (!ValidateInput(email, password))
        {
            errorText.text = "Email and password cannot be empty.";
            return;
        }
        if (!IsValidEmail(email))
        {
            errorText.text = "Please enter a valid email address.";
            return;
        }

        // 2. Execute Python Script to handle database insertion
        bool scriptSucceeded = RunPythonScript(email);

        if (scriptSucceeded)
        {
            errorText.text = "";
            // Assuming successful script execution means we can load the next scene
            SceneManager.LoadScene("City");
        }
        else
        {
            // The python script should print an error if it fails
            errorText.text = "Login failed: Database error or invalid credentials.";
        }
    }

    bool ValidateInput(string user, string pass)
    {
        // Simple non-empty check
        return !string.IsNullOrEmpty(user) && !string.IsNullOrEmpty(pass);
    }

    bool RunPythonScript(string email)
    {
        // Get the full path to the Python script.
        // It's best practice to place external files in the root of the project 
        // or a dedicated folder that is accessible at runtime.
        string scriptPath = ScriptFileName;

        // This object holds all the necessary info to start the process
        ProcessStartInfo startInfo = new ProcessStartInfo
        {
            FileName = PythonPath, // The Python executable
            Arguments = $"\"{scriptPath}\" \"{email}\"", // Script path followed by the email argument
            UseShellExecute = false,
            RedirectStandardOutput = true, // To capture the script's output
            RedirectStandardError = true,  // To capture errors
            CreateNoWindow = true          // Don't show a console window
        };

        try
        {
            using (Process process = Process.Start(startInfo))
            {
                if (process == null)
                {
                    UnityEngine.Debug.LogError("Failed to start Python process.");
                    return false;
                }

                // Wait for the script to finish
                process.WaitForExit();

                // Read the output and error streams (optional, but good for debugging)
                string output = process.StandardOutput.ReadToEnd();
                string error = process.StandardError.ReadToEnd();
                int exitCode = process.ExitCode;

                UnityEngine.Debug.Log($"Python Output: {output}");

                if (exitCode == 0)
                {
                    // Success, the user was either inserted or already exists
                    return true;
                }
                else
                {
                    // Script failed (e.g., missing argument, connection error)
                    UnityEngine.Debug.LogError($"Python Error (Exit Code {exitCode}): {error}");
                    return false;
                }
            }
        }
        catch (System.Exception ex)
        {
            UnityEngine.Debug.LogError($"Exception when running Python: {ex.Message}");
            return false;
        }
    }
    bool IsValidEmail(string email)
    {
        // Simple regex for email validation
        try
        {
            var addr = new System.Net.Mail.MailAddress(email);
            return addr.Address == email;
        }
        catch
        {
            return false;
        }
    }
}
