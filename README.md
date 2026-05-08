# Medical Literature Research AI Agent

AI-powered research assistant that automates medical literature review using LangChain ReAct architecture and PubMed API.

## Features
- Auto-decomposes research questions into sub-queries
- Searches PubMed in real-time via API
- Generates structured reports with mandatory PMID citations
- Streamlit interactive frontend with report download

## Tech Stack
Python | LangChain | LangGraph | DeepSeek API | PubMed API | Streamlit

## Results
North Star Metric: Time to complete 10-paper literature review
Internal test: Reduced from ~2 hours to ~12 minutes

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Create `.env` file with `DEEPSEEK_API_KEY=your_key`
3. Run: `streamlit run app.py`
