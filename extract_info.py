import requests
from bs4 import BeautifulSoup
import re
import csv
from google import genai

# Initialize Gemini API client
client = genai.Client(api_key="AIzaSyB7GeXEe4CFifXthl-if0-cOyv4Od9ryDY")

def scrape_website(url):
    """Scrapes text content from a given website URL."""
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup.get_text(separator=" ", strip=True)  # Extract text content
        else:
            print(f"Failed to retrieve {url}: Status Code {response.status_code}")
            return None
    except Exception as e:
        print(f"Error scraping {url}: {str(e)}")
        return None
def search_company_info(company):
    """Searches Google for the company's about page or relevant information."""
    query = f"{company} company about site:linkedin.com OR site:wikipedia.org OR site:crunchbase.com"
    try:
        search_results = list(search(query, num=1, stop=1, pause=2))
        if search_results:
            return scrape_website(search_results[0])
    except Exception as e:
        print(f"Google search failed for {company}: {str(e)}")
    return None
def clean_text(text_content):
    """Cleans the scraped text content."""
    text_content = re.sub(r'\s+', ' ', text_content)  # Remove extra spaces
    text_content = re.sub(r'[^\w\s.,!?-]', '', text_content)  # Remove special characters
    return text_content.strip()

def extract_info_with_gemini(text):
    """Extracts structured details from text using Gemini API."""
    prompt = f"""
    Extract the following details from the provided company information:
    - Mission statement or core values
    - Products or services offered
    - Founding year and founders
    - Headquarters location
    - Key executives or leadership
    - Notable awards or recognitions

    Text: {text}

    Provide the extracted details in a structured format.
    """
    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
    return response.text

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

        if not text_data:
            print(f"Scraping failed for {company}. Searching on Google...")
            text_data = search_company_info(company)

        if text_data:
            cleaned_text = clean_text(text_data)
            extracted_info = extract_info_with_gemini(cleaned_text)
            writer.writerow([company, extracted_info])
            print(f"Extracted details for {company} saved!\n")
        else:
            print(f"Skipping {company} due to no data found.")


print("Extraction completed! Results saved in 'company_details.csv'.")

# import requests
# from bs4 import BeautifulSoup
# import re
# import csv
# import google.generativeai as genai
# from googlesearch import search

# # Initialize Gemini API client
# genai.configure(api_key="AIzaSyB7GeXEe4CFifXthl-if0-cOyv4Od9ryDY")


# def scrape_website(url):
#     """Scrapes text content from a given website URL."""
#     headers = {"User-Agent": "Mozilla/5.0"}
#     try:
#         response = requests.get(url, headers=headers, timeout=10)
#         if response.status_code == 200:
#             soup = BeautifulSoup(response.text, 'html.parser')
#             return soup.get_text(separator=" ", strip=True)  # Extract text content
#         else:
#             print(f"Failed to retrieve {url}: Status Code {response.status_code}")
#             return None
#     except Exception as e:
#         print(f"Error scraping {url}: {str(e)}")
#         return None


# def clean_text(text_content):
#     """Cleans the scraped text content."""
#     text_content = re.sub(r'\s+', ' ', text_content)  # Remove extra spaces
#     text_content = re.sub(r'[^\w\s.,!?-]', '', text_content)  # Remove special characters
#     return text_content.strip()


# def extract_info_with_gemini(text):
#     """Extracts structured details from text using Gemini API."""
#     prompt = f"""
#     Extract the following details from the provided company information:
#     - Mission statement or core values
#     - Products or services offered
#     - Founding year and founders
#     - Headquarters location
#     - Key executives or leadership
#     - Notable awards or recognitions

#     Text: {text}
    
#     Provide the extracted details in a structured format.
#     """
#     model = genai.GenerativeModel("gemini-pro")
#     response = model.generate_content(prompt)
#     return response.text if response else "No information found"


# def search_company_info(company):
#     """Searches Google for the company's about page or relevant information."""
#     query = f"{company} company about site:linkedin.com OR site:wikipedia.org OR site:crunchbase.com"
#     try:
#         search_results = list(search(query, num=1, stop=1, pause=2))
#         if search_results:
#             return scrape_website(search_results[0])
#     except Exception as e:
#         print(f"Google search failed for {company}: {str(e)}")
#     return None


# # List of companies and their "About" page URLs
# companies = {
#     "General Motors": "https://www.gm.com/company",
#     "Siemens Mobility": "https://www.mobility.siemens.com/global/en/company.html",
#     "Alibaba": "https://www.alibaba.com/about",
#     "Morgan Stanley": "https://www.morganstanley.com/about-us",
#     "Marriott": "https://www.marriott.com/about",
#     "BASF": "https://www.basf.com/who-we-are",
#     "LinkedIn": "https://about.linkedin.com",
#     "Twitter": "https://about.twitter.com",
#     "Salesforce": "https://www.salesforce.com/company",
#     "eBay": "https://www.ebayinc.com/our-company"
# }

# # Open CSV file to store extracted data
# with open("company_details.csv", "w", newline="", encoding="utf-8") as file:
#     writer = csv.writer(file)
#     writer.writerow(["Company", "Mission Statement", "Products/Services", "Founded", "Headquarters", "Leadership", "Awards"])

#     for company, url in companies.items():
#         print(f"Processing {company}...")
#         text_data = scrape_website(url)

#         if not text_data:
#             print(f"Scraping failed for {company}. Searching on Google...")
#             text_data = search_company_info(company)

#         if text_data:
#             cleaned_text = clean_text(text_data)
#             extracted_info = extract_info_with_gemini(cleaned_text)
#             writer.writerow([company, extracted_info])
#             print(f"Extracted details for {company} saved!\n")
#         else:
#             print(f"Skipping {company} due to no data found.")

# print("Extraction completed! Results saved in 'company_details.csv'.")
