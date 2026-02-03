# CV Tailor

An AI-powered tool to tailor your CV (Markdown) to any job description using Google Gemini 3 Flash (Preview).

## Features
-   **AI-Powered Customization**: Uses Gemini 3 Flash (Preview) to rewrite your CV.
-   **Markdown Preservation**: Keeps your original formatting.
-   **Privacy Focused**: Runs locally on your machine.
-   **Premium UI**: Clean and simple interface built with Streamlit.

## Setup

1.  **Install Dependencies**:
    ```bash
    uv sync
    ```

2.  **Environment Setup**:
    -   Copy `.env.example` to `.env`:
        ```bash
        cp .env.example .env  # On Windows: copy .env.example .env
        ```
    -   Add your Gemini API Key to `.env`.

## Usage

Run the application:
```bash
uv run streamlit run app.py
```

1.  Upload your **Markdown CV**.
2.  Paste the **Job Description**.
3.  Click **Tailor Resume**.
4.  Download the result!

PS: A great tool to use to create a markdown CV is [Markdown Resume](https://github.com/junian/markdown-resume)

TODO: Potentially add proper integrationm with Markdown Resume to avoid needing to copy back and forth between the two tools.
