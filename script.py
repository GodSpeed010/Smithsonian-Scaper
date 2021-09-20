import requests
import bs4
import re

def main():
    url = 'https://transcription.si.edu'
    browse_path = '/browse?filter=owner%3A16'
    
    soup = request_and_parse(url + browse_path)
    #loop through all projects. There are only a few of these.
    for project in soup.find_all('a', class_ = 'browse-project-action-button ir'):
        project_soup = request_and_parse(url + project['href'])
        doc_path, doc_id, page_count = doc_info(project_soup)

        for x in range(doc_id, page_count + 1):
            request_and_parse(url + doc_path)
            str(x).zfill(5)
            break

def doc_info(soup):
    doc_path = soup.find('a', class_ = 'white-box')['href']
    doc_id_re = re.compile(r'_(\d+)')
    doc_id = int(re.search(doc_id_re, doc_path)[1])
    page_count = int(soup.find_all('p', class_ = 'contribution-head')[1].text)
    return doc_path, doc_id, page_count

def request_and_parse(url):
    html = requests.get(url)
    html.raise_for_status()
    soup = bs4.BeautifulSoup(html.text, 'html.parser')
    return soup

main()