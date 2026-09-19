# AI Data Leak Detector

This is my first AI application project. I built it to learn how Python and an AI model could be used together to find potentially sensitive information in text.

As I worked on the project, I realized that sending sensitive data to an AI model in order to find out whether it is sensitive creates its own security problem. I added local detection and redaction so several types of sensitive information can be masked before the text is sent to the AI model.

## Live Demo

The Streamlit version of the project is available here:

https://ai-data-leak-detector.streamlit.app/

Use fake test data only. Do not enter real passwords, API keys, SSNs, medical information, or other confidential information.

## What the Tool Does

The user enters a block of text that they want to scan.

Before the AI analysis begins, Python uses regular expressions to look for several recognizable sensitive-data patterns. When one is found, the value is replaced with a redacted placeholder.

The redacted text is then sent to the AI model for a security analysis.

The final report includes:

- Risk score
- Type of data found
- Redacted evidence
- Explanation of the risk
- Recommended remediation

## How It Works

1. The user enters text.
2. The program checks that the user actually entered something.
3. Regular expressions check the text locally for known sensitive-data patterns.
4. Detected values are replaced with redacted placeholders.
5. The redacted text is added to the AI prompt.
6. The prompt is sent through the OpenAI API.
7. The model returns the analysis as JSON.
8. Python reads the JSON response.
9. The notebook or Streamlit application displays the risk score, findings, and remediation.

The basic flow is:

User Input → Local Detection → Local Redaction → AI Analysis → JSON Response → Security Report

## Local Detection and Redaction

The current version checks locally for:

- Social Security Numbers
- Email addresses
- Phone numbers
- `sk-` style API keys
- Labeled passwords, secrets, and access tokens

Examples of the placeholders used after detection include:

- `[REDACTED-SSN]`
- `[REDACTED-EMAIL]`
- `[REDACTED-PHONE]`
- `[REDACTED-API-KEY]`
- `[REDACTED-PASSWORD]`

The goal is to reduce the amount of recognizable sensitive information sent to the AI model.

## Testing

I tested the project with fake data only.

Testing included:

- Clean text with no obvious sensitive information
- Multiple sensitive-data types in the same input
- SSNs
- Email addresses
- Phone numbers
- API keys
- Passwords and other labeled credentials
- Empty input
- False-positive cases
- False-negative cases

Testing found problems that I had to correct.

One false-positive test used a product ID that looked like a phone number. The local pattern treated it as a phone number even though it was not one.

I also found false negatives. The first version of my SSN pattern did not detect an SSN written with spaces, and the original phone pattern missed a phone number with no separators. I updated the patterns and tested them again.

An obfuscated email such as `test.user [at] example.com` is still not detected by the current email pattern. I left this as a documented limitation instead of making the pattern so broad that it could create more false positives.

### Required Test Cases

I also ran the finished project against the six required test cases:

- Clean text with no sensitive information: returned a low risk score with no findings.
- Fake SSN: identified as sensitive PII with a high risk score and applicable regulatory context.
- Fake API key: identified as a credential/secret with recommendations for rotation and secrets management.
- Medical information without an identifying number: recognized the health information from context.
- ZIP code, birth date, and gender: identified the combined values as a re-identification risk.
- Database connection string: identified multiple risks, including credentials and internal resource information.

The SSN test initially identified the data correctly but did not name an applicable regulation. I updated the prompt and reran the test successfully. This change is documented in `PROMPT_ITERATION_LOG.md`.

## Input and Error Handling

The project includes basic checks for problems that can happen while it is running.

If the user submits an empty input, the application stops and asks for text instead of sending an API request.

The application also handles API errors and invalid JSON responses so a failure does not automatically produce an unhandled Python error.

## API Key Handling

The API key is not hard-coded into the project.

The Colab notebook uses protected key entry instead of storing the key directly in the code.

The deployed Streamlit application reads the API key from Streamlit Secrets.

The real API key is not included in the repository.

## Prompt Changes

The prompt changed as I worked through the project.

The first version focused on getting a useful security report. The next version added instructions for redacted evidence and used locally redacted data instead of the original input. The prompt changed as I worked through the project.

The first version focused on getting a useful security report. The next version added instructions for redacted evidence and used locally redacted data instead of the original input. The final version requires JSON so Python can work with individual parts of the response.

During final testing, I also added instructions for the model to identify relevant privacy, security, or data protection regulations when they clearly apply, while telling it not to invent a regulation when one does not apply.

The full prompt development notes are available in `PROMPT_ITERATION_LOG.md`.

## Streamlit Interface

After the notebook version was working, I built a Streamlit interface so the detector could be tested as a web application.

The interface includes:

- Multiline text input
- Scan button
- Input validation
- Risk score display
- Individual findings
- Risk explanations
- Remediation recommendations

This was an additional upgrade beyond running the project only inside Google Colab.

## Limitations

This is a learning project and proof of concept. It is not an enterprise Data Loss Prevention system.

Some current limitations are:

- Regular expressions only recognize patterns they were designed to detect.
- Sensitive information written in unusual or obfuscated formats may not be redacted.
- Making a regex pattern broader can also increase false positives.
- The AI model can still produce incorrect classifications.
- The risk score is generated by the model and should not be treated as an official security rating.
- Local redaction reduces exposure but does not guarantee that every type of sensitive information has been removed.
- The project should only be tested with fake or authorized data.

## Technologies Used

- Python
- Google Colab
- OpenAI API
- Regular Expressions
- JSON
- Streamlit
- GitHub

## How to Run the Notebook

1. Open `AI_Data_Leak_Detector.ipynb` in Google Colab.
2. Run the cells in order.
3. Enter the API key when prompted.
4. Enter fake sample data.
5. Run the local detection and redaction steps.
6. Run the AI analysis.
7. Review the risk score, findings, and remediation.

A fake dataset is included in `sample_test_data.txt`.

## How to Run the Streamlit Version

Install the required packages:

```text
pip install -r requirements.txt
```

Run the application:

```text
streamlit run app.py
```

The application expects an OpenAI API key to be available through Streamlit Secrets as `OPENAI_API_KEY`.

Do not place the real API key directly inside `app.py`.

## Project Files

- `AI_Data_Leak_Detector.ipynb` - Colab notebook
- `app.py` - Streamlit application
- `requirements.txt` - Python package requirements
- `sample_test_data.txt` - fake data for testing
- `PROMPT_ITERATION_LOG.md` - changes made to the prompt
- `STAR-E.md` - project STAR-E writeup
- `.gitignore` - files and secrets that should not be committed

## What I Learned

This was my first time building an AI application, and I originally thought most of the work would be getting the model to return the right answer.

While building and testing it, I learned that I also had to think about what data was being sent to the model, what should be removed first, how consistent the response would be, what happens when something fails, and how I could test whether my own detection was wrong.

Finding false positives and false negatives was one of the most useful parts of the project because it showed me that getting a successful output does not automatically mean the tool is working correctly.

## Author

Erin Cockrell
