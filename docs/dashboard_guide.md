# Dashboard Guide

The Enterprise UI Dashboard is a sleek, modern web application built for insurance adjusters and support teams to visually inspect AI decisions.

## Accessing the Dashboard

Ensure the application is running via the `start.ps1` script. Open your web browser and navigate to:
`http://localhost:3000`

## Submitting a Claim

1. **Claim Object**: Select the category of the damaged item (Car, Laptop, or Package).
2. **User Description**: Enter what happened in plain English (e.g., "I dropped my laptop and the screen cracked").
3. **Evidence Image**: Drag and drop a `.jpg` or `.png` file into the upload area.
4. **Mock Mode**: For testing or demos without LLM API keys, ensure the **"Use Mock AI"** checkbox is checked.
5. Click **Process Claim**.

## Understanding the Results Card

After a few moments (or instantly if using Mock AI), the Results Card will slide into view.

- **Claim Status**: The ultimate verdict from the Decision Engine (`supported`, `rejected`, or `escalated`).
- **Detected Object Part & Issue**: What the Vision Engine identified in the photo.
- **Justification**: A polished, human-readable explanation written by the Explainability Engine outlining *why* the decision was made.
- **Severity & Evidence Standard**: Shows whether the image quality and angles met the strict corporate requirements.
- **Risk & Fraud Flags**: If any red flags are detected (e.g., missing metadata, perceptual hashing duplication, high-risk user history), they will be listed here as bright red badges.
