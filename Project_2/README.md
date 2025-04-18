# Project Overview
This project analyzes Generative AI (GenAI) startups in India and Australia to identify trends, technological focus areas, and potential partnership opportunities for Dell. The analysis is conducted through data extraction, preprocessing, and machine learning techniques to derive actionable insights.

# Key Features
- Data Collection: Web scraping of startup information from various sources
- Text Preprocessing: Cleaning and standardizing text data using NLTK
- Landscape Mining:
    - KeyBERT for phrase extraction
    - Zero-shot classification to categorize startups by industry, tech stack, use case, and business model
  
- Comparative Analysis: Visualization of differences between Indian and Australian GenAI startups
- GenAI Filtering: Identification of startups focused specifically on Generative AI

# Technologies Used
- Python
- Jupyter Notebook
- KeyBERT for keyword extraction
- Hugging Face Transformers for zero-shot classification
- NLTK for text preprocessing
- BeautifulSoup and Selenium for web scraping
- Pandas for data manipulation
- Matplotlib and Seaborn for visualization

# Notebook Structure
1. Introduction
- Project objectives and key steps

2. Text Preprocessing
- Loading datasets for Indian and Australian startups
- Text cleaning and standardization

3. Startup Landscape Mining
- Tag extraction using KeyBERT
- Zero-shot classification into categories:
    - Industries (Healthcare, Finance, Retail, etc.)
    - Tech Stack (NLP, Computer Vision, Generative AI, etc.)
    - Use Cases (Chatbots, Fraud Detection, etc.)
    - Business Models (B2B, SaaS, etc.)

4. GenAI Startup Filtering
- Identification of startups with "Generative AI" in their tech stack tags

5. Comparative Analysis
- Visualization of industry distribution
- Tech stack trends comparison
- Business model analysis

# Key Findings
- Identification of top industries and technologies among GenAI startups in both countries
- Comparative analysis highlighting differences between Indian and Australian startup ecosystems
- Potential partnership opportunities based on technological focus areas

# How to Use
- Clone the repository
- Run the python file `python data_extraction.py`
- Install required dependencies listed in the notebook
- Run the Jupyter notebook genai_startups.ipynb sequentially

# The notebook will:
- Preprocess the startup data
- Perform landscape mining
- Generate visual comparisons
- Output filtered GenAI startup lists

# Data Sources
- Indian startups dataset: ``data/indian_startups.csv``
- Australian startups dataset: ``data/australian_startups.csv``
- Web scraped content from startup websites

# Future Enhancements
- Expand data collection to more countries
- Incorporate funding data for deeper analysis
- Add sentiment analysis of startup descriptions
- Develop a recommendation system for partnership opportunities

This project demonstrates my skills in data analysis, natural language processing, and business intelligence applied to the emerging GenAI sector.
