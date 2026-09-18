# STAR-E Writeup
## AI Data Leak Detector

### Situation

This was my first time building an AI application. The project was to create a tool that could scan internal data for PII, PHI, credentials, and secrets and return a risk assessment. I already had experience working with technical systems and troubleshooting, but I had not built an application that sent data to an AI model through an API.

### Task

My goal was to build a working sensitive-data scanner that could accept a block of text, identify possible exposure, assign a risk score, explain the findings, and recommend remediation.

As I worked on it, I also wanted to make sure the tool was not creating another security problem by exposing the same sensitive information it was supposed to detect.

### Action

I first built the basic input and AI analysis flow. I then added local pattern matching and redaction so known sensitive values could be masked before the data was sent to the AI model.

I added detection for SSNs, email addresses, phone numbers, API keys, and labeled credentials. During testing, I found both false positives and false negatives. For example, a product ID formatted like a phone number was incorrectly detected as a phone number. I also found that the original patterns missed an SSN containing spaces and a phone number without separators.

I adjusted the patterns and tested them again. I also added input validation, API error handling, JSON response handling, and instructions preventing the model from returning raw sensitive values.

After the notebook was working, I built a Streamlit interface and deployed the application so it could be tested through a web interface instead of only through Colab.

### Result

The finished application accepts text, redacts known sensitive-data patterns locally, sends the redacted version for AI analysis, and returns a risk score, individual findings, risk explanations, and remediation steps.

I tested the application with clean data, multiple types of sensitive data, false-positive and false-negative cases, updated detection patterns, and empty input. I also moved the API key out of the code and stored it as a private secret for the deployed application.

Testing showed that the tool works, but it also exposed limitations that I documented instead of treating the detector as perfect.

### Engineering Tradeoff

The biggest tradeoff was using a third-party AI model for reasoning while trying to protect the data being analyzed.

Sending more of the original data to the model can give it more context, but it also increases the amount of information leaving the local application. I reduced that exposure by redacting known patterns before the API request.

That creates another tradeoff. Pattern matching does not catch every possible representation of sensitive information. Making the patterns broader can catch more data, but it can also increase false positives. Keeping them narrow reduces false positives but can allow some sensitive data to pass through.

For example, testing showed that an obfuscated email such as `test.user [at] example.com` is not currently caught by the local email pattern. I chose to document that limitation rather than claim that the tool can detect every form of sensitive data.
