# Importing libraries
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import re
import json


# Function to check company name
def clean_company_name(df):
    # List of company names
    company_keywords = ['Tata Consultancy Services', 'Infosys', 'Wipro', 'Tech Mahindra', 'Cognizant', 'HCLTech', 'LTIMindtree']

    def extract_company(name):
        for company in company_keywords:
            if company.lower() in name.lower():
                return company
        return None
    
    # Apply function to extract required companies
    df['Company Name'] = df['Company Name'].apply(extract_company)

    # Drop rows where company name is None
    df = df.dropna(subset=['Company Name']).reset_index(drop=True)

    return df


# Function to perform text preprocessing on the descriptions
def preprocess_text(df, column_name):
    nltk.download('stopwords')
    nltk.download('punkt')
    nltk.download('wordnet')

    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()

    def clean_text(text):
        if pd.isna(text):
            return ""
        
        text = text.lower()
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text) # remove special characters
        text = re.sub(r'\s+', ' ', text).strip() # remove extra spaces
        words = word_tokenize(text)
        words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]

        return ' '.join(words)
    
    df['column_name'] =  df[column_name].apply(clean_text)

    return df

# Imputing NaN values in Content column with value in Headline column
def impute_missing_content(df):
    df['Content'] = df['Content'].fillna(df['Headline'])
    return df

# Function to Convert all the datasets to json format
def df_to_json(df):
    return json.loads(df.to_json(orient='records'))