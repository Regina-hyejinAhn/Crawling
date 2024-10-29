from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import requests
from PyPDF2 import PdfReader
import datetime as dt

def extract_pdf_title(file_path):
    try:
        reader = PdfReader(file_path)
        # Extract the title from the first page, or use document info if available
        first_page = reader.pages[0]
        text = first_page.extract_text()
        if text:
            # Get the first line as the title, with some basic cleanup
            title = text.split('\n')[0].strip()[:100]
            if title == "1":
                title = text.split('\n')[1].strip()[:100]
            return title if title else "untitled"
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return "untitled"

def download_pdfs():
    icloud_folder = os.path.expanduser("~/Library/Mobile Documents/com~apple~CloudDocs/0a.AI_PhD_2024-/arxiv_pdfs")
    date = dt.date.today().strftime("%Y%m%d")

    driver = webdriver.Chrome()  # Ensure you have the correct ChromeDriver installed
    driver.get("https://arxiv.org/list/cs.AI/recent")

    # Wait for the page to load fully
    time.sleep(5)

    # Create a folder to save the PDFs
    if not os.path.exists(f"{icloud_folder}"):
        os.makedirs(f"{icloud_folder}")

    # Find all PDF links
    papers = driver.find_elements(By.XPATH, '//a[@title="Download PDF"]')
    idx = 1
    for paper in papers:
        pdf_url = paper.get_attribute("href")
        file_path = f"{icloud_folder}/temp.pdf"  # Temporary filename

        try:
            # Download and save each PDF temporarily
            response = requests.get(pdf_url)
            with open(file_path, 'wb') as f:
                f.write(response.content)

            # Extract title from the saved PDF
            title = extract_pdf_title(file_path)

            pdf_list = os.listdir(icloud_folder)
            if any(title in pdf for pdf in pdf_list):
                continue
            else:
                idx += 1
                safe_title = "".join([c for c in title if c.isalpha() or c in ' _-']).rstrip()
                safe_title = f'{safe_title}_{date}'

                # Rename the file with the extracted title
                new_file_path = f"{icloud_folder}/{safe_title}.pdf"
                os.rename(file_path, new_file_path)
                # print(f"Saved: {new_file_path}")
        except Exception as e:
            print(f"Failed to download {pdf_url}: {e}")

    print(f'{idx} files downloaded')
    driver.quit()

if __name__ == "__main__":
    download_pdfs()