from utils import *
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

# Load environment variables
load_dotenv()

# Cached data loading
@st.cache_resource(show_spinner=False)
def load_and_preprocess_data():
    jobs_df = pd.read_csv('data/jobs_data.csv')
    articles_df = pd.read_csv('data/genai_company_articles.csv')
    news_df = pd.read_csv('data/google_news.csv')
    
    jobs_df = clean_company_name(jobs_df)
    jobs_df = preprocess_text(jobs_df, "Content")
    articles_df = preprocess_text(articles_df, "Content")
    news_df = impute_missing_content(news_df)
    news_df = preprocess_text(news_df, 'Content')
    
    return jobs_df, articles_df, news_df

# Cached vector store creation
@st.cache_resource(show_spinner=False)
def get_vector_store():
    jobs_df, articles_df, news_df = load_and_preprocess_data()
    
    news_data = news_df.to_dict(orient='records')
    jobs_data = jobs_df.to_dict(orient='records')
    articles_data = articles_df.to_dict(orient='records')
    
    documents = [str(item)[:1000] for item in news_data + jobs_data + articles_data]
    
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}
    )
    
    return FAISS.from_texts(documents, embeddings)

def main():
    st.title("GenAI Market Intelligence Dashboard")
    st.subheader("Understanding GenAI initiatives and partnership opportunities for Dell")
    
    # Initialize components
    with st.spinner("Loading AI components..."):
        vector_store = get_vector_store()
        retriever = vector_store.as_retriever(search_kwargs={"k":3})  # Reduce from 5 to 3
        
        llm = ChatGroq(
            temperature=0.7,
            model_name="llama-3.3-70b-versatile",
            groq_api_key=os.getenv('GROQ_API_KEY'),
            timeout=30  # Increase timeout if needed
        )
    
    # UI Elements
    companies = ['Tata Consultancy Services', 'Infosys', 'HCLTech', 'Wipro', 
                'Cognizant', 'Tech Mahindra', 'LTIMindtree']
    selected_company = st.selectbox("Select a company for insights:", companies, key='company_select')
    
    regions = ["India", "Australia", "Global"]
    selected_region = st.selectbox("Filter by region:", regions, key='region_select')
    
    analysis_types = {
        "Competitor Landscape Analysis": "...",
        "Market Trend Forecasting": "...",
        "Synergy Identification for Dell": "...",
        "Partnership Opportunity Scoring": "..."
    }
    selected_analysis = st.selectbox("Select analysis type:", list(analysis_types.keys()), key='analysis_select')
    
    if st.button("Generate analysis", key='analyze_btn'):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("Preparing analysis...")
        progress_bar.progress(20)
        
        # Create dynamic prompt based on selection
        base_prompt = analysis_types[selected_analysis]

        prompt_template = ChatPromptTemplate.from_template("""
        As a senior market intelligence analyst specializing in GenAI partnerships, provide insights on:
        {base_prompt}

        Company: {company}
        Region: {region}

        Context from company data:
        {context}

        Structure your response with:
        1. Executive Summary
        2. Key Findings
        3. Strategic Recommendations
        4. Actionable Next Steps
        """)
        
        status_text.text("Creating analysis chains...")
        progress_bar.progress(40)
        
        # Create chains
        document_chain = create_stuff_documents_chain(llm, prompt_template)
        retrieval_chain = create_retrieval_chain(retriever, document_chain)
        
        status_text.text(f"Analyzing {selected_company}...")
        progress_bar.progress(60)
        
        # Correct way to invoke the retrieval chain
        response = retrieval_chain.invoke({
            "input": f"{selected_company} {selected_region} Generative AI",  # This should be a string query
            "company": selected_company,
            "region": selected_region,
            "base_prompt": base_prompt
        })
        
        progress_bar.progress(100)
        status_text.text("Analysis complete!")
        
        # Display results
        st.subheader(f"{selected_analysis} - {selected_company} ({selected_region})")
        st.markdown(response["answer"])
        
        with st.expander("Show supporting data points"):
            st.json(response["context"])

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()