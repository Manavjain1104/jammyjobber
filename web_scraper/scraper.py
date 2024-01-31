from bs4 import BeautifulSoup
import requests
import pandas as pd


def extract_job_title(job_elem):
    title_elem = job_elem.h3
    return title_elem.get_text(strip=True)


def extract_job_company(job_elem):
    company_elem = job_elem.find("div", class_="search-results-job-box-department")
    return company_elem.get_text(strip=True)


def extract_job_location(job_elem):
    company_elem = job_elem.find("div", class_="search-results-job-box-location")
    return company_elem.get_text(strip=True)


def extract_job_description(job_elem):
    description_elem = job_elem.h3.find("a")
    description_link = description_elem.attrs["href"]

    description_text = requests.get(description_link).text
    description_soup = BeautifulSoup(description_text, "lxml")
    main_text = description_soup.find("div", class_="vac_display_panel_main")
    text_elems = main_text.find_all("div", class_="vac_display_field_value")
    description = "".join(elem.text.strip() for elem in text_elems)
    return description


def print_to_csv(data, file_name):
    table = pd.DataFrame(data, columns=["title", "company", "location", "description"])
    table.to_csv(file_name + ".csv", index=False, encoding="utf-8")


def get_jobs_for_url(url, data, min_results):
    """
    Scrapes the job website given its url and stores it in the data map.
    Finds at least min_results number of jobs (if available)
    """
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, "lxml")

    # Store required characteristics of the job posting to the data object
    jobs = soup.find_all("li", class_="search-results-job-box")
    for job in jobs:
        title = extract_job_title(job)
        company = extract_job_company(job)
        location = extract_job_location(job)
        description = extract_job_description(job)

        data["title"].append(title)
        data["company"].append(company)
        data["location"].append(location)
        data["description"].append(description)

    # Continue search onto next page if more jobs are needed
    next_page_elem = soup.find("a", title="Go to next search results page")
    while (next_page_elem is not None) and (len(data["title"]) < min_results):
        next_page_url = next_page_elem.attrs["href"]
        get_jobs_for_url(next_page_url, data, min_results)


def extract(url, file_name, min_results):
    """
    Initialises data, calls the actual scraping function and then handles printing the data to a new csv file
    """

    # Data ~= Format for the extracted data. Stores the list of information per column
    data = {"title": [], "company": [], "location": [], "description": []}
    get_jobs_for_url(url, data, min_results)
    print("No. of jobs found: " + str(len(data["title"])))
    print_to_csv(data, file_name)


if __name__ == "__main__":
    """
    Pass the url of the |civilservicejobs| page to scrape, along with the desired name of the output csv file and
    min no. of jobs needed, to the EXTRACT function
    """
    computer_url = (
        "https://www.civilservicejobs.service.gov.uk/csr/index.cgi?SID"
        "=cGFnZWNsYXNzPVNlYXJjaCZwYWdlYWN0aW9uPXNlYXJjaGNvbnRleHQmY29udGV4dGlkPTY2MDA3NTg5Jm93bmVyPTUwNzAwMDAmb3duZXJ0eXBlPWZhaXImcmVxc2lnPTE3MDYwMTY3MTktNWY2NTM0MTM3ZWUwZGRiOGY3NjJiOTk0NDE4ZDE0MzU4ZDBkNTMzMw=="
    )
    extract(computer_url, "computer", min_results=30)
