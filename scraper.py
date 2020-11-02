import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import json

high_word_count = 0
page_with_highest_word_count = None

def check_url_domain(url):
    if(re.match(r"(.*\.ics\.uci\.edu.*)" , url)):
        return 'ics.uci.edu'
    elif(re.match(r"(.*\.cs\.uci\.edu.*)"  , url)):
        return 'cs.uci.edu'
    elif(re.match(r"(.*\.informatics\.uci\.edu.*)" , url)):
        return 'informatics.uci.edu'
    elif(re.match(r"(.*\.stat\.uci\.edu.*)" , url)):
        return 'stat.uci.edu'
    elif(re.match(r"(today\.uci\.edu/department/information_computer_sciences.*)" , url)):
        return 'today.uci.edu/department/information_computer_sciences'
    else:
        return None
    
def get_subdomain(domain, url):
    subdomain = url.split(domain)
    if(len(subdomain)>0):
        return subdomain[0] + domain
    else:
        return domain

def count_words_in_page(url, resp):
    #https://matix.io/extract-text-from-webpage-using-beautifulsoup-and-python/
    blacklist = [
    '[document]',
    'noscript',
    'header',
    'html',
    'meta',
    'head', 
    'input',
    'script',
    'button',
    'div',
    'body'
    ]
    text = ""
    if(not resp.raw_response):
        return list()
    soup = BeautifulSoup(resp.raw_response.text, "html.parser")
    extracted_text = []
    for t in soup.find_all(text=True):
        if(t.parent.name not in blacklist):
            extracted_text.append(t)

    word_list = []
    for text in extracted_text:
        word_list.extend([word.lower() for word in re.findall("[a-zA-Z0-9]+", text)])
    return len(word_list)
    
    
def save_page_count(pagecount,pageurl):
    with open("URLdata.json", 'r') as database:
        myFile = json.load(database)
    with open("URLdata.json", "w") as database:
        myFile["longest_page"]["word_count"] = pagecount
        myFile["longest_page"]["url"] = pageurl
        json.dump(myFile, database, indent=4)


def save_url(url):
    #takes the url and saves it to the json database 
    with open("URLdata.json", 'r') as database:
        myFile = json.load(database)

    with open("URLdata.json", "w") as database:
        domain = check_url_domain(url)
        if(domain is None):
            print("save_url error: domain is None url=", url)
            json.dump(myFile, database)
            return -1
        subdomain = get_subdomain(domain, url)
        if(subdomain not in myFile[domain]):  
            myFile[domain][subdomain] = {'pages': [], 'count': 0}
        myFile[domain][subdomain]['pages'].append(url)
        myFile[domain][subdomain]['count']+=1 
        json.dump(myFile, database, indent=4)

def database_contains_url(url):
    
    try:
        with open("URLdata.json", 'r') as database:
            myFile = json.load(database)
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        with open("URLdata.json", 'w') as database:
            format_dict = {
                "longest_page": {"word_count":0, "url": ""},
                "ics.uci.edu": {}, 
                "stat.uci.edu": {},
                "cs.uci.edu": {},
                "informatics.uci.edu": {},
                "today.uci.edu/department/information_computer_sciences": {}
            }
            json.dump(format_dict, database, indent=4)
            return False

    domain = check_url_domain(url)
    subdomain = get_subdomain(domain, url)
    
    if subdomain not in myFile[domain]:
        return False
   
    return url in myFile[domain][subdomain]['pages']

def scraper(url, resp):
    if(database_contains_url(url)):
        return []
    if save_url(url) == -1:
        print("ERROR: url not saved")
        
    word_count = count_words_in_page(url,resp)
    if(word_count > high_word_count):
        high_word_count = word_count
        page_with_highest_word_count = url
        save_page_count(high_word_count,page_with_highest_word_count)
    
    links = extract_next_links(url, resp)
    return links

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
        if(not href or href=="#"):
            continue
        defragmented = defragment_href(href)
        if(is_valid(defragmented) and not database_contains_url(defragmented)):
            extracted_links.append(defragmented)
    return extracted_links


def is_valid(url):
    try:    
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        
        ics_url_match = re.match(r"(.*\.ics\.uci\.edu.*)" , url)
        cs_url_match = re.match(r"(.*\.cs\.uci\.edu.*)"  , url)
        informatics_url_match = re.match(r"(.*\.informatics\.uci\.edu.*)" , url)
        stats_url_match = re.match(r"(.*\.stat\.uci\.edu.*)" , url)
        today_url_match = re.match(r"(today\.uci\.edu/department/information_computer_sciences.*)" , url)
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