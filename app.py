
import streamlit as st
import re
import json
from openai import OpenAI

st.set_page_config(
    page_title="AI Data Leak Detector",
    page_icon="🔐",
    layout="centered"
)

st.title("🔐 AI Data Leak Detector")

st.write(
    "Scan text for potentially sensitive information before it is analyzed by AI."
)

st.warning(
    "Use fake or authorized test data only. Do not enter real passwords, API keys, "
    "SSNs, PHI, or other confidential information."
)

# Local sensitive-data detection patterns
ssn_pattern = r"\b\d{3}[-\s]\d{2}[-\s]\d{4}\b"

email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"

phone_pattern = r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"

api_key_pattern = r"\bsk-[A-Za-z0-9_-]{10,}\b"

password_pattern = r"(?i)\b(password|passwd|pwd|secret|access[_\s-]?token)\s*[:=]\s*\S+"

data = st.text_area(
    "Enter text to scan:",
    height=220,
    placeholder="Paste fake or authorized test data here..."
)

scan_button = st.button("Scan for Sensitive Data")

def redact_sensitive_data(data):
    redacted_data = re.sub(ssn_pattern, "[REDACTED-SSN]", data)
    redacted_data = re.sub(email_pattern, "[REDACTED-EMAIL]", redacted_data)
    redacted_data = re.sub(phone_pattern, "[REDACTED-PHONE]", redacted_data)
    redacted_data = re.sub(api_key_pattern, "[REDACTED-API-KEY]", redacted_data)
    redacted_data = re.sub(password_pattern, "[REDACTED-PASSWORD]", redacted_data)

    return redacted_data

if scan_button:
    if not data.strip():
        st.error("Please enter text to scan.")
    else:
        redacted_data = redact_sensitive_data(data)

        prompt = f"""
You are a data security auditor.

Analyze the following internal data for sensitive information.

Check for PII, PHI, secrets, and credentials.

Return ONLY valid JSON. Do not include markdown, code fences, or text outside the JSON.

Use exactly this structure:

{{
  "score": 0,
  "findings": [
    {{
      "data_type": "type of sensitive data",
      "evidence": "redacted evidence only",
      "risk": "why this finding is risky"
    }}
  ],
  "remediation": [
    "recommended action"
  ]
}}

The score must be an integer from 1 to 100, where higher numbers indicate greater risk.

Do not reproduce raw passwords, credentials, secrets, PII, or PHI in your response.

Refer to sensitive values only by their data type or a redacted placeholder.

If no sensitive information is detected, return an empty findings list and appropriate remediation.

Data:

{redacted_data}
"""

        try:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

            with st.spinner("Analyzing sanitized data..."):
                response = client.responses.create(
                    model="gpt-5-mini",
                    input=prompt
                )

            raw_output = response.output_text.strip()

            # Remove markdown code fences if the model adds them
            if raw_output.startswith("```"):
                raw_output = raw_output.strip("`")
                if raw_output.lower().startswith("json"):
                    raw_output = raw_output[4:].strip()

            analysis = json.loads(raw_output)

            st.subheader("Security Analysis")

            st.metric("Risk Score", f'{analysis["score"]}/100')

            st.subheader("Findings")

            if analysis["findings"]:
                for finding in analysis["findings"]:
                    with st.container(border=True):
                        st.write(f'**Data Type:** {finding["data_type"]}')
                        st.write(f'**Evidence:** {finding["evidence"]}')
                        st.write(f'**Risk:** {finding["risk"]}')
            else:
                st.success("No sensitive-data findings detected.")

            st.subheader("Remediation")

            for action in analysis["remediation"]:
                st.write(f"- {action}")

        except json.JSONDecodeError:
            st.error("The AI response was not valid JSON. Please try again.")

        except Exception as error:
            st.error("The AI analysis could not be completed.")
            st.error(str(error))
