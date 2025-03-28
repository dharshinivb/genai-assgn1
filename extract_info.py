

import requests
from bs4 import BeautifulSoup
import re
import csv
import google.generativeai as genai
import json
import certifi
import ssl
import time

# Initialize Gemini API client
genai.configure(api_key="AIzaSyB7GeXEe4CFifXthl-if0-cOyv4Od9ryDY")

# Ensure proper SSL handling
ssl_context = ssl.create_default_context(cafile=certifi.where())

def scrape_website(url):
    """Scrapes text content from a given website URL."""
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)  # Keep SSL verification enabled
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup.get_text(separator=" ", strip=True)  # Extract text content
        else:
            print(f"Failed to retrieve {url}: Status Code {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Error scraping {url}: {str(e)}")
        return None

def clean_text(text_content):
    """Cleans the scraped text content."""
    text_content = re.sub(r'\s+', ' ', text_content).strip()  # Remove extra spaces
    text_content = re.sub(r'[^\w\s.,!?-]', '', text_content)  # Remove special characters
    text_content = text_content.replace("```json", "").replace("```", "")  # Remove backticks
    return text_content

def extract_info_with_gemini(text):
    """Extracts structured details from text using Gemini API."""
    prompt = f"""
    Extract the following details from the provided company information in **valid JSON** format:
    {{
        "mission_statement": "Company's mission statement or core values",
        "products_services": "List of major products or services offered",
        "founded": "Year founded and founders",
        "headquarters": "Headquarters location",
        "leadership": "Key executives or leadership team",
        "awards": "Notable awards or recognitions"
    }}
    
    Ensure the response is **valid JSON** format.

    Text: {text}
    """
    
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)

    if response and response.text:
        try:
            json_text = response.text.strip().replace("```json", "").replace("```", "")  # Remove any backticks
            return json.loads(json_text)  # Convert to JSON
        except json.JSONDecodeError as e:
            print("Error parsing Gemini response as JSON. Raw response:", response.text)
            return {}
    else:
        print("Empty response from Gemini API.")
        return {}

# List of companies and their "About" page URLs
companies = {
    "General Motors": "https://www.gm.com/company",
    "Siemens Mobility": "https://www.mobility.siemens.com/global/en/company.html",
    "Alibaba": "https://www.alibaba.com/about",
    "Morgan Stanley": "https://www.morganstanley.com/about-us",
    "Marriott": "https://www.marriott.com/about",
    "BASF": "https://www.basf.com/who-we-are",
    "LinkedIn": "https://about.linkedin.com",
    "Twitter": "https://about.twitter.com",
    "Salesforce": "https://www.salesforce.com/company",
    "eBay": "https://www.ebayinc.com/our-company"
}

# Open CSV file to store extracted data
with open("company_details.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Company", "Mission Statement", "Products/Services", "Founded", "Headquarters", "Leadership", "Awards"])

    for company, url in companies.items():
        print(f"Processing {company}...")

        text_data = scrape_website(url)

        if text_data:
            cleaned_text = clean_text(text_data)
            extracted_info = extract_info_with_gemini(cleaned_text)
            
            # Write structured details into CSV
            writer.writerow([
                company,
                extracted_info.get("mission_statement", "N/A"),
                extracted_info.get("products_services", "N/A"),
                extracted_info.get("founded", "N/A"),
                extracted_info.get("headquarters", "N/A"),
                extracted_info.get("leadership", "N/A"),
                extracted_info.get("awards", "N/A")
            ])
            print(f"Extracted details for {company} saved!\n")
            
            time.sleep(2)  # Avoid hitting API rate limits
        else:
            print(f"Skipping {company} due to no data found.")

print("Extraction completed! Results saved in 'company_details.csv'.")
