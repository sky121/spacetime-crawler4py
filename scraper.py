import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import json



def save_url(url):
    #takes the url and saves it to the json database 
    print(url)
    with open("URLdata.json", "w+") as outfile:
        myFile = {"test":" my test"}
        json.dump(myFile, outfile)


def scraper(url, resp):
    save_url(url)
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def defragment_href(href):
    defragmented = href.split('#')[0]
    return defragmented

def extract_next_links(url, resp):
    # Implementation requred.
    # Based on https://www.tutorialspoint.com/beautiful_soup/beautiful_soup_quick_guide.htm
    if(not resp.raw_response):
        return list()
    soup = BeautifulSoup(resp.raw_response.text, "html.parser")
    extracted_links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if(not href):
            continue
        defragmented = defragment_href(href)
        #Check Database for URL
            #If in Database -> skip
            #else Append and Count
        extracted_links.append(defragmented)
    return extracted_links


def is_valid(url):
    try:    
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        
        ics_url_match = re.match(r"(.*\.ics\.uci\.edu/.*)" , url)
        cs_url_match = re.match(r"(.*\.cs\.uci\.edu/.*)"  , url)
        informatics_url_match = re.match(r"(.*\.informatics\.uci\.edu/.*)" , url)
        stats_url_match = re.match(r"(.*\.stat\.uci\.edu/.*)" , url)
        today_url_match = re.match(r"(today\.uci\.edu/department/information_computer_sciences/.*)" , url)
        url_match = cs_url_match or ics_url_match or informatics_url_match or stats_url_match or today_url_match
        file_type_match = not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())
        return url_match and file_type_match

    except TypeError:
        print ("TypeError for ", parsed)
        raise