
# Google ADK Voice Agents & Demos

Welcome to the **Google ADK Voice Agents** repository. This project serves as a comprehensive showcase for building intelligent, multimodal agents using the **Google ADK (Agent Development Kit)** and **Gemini models**.

The examples in this repository demonstrate the progression from simple, single-purpose agents to complex, multi-agent systems capable of autonomous research, structured reporting, and audio content generation.

## 🚀 Examples Overview

This repository contains several example applications (`app`, `app01`, `app06`, etc.), each highlighting different capabilities of the framework.

| Directory | Agent Name | Key Features | Complexity |
|:--- |:--- |:--- |:--- |
| **`app_01`** | **The Guardrailed Assistant** | Basic tool usage (`google_search`), strict instruction adherence, specialized domain focus (AI News only). | 🟢 Low |
| **`app` / `app04`** | **The Interactive Agent** | Rich tool chains (Sentiment Analysis, Trends, Finance, Stocks), interactive user feedback loops, formatted UI responses. | 🟡 Medium |
| **`app05`** | **The Policy Enforcer** | Introduction of **Callbacks** & **Hooks**. Demonstrates how to intercept tool calls for policy enforcement (filtering sources), logging, and persistence. | 🟠 Medium-High |
| **`app06`** | **The Autonomous Podcaster** | Full Multi-Agent Orchestration (`Researcher` + `Podcaster`). Automates an entire pipeline: Research → Report Writing → Scripting → Audio Generation. | 🔴 High |

---

## 🛠️ Deep Dive: The Showcase Apps

### 1. `app_01`: The Foundation
A straightforward implementation of a `root_agent` powered by `gemini-2.0-flash`.
*   **Goal:** Answer user questions strictly about recent AI news.
*   **Mechanism:** Uses `google_search` to ground answers in reality.
*   **Key Learnings:** How to define an agent, attach tools, and use system instructions to enforce strict behavioral guardrails (e.g., refusing off-topic requests).

### 2. `app` & `app04`: The Analyst
A more sophisticated agent designed for interactive analysis.
*   **Goal:** Provide detailed analysis of AI news for US-listed companies.
*   **Tools Stack:**
    *   `google_search`: Source retrieval.
    *   `analyze_news_sentiment`: Determines if news is 🟢 Positive, 🔴 Negative, or ⚪ Neutral.
    *   `track_ai_trends`: Extracts technology trends.
    *   `get_financial_context`: Fetches real-time stock data (via yfinance).
*   **Key Learnings:** How to chain multiple tools to enrich a single response and how to present complex data visually in the chat interface.

### 3. `app06`: The Podcaster (Advanced) 🎙️
The capstone example showing the full power of the Google ADK.
*   **Goal:** autonomously produce an "AI Today" podcast episode based on real-time news.
*   **Architecture:**
    *   **Root Agent (`ai_news_researcher`)**: Conducts deep research on NASDAQ companies, filters for sources, and compiles a structured Markdown report (`ai_research_report.md`).
    *   **Sub-Agent (`podcaster_agent`)**: A specialized agent that takes the report, writes a conversational script between two hosts (Joe & Jane), and generates an audio file.
*   **Advanced Features:**
    *   **Callbacks:** `filter_news_sources_callback` ensures only trusted domains are used; `enforce_data_freshness_callback` guarantees recent news.
    *   **Structured Output:** Uses Pydantic models (`AINewsReport`) to ensure data integrity across agent handoffs.
    *   **Multimodal Output:** Produces actual `.wav` audio files.

---

## 💻 Technical Stack

*   **Framework:** Google ADK (Agent Development Kit)
*   **Models:** Gemini 2.0 Flash / Gemini 2.5 Flash
*   **Language:** Python 3.10+
*   **External Data:** `yfinance`, `alpha_vantage` (implied)
*   **Search:** Google Search Tool

## ⚙️ Getting Started

1.  **Clone the repository**:
    ```bash
    git clone <repo-url>
    cd GoogleADK-voice-agents
    ```

2.  **Environment Setup**:
    Ensure you have your API keys (Google GenAI, etc.) ready. Most agents look for a `.env` file in their respective directories.
    ```bash
    # Example .env structure
    GOOGLE_API_KEY=your_key_here
    ```

3.  **Run an Agent**:
    Navigate to the desired app directory and run the agent module.
    *   *Note: Specific runner scripts may vary based on your local setup.*

    ```bash
    # Example for running the app06 podcaster
    python -m app06.agent
    ```

## 📂 Project Structure

```text
├── app/                # Interactive Analyst Agent
├── app04/              # Variant of Analyst Agent
├── app05/              # Callback & Persistence Demo
├── app06/              # Multi-Agent Podcaster Demo
├── app_01/             # Basic "Hello World" Agent
├── ai_research_report.md # Generated report output (example)
└── ai_today_podcast.wav  # Generated audio output (example)
```

---
*Created with the Google ADK Framework.*
