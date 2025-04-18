# 🛠 GenAI Market Intelligence Dashboard

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

*A data-driven platform for tracking Generative AI initiatives, competitor analysis, and partnership opportunities for Dell*

![Dashboard Screenshot]([https://via.placeholder.com/800x400?text=GenAI+Market+Intelligence+Dashboard](https://github.com/Rishiraj-S/Research-Project-under-Mr.-PK-Gupta/blob/main/img/landing_page.png))

## 📌 Overview

This project automates the collection and analysis of **Generative AI (GenAI)** initiatives from **7 major IT companies** (TCS, Infosys, Wipro, LTIMindtree, HCLTech, Tech Mahindra, and Cognizant) across **India and Australia**, providing Dell with actionable insights on:

✅ **Competitor AI investments**  
✅ **Emerging market trends**  
✅ **Potential partnership opportunities**  
✅ **Talent acquisition strategies**  

Built with **Python, Selenium, LangChain, and Streamlit**, it combines **web scraping, NLP, and LLM-powered analytics** into an interactive dashboard.

## ✨ Key Features

| Feature                          | Tech Used                     | Impact |
|----------------------------------|-------------------------------|--------|
| Automated Job & News Scraping    | Selenium, BeautifulSoup, SerpAPI | Collected 1,500+ job listings & 300+ news articles |
| Multi-threaded Scraping          | ThreadPoolExecutor, User-Agent Rotation | 40% faster data collection with fewer blocks |
| NLP Preprocessing                | NLTK, Regex, Lemmatization    | Cleaned text for accurate embeddings |
| Semantic Search (RAG)            | HuggingFace (MiniLM-L6-v2), FAISS | Real-time retrieval of relevant insights |
| LLM-Powered Analysis             | LLaMA 3.3-70B (Groq), LangChain | Strategic recommendations with citations |
| Interactive Dashboard            | Streamlit                     | User-friendly filtering by company/region |

## 🚀 Pipeline Architecture

```mermaid
graph TD
    A[Scrapers] -->|Selenium/BS4| B(Raw Data)
    B --> C[Cleaning & Deduplication]
    C --> D[FAISS Vector Store]
    D --> E[Streamlit UI]
    E --> F[LLM Analysis]
    F --> G[Strategic Insights]
