# Prompt Iteration Log
## AI Data Leak Detector

This was my first time building an AI application. At first, I was focused on getting the model to identify sensitive data and return useful results. As I tested the project, I started finding problems I had not considered at the beginning. I changed the prompt as I found those problems.

## Version 1: Initial Security Audit

My first version gave the model a role and told it what types of information to look for.

### Prompt

You are a data security auditor.

Analyze the following internal data for sensitive information.

Check for PII, PHI, secrets, and credentials.

Return your analysis in this format:

Risk Score (1-100):

Exposed Data Types:

Exact Risky Text:

Why It Is Risky:

How To Fix It:

Data:

{data}

### What I noticed

The model could identify sensitive information and explain the risk, but I saw a problem with the way I was handling the data. I was sending the original data to the model and asking it to return the exact risky text.

For a tool that is supposed to help find sensitive-data exposure, I did not want it unnecessarily repeating the same sensitive information.

That led to my second version.

## Version 2: Redaction Before AI Analysis

I added a local redaction step and changed the prompt so the model received `redacted_data` instead of the original `data`.

I also changed `Exact Risky Text` to `Sensitive Data Evidence (redacted only)`.

### Prompt

You are a data security auditor.

Analyze the following internal data for sensitive information.

Check for PII, PHI, secrets, and credentials.

Return your analysis in this format:

Risk Score (1-100):

Exposed Data Types:

Sensitive Data Evidence (redacted only):

Why It Is Risky:

How To Fix It:

Do not reproduce raw passwords, credentials, secrets, PII, or PHI in your response.

Refer to sensitive values only by their data type or a redacted placeholder.

Data:

{redacted_data}

### What changed

The model could still explain what it found, but the sensitive values were represented by placeholders such as `[REDACTED-SSN]`, `[REDACTED-EMAIL]`, `[REDACTED-PHONE]`, `[REDACTED-API-KEY]`, and `[REDACTED-PASSWORD]`.

The next problem I wanted to solve was the format of the response. It was readable, but it was still one text report. I wanted my program to be able to work with the individual parts of the report.

## Version 3: JSON Output

For the final version, I required the model to return only valid JSON.

### Prompt Changes

Return ONLY valid JSON. Do not include markdown, code fences, or text outside the JSON.

Use exactly this structure:

{
  "score": 0,
  "findings": [
    {
      "data_type": "type of sensitive data",
      "evidence": "redacted evidence only",
      "risk": "why this finding is risky"
    }
  ],
  "remediation": [
    "recommended action"
  ]
}

The score must be an integer from 1 to 100.

When a finding may be subject to a specific privacy, security, or data protection regulation, identify the relevant regulation in the risk explanation.

Do not invent a regulation if one does not clearly apply.

Do not reproduce raw passwords, credentials, secrets, PII, or PHI in your response.

Refer to sensitive values only by their data type or a redacted placeholder.

If no sensitive information is detected, return an empty findings list and appropriate remediation.

Data:

{redacted_data}

### What changed

The response was now separated into a risk score, findings, evidence, risk explanations, and remediation steps.

I used `json.loads()` to read the JSON response in Python. This also allowed me to display each part separately when I built the Streamlit interface.

## Final Testing Adjustment

During the required SSN test, the scanner correctly identified the SSN as sensitive PII and gave it a high risk score, but the response mentioned regulatory requirements without naming one. I updated the prompt to identify a relevant privacy, security, or data protection regulation when one clearly applies. I also added an instruction not to invent a regulation when one does not clearly apply.

I ran the SSN test again after the change. The scanner still identified the SSN as sensitive PII and returned a high risk score, but it also included applicable regulatory context in the risk explanation.

## What I Learned

This project changed how I thought about prompting. I started out thinking mainly about what I wanted the AI to tell me. Testing made me start thinking about what information I was giving the AI, what it could return, and how my program would use that response.

I also learned that the prompt could not solve everything. I still needed local redaction, input validation, error handling, and testing. My testing found both false positives and false negatives, which showed me that the detector still has limitations even when the AI response looks correct.
