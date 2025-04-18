import json
import pandas as pd
import os
from dotenv import load_dotenv
from serpapi import GoogleSearch

def get_google_jobs(query, location, company, api_key):
    """
    Fetches job listings from Google Jobs using SerpAPI.
    
    Parameters:
        query (str): The job title or keyword to search for.
        location (str): The location where jobs are being searched.
        company (str): The company name to filter job results.
        api_key (str): The API key for SerpAPI.
    
    Returns:
        list: A list of dictionaries containing job details.
    """
    params = {
        "engine": "google_jobs",
        "q": f"{query} {company} {location}", # query
        "api_key": api_key
    }
    
    search = GoogleSearch(params)
    results = search.get_dict()
    jobs = results.get("jobs_results", [])
    
    job_list = []
    for job in jobs:
        # Extract the job posting date if available
        detected_extensions = job.get("detected_extensions", {})
        job_date = detected_extensions.get("posted_at", "N/A")  # Default to "N/A" if date is not available

        job_list.append({
            "Job Title": job.get("title"),
            "Company Name": job.get("company_name"),
            "Location": job.get("location"),
            "Content": job.get("description", ""),
            "Link": job.get("apply_options", [{}])[0].get("link", "N/A"),
            "Date": job_date
        })
    
    return job_list

def fetch_jobs(api_key, csv_filename="data/jobs_data.csv"):
    """
    Fetches job listings for multiple locations and companies, then stores them in a CSV file.
    
    Parameters:
        api_key (str): The API key for SerpAPI.
        csv_filename (str): The name of the CSV file to store job data.
    
    Returns:
        pd.DataFrame: A DataFrame containing the job listings.
    """
    locations = ["India", "Australia"]
    companies = ["TCS", "Infosys", "Wipro", "LTIMindtree", "Cognizant", "Tech Mahindra", "HCLTech"]
    all_jobs = []
    
    # Iterate through each location and company to fetch job listings
    for location in locations:
        for company in companies:
            jobs = get_google_jobs("GenAI", location, company, api_key)
            all_jobs.extend(jobs)
    
    new_jobs_df = pd.DataFrame(all_jobs)
    
    # Check if the CSV file already exists
    if os.path.exists(csv_filename):
        existing_jobs_df = pd.read_csv(csv_filename)
        # Append new job listings while avoiding duplicates based on "Job Title"
        combined_df = pd.concat([existing_jobs_df, new_jobs_df]).drop_duplicates(subset=["Job Title"], keep="first")
    else:
        combined_df = new_jobs_df
    
    # Save the updated job listings to CSV
    combined_df.to_csv(csv_filename, index=False)
    return combined_df

if __name__ == "__main__":
    # Replace with your actual SerpAPI key
    load_dotenv()
    
    API_KEY = os.getenv('SERPAPI')
    jobs_df = fetch_jobs(API_KEY)
    print("Job data updated successfully.")
