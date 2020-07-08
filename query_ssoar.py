import requests
from bs4 import BeautifulSoup as bs
import bibtexparser
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import json
import time

def crawl_ssoar_metadata(id):
    """
    Takes an id (integer) as input and returns a dictionary of metadata for the reference
    entry if the id exists.
    """
    try:
         # specify retry strategy and initialize session
        retry_strategy = Retry(total=3, status_forcelist=[429,500,502,503,504], method_whitelist=["HEAD", "GET", "OPTIONS"])
        adapter = HTTPAdapter(max_retries=retry_strategy)
        http = requests.Session()
        http.mount("https://", adapter)
        http.mount("http://", adapter)

        # specify query
        base_url = "https://www.ssoar.info/ssoar/handle/document/"
        url = base_url + str(id)
        params = {"style": "bibtex"}

        # make a reequest to ssoar
        r = http.get(url, params=params)
        soup = bs(r.text, "lxml")

        # check if the article with the given id exists, return otherwise
        if soup.find("div", {"id": "aspect_general_PageNotFoundTransformer_div_page-not-found"}):
            return

        # if the id exists, get the metadata and return it
        bibtex_html = soup.find("pre", {"id": "citation_content"}).text
        
        bibtex_str = bibtexparser.loads(bibtex_html)
        return bibtex_str.entries[0]

    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
        


def main():
    ids = range(1000000)
    
    with open('ssoar_metadata.txt', 'w') as file:
        for id in ids:
            metadata = crawl_ssoar_metadata(id)
            if metadata != None:
                file.write(json.dumps(metadata))
            time.sleep(1)    

if __name__ == "__main__":
    main()

    