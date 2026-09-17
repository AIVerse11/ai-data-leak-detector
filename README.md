# AI Data Leak Detector

An AI-assisted security tool that analyzes text for potential PII, PHI, credentials, and secrets while reducing sensitive-data exposure through local redaction before API transmission.

## Project Overview
The AI Data Leak Detector was built to explore how large language models can assist with identifying sensitive information in text. The tool accepts user-provided text, performs local pattern-based redaction for Social Security Numbers, and sends the sanitized data to an AI model for a structured security assessment.

The analysis returns a risk score, identifies exposed data types, explains why the information may be risky, and provides remediation recommendations.

## Security Features

- Local SSN detection using regular expressions
- Sensitive-data redaction before API transmission
- Masked API key entry using environment variables
- Input validation to detect empty submissions
- API error handling with try/except
- Structured AI security analysis for PII, PHI, credentials, and secrets

## How It Works

1. The user enters text to be scanned.
2. The program validates that input was provided.
3. Python regular expressions detect SSN patterns locally.
4. Detected SSNs are replaced with `[REDACTED-SSN]` before API transmission.
5. The sanitized text is inserted into a structured security-audit prompt.
6. The prompt is sent to the AI model through the OpenAI API.
7. The model returns a risk score, detected data types, risk explanation, and remediation recommendations.
8. API errors are handled gracefully using Python exception handling.

## Testing

The detector was tested with multiple types of sample data to evaluate its ability to distinguish between low-risk and sensitive information.

| Test Case | Expected Detection | Result |
|---|---|---|
| General meeting information | No sensitive data | Passed |
| Fake Social Security Number | PII / SSN | Passed |
| Fake API key | Secret / Credential | Passed |
| Medical information | PHI | Passed |
| ZIP code + birthday + gender | Re-identification risk | Passed |
| Fake database connection string | Credentials / Secrets | Passed |
| Locally redacted SSN | Detect SSN context without receiving the original value | Passed |

## Privacy and Security Considerations

The original design sent user-provided text directly to the AI API for analysis. This creates a security tradeoff because potentially sensitive information could be transmitted to a third-party service before it is identified as sensitive.

To reduce this exposure, the project was upgraded with local regex-based SSN detection. SSN-shaped values are replaced with `[REDACTED-SSN]` before the prompt is created and transmitted to the AI model.

This demonstrates a hybrid approach: deterministic local detection protects recognizable sensitive-data patterns, while the AI model performs broader contextual analysis on the sanitized text.

## Limitations

- Local redaction currently detects SSNs in the `###-##-####` format only.
- Other sensitive information may still be transmitted to the AI API.
- AI-generated risk scores are model assessments and should not be treated as deterministic security ratings.
- AI analysis can produce false positives or false negatives.
- The tool is an educational prototype and is not a replacement for enterprise DLP, compliance, or incident-response systems.

## Technologies Used

- Python
- Google Colab
- OpenAI API
- Regular Expressions (Regex)
- GitHub

## How to Run

1. Open `AI_Data_Leak_Detector.ipynb` in Google Colab.
2. Run the installation and import cells.
3. Enter your OpenAI API key when prompted. The key is entered using masked input and should never be hard-coded into the notebook.
4. Enter sample text to analyze.
5. Run the remaining cells in order.
6. Review the sanitized data and AI-generated security analysis.

> **Security Note:** Never enter real passwords, API keys, Social Security Numbers, medical records, or other sensitive information when testing this educational project. Use fake sample data only.

## Future Improvements

- Expand local regex redaction to additional sensitive-data patterns such as API keys, email addresses, phone numbers, and database credentials.
- Add structured JSON output for easier parsing and automation.
- Add multiline text input for scanning larger documents.
- Improve local preprocessing to minimize the amount of sensitive information transmitted to external AI services.
- Add a simple user interface with Streamlit.
- Evaluate model responses against predefined test cases to measure false positives and false negatives.

## Author

Erin Cockrell

Built as a hands-on AI security project focused on sensitive-data detection, privacy-aware AI integration, prompt design, and secure API usage.
