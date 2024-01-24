from bs4 import BeautifulSoup
import requests
import pandas as pd


def extract_job_title(job_elem):
    title_elem = job_elem.a
    return title_elem.get_text(strip=True)


def extract_job_company(job_elem):
    company_elem = job_elem.find("strong")
    return company_elem.get_text(strip=True)


def extract_job_location(job_elem):
    location_elem = job_elem.find("span")
    return location_elem.get_text(strip=True)


def extract_job_link(job_elem):
    link_elem = job_elem.a
    return link_elem.attrs["href"]


def extract_job_description(job_elem):
    description_link = extract_job_link(job_elem)
    description_text = requests.get(description_link).text
    description_soup = BeautifulSoup(description_text, 'lxml')
    description = description_soup.find("div", itemprop="description")
    return description.get_text(strip=True)


def print_to_csv(data, file_name):
    table = pd.DataFrame(data, columns=["title", "company", "location", "description", "link"])
    table.to_csv(file_name + ".csv", index=False, encoding="utf-8")


def get_jobs_for_url(url, data, min_results):
    """
    Scrapes the job website given its url and stores it in the data map.
    Finds at least min_results number of jobs (if available)
    """
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')
    jobs = soup.find_all("div", class_="search-result")

    # Store required characteristics of the job postings to the data object
    for job in jobs:
        title = extract_job_title(job)
        company = extract_job_company(job)
        location = extract_job_location(job)
        description = extract_job_description(job)
        link = extract_job_link(job)

        data['title'].append(title)
        data['company'].append(company)
        data['location'].append(location)
        data['description'].append(description)
        data['link'].append(link)

    # Continue search onto next page if more jobs are needed
    next_page_elem = soup.find("a", class_="govuk-link pager-next")
    while (next_page_elem is not None) and (len(data['title']) < min_results):
        next_page_url = next_page_elem.attrs["href"]
        get_jobs_for_url(next_page_url, data, min_results)


def extract(url, file_name, min_results):
    """
    Initialises data, calls the actual scraping function and then handles printing the data to a new csv file
    """

    # Data ~= Format for the extracted data. Stores the list of information per column
    data = {
        'title': [],
        'company': [],
        'location': [],
        'description': [],
        'link': []
    }
    get_jobs_for_url(url, data, min_results)
    print("No. of jobs found: " + str(len(data['title'])))
    print_to_csv(data, file_name)


if __name__ == "__main__":
    """
    Pass the url of the |https://findajob.dwp.gov.uk/| page to scrape, along with the desired name of the output csv 
    file and min no. of jobs needed, to the EXTRACT function
    """
    nurse_url = "https://findajob.dwp.gov.uk/search?q=nurse&w="
    extract(url=nurse_url, file_name="nurse", min_results=50)
