using TMPro;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;
using System.Diagnostics;
using System.IO;

public class LoginManager : MonoBehaviour
{
    [Header("Email Screen")]
    public GameObject emailScreen;
    public TMP_InputField emailField;
    public Button sendOTPButton;
    public TMP_Text emailErrorText;

    [Header("OTP Screen")]
    public GameObject otpScreen;
    public TMP_InputField otpField;
    public Button verifyOTPButton;
    public TMP_Text otpErrorText;

    // --- Configuration for Python Script ---
    private const string PythonPath = "python"; 
    private const string ScriptFileName = "Assets/Scripts/db_otp.py";
    private const string OTPFilePath = "Assets/otp.txt";

    private string currentEmail;

    void Start()
    {
        // Setup button listeners
        sendOTPButton.onClick.AddListener(HandleEmailSubmit);
        verifyOTPButton.onClick.AddListener(HandleOTPVerify);

        // Show email screen first, hide OTP screen
        ShowEmailScreen();
    }

    void ShowEmailScreen()
    {
        emailScreen.SetActive(true);
        otpScreen.SetActive(false);
        emailErrorText.text = "";
        emailField.text = "";
    }

    void ShowOTPScreen()
    {
        emailScreen.SetActive(false);
        otpScreen.SetActive(true);
        otpErrorText.text = "";
        otpField.text = "";
    }

    void HandleEmailSubmit()
    {
        string email = emailField.text;

        // Validate email
        if (string.IsNullOrEmpty(email))
        {
            emailErrorText.text = "Email cannot be empty.";
            return;
        }
        if (!IsValidEmail(email))
        {
            emailErrorText.text = "Please enter a valid email address.";
            return;
        }

        // Execute Python script to generate and send OTP
        bool scriptSucceeded = RunPythonScript(email);

        if (scriptSucceeded)
        {
            currentEmail = email;
            emailErrorText.text = "";
            // Move to OTP screen
            ShowOTPScreen();
        }
        else
        {
            emailErrorText.text = "Failed to send OTP. Please try again.";
        }
    }

    void HandleOTPVerify()
    {
        string enteredOTP = otpField.text;

        // Validate OTP input
        if (string.IsNullOrEmpty(enteredOTP))
        {
            otpErrorText.text = "OTP cannot be empty.";
            return;
        }

        // Read the OTP from the file written by Python
        string correctOTP = ReadOTPFromFile();

        if (string.IsNullOrEmpty(correctOTP))
        {
            otpErrorText.text = "Error reading OTP. Please request a new one.";
            return;
        }

        // Compare OTPs
        if (enteredOTP.Trim() == correctOTP.Trim())
        {
            // OTP is correct, proceed to next scene
            otpErrorText.text = "";

            // Clean up the OTP file for security
            CleanupOTPFile();

            SceneManager.LoadScene("City");
        }
        else
        {
            otpErrorText.text = "Invalid OTP. Please try again.";
        }
    }

    bool RunPythonScript(string email)
    {
        string scriptPath = ScriptFileName;

        ProcessStartInfo startInfo = new ProcessStartInfo
        {
            FileName = PythonPath,
            Arguments = $"-u \"{Path.GetFullPath(scriptPath)}\" \"{email}\"",
            UseShellExecute = false,
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            CreateNoWindow = true,
            WorkingDirectory = Application.dataPath // ensures correct relative paths
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

                process.WaitForExit();

                string output = process.StandardOutput.ReadToEnd();
                string error = process.StandardError.ReadToEnd();
                int exitCode = process.ExitCode;

                UnityEngine.Debug.Log($"Python Output: {output}");

                if (exitCode == 0)
                {
                    return true;
                }
                else
                {
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

    string ReadOTPFromFile()
    {
        try
        {
            if (File.Exists(OTPFilePath))
            {
                string otp = File.ReadAllText(OTPFilePath);
                return otp;
            }
            else
            {
                UnityEngine.Debug.LogError($"OTP file not found at: {OTPFilePath}");
                return null;
            }
        }
        catch (System.Exception ex)
        {
            UnityEngine.Debug.LogError($"Error reading OTP file: {ex.Message}");
            return null;
        }
    }

    void CleanupOTPFile()
    {
        try
        {
            if (File.Exists(OTPFilePath))
            {
                File.Delete(OTPFilePath);
                UnityEngine.Debug.Log("OTP file cleaned up.");
            }
        }
        catch (System.Exception ex)
        {
            UnityEngine.Debug.LogError($"Error deleting OTP file: {ex.Message}");
        }
    }

    bool IsValidEmail(string email)
    {
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