using TMPro;
using UnityEngine;

public class CreditScoreDisplay : MonoBehaviour
{
    public TMP_Text creditScoreText;

    void Start()
    {
        string creditScore = PlayerPrefs.GetString("CurrentUserCreditScore", "N/A");
        if (creditScore == "good")
        {
            creditScoreText.color = Color.green;
            creditScoreText.text = "900";
        }
        else if (creditScore == "average")
        {
            creditScoreText.color = Color.yellow;
            creditScoreText.text = "500";
        }
        else if (creditScore == "poor")
        {
            creditScoreText.color = Color.red;
            creditScoreText.text = "250";
        }
    }
}