import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import json
from hashlib import sha224

global high_word_count, page_with_highest_word_count, word_frequency
high_word_count = 0
page_with_highest_word_count = ""
word_frequency = dict()
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

def computeWordFrequencies(token_list): 
    local_pages_word_frequencies = dict()
    for token in token_list: 
        if token in local_pages_word_frequencies:
            local_pages_word_frequencies[token]+=1
        else:
            local_pages_word_frequencies[token]=1
    for token in token_list: 
        if token in word_frequency:
            word_frequency[token]+=1
        else:
            word_frequency[token]=1
    return local_pages_word_frequencies

def simhash(word_frequency_dict):
    '''takes in the word frequency dict and output a binary vector for the ID of the website'''
    bin_length = 256
    total_vector = [0] * bin_length
    for word in word_frequency_dict.keys():
        one_vector = list()
        hash_val = bin(int(sha224(word.encode("utf-8")).hexdigest(), 16))[2:(bin_length+2)]
        hash_len = len(hash_val)
        
        if (hash_len<bin_length):
            difference = bin_length - hash_len
            hash_val = ("0" * difference) + hash_val
        for binary in hash_val:
            if binary == "0":
                one_vector.append(-1*word_frequency_dict[word])
            else:
                one_vector.append(word_frequency_dict[word])
        
        for indx in range(len(total_vector)):
            total_vector[indx] += one_vector[indx]
    binary_str = ""
    for i in total_vector:
        if i>0:
            binary_str+="1"
        else:
            binary_str+="0"   
            
    return binary_str



    
def get_words_in_page(url, resp):
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
    stopWords = 
    text = ""
    if(not resp.raw_response):
        return list()
    soup = BeautifulSoup(resp.raw_response.text, "html.parser")
    extracted_text = []
    for t in soup.find_all(text=True):
        if(t.parent.name not in blacklist):
            extracted_text.append(t)

    word_list = []
    with open("stop_words.txt", 'r') as stop_words:
        for text in extracted_text:
            word_list.extend([word.lower() for word in re.findall("[a-zA-Z0-9]+", text) if not in stop_words])
    print(word_list)

    return word_list


def check_duplicate_page(word_frequency_dict):
    fingerprint = simhash(word_frequency_dict)
    with open("URLdata.json", 'r') as database:
        myFile = json.load(database)
    with open("URLdata.json", "w") as database:
        visited_websites = myFile["visited_website"]
        threshold = 0.9
        for each_website in visited_websites:
            total = 0
            xorval = bin(int(fingerprint, 2)^int(each_website, 2))[2:]
            if (len(xorval)<len(fingerprint)):
                difference = len(fingerprint)-len(xorval)
                xorval = ("0" * difference) + xorval
            for i in xorval:
                # we are forced to use xor but not xnor in this case
                # counting 0 means two digits are the same in xor
                if i == "0":
                    total += 1
            similarity = float(total)/len(fingerprint)
            if similarity > threshold:
                myFile["visited_website"][fingerprint] = fingerprint
                json.dump(myFile, database, indent=4)
                return True
        myFile["visited_website"][fingerprint] = fingerprint
        json.dump(myFile, database, indent=4)
        return False
        
    
    

def update_word_frequencies_in_database():
    with open("URLdata.json", 'r') as database:
        myFile = json.load(database)
    with open("URLdata.json", "w") as database:
        top50word = sorted(word_frequency.items(), key = lambda x: x[1], reverse=True)[:50]
        myFile["top_50_words"] = top50word
        json.dump(myFile, database, indent=4)
    
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
        myFile["number_of_unique_pages"]+=1 
        json.dump(myFile, database, indent=4)

def database_contains_url(url):
    
    try:
        with open("URLdata.json", 'r') as database:
            myFile = json.load(database)
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        with open("URLdata.json", 'w') as database:
            format_dict = {
                "number_of_unique_pages": 0,
                "longest_page": {"word_count":0, "url": ""},
                "visited_website": {},
                "top_50_words": [],
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
    global high_word_count, page_with_highest_word_count, word_frequency
    if(resp.status >= 400 and resp.status < 600):
        return []

    if( resp.raw_response == None or len(resp.raw_response.text) < 1):
       return []

    if(database_contains_url(url)):
        return []
    
    if save_url(url) == -1:
        print("ERROR: url not saved")
        return []
        
    word_list = get_words_in_page(url,resp)
    word_count = len(word_list)
    word_frequency_dict = computeWordFrequencies(word_list)
    if(len(word_frequency_dict)<50):
        return []
    if (check_duplicate_page(word_frequency_dict)):
        return []
    update_word_frequencies_in_database()
    
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
        if(is_valid(href) and not database_contains_url(defragmented)):
            extracted_links.append(defragmented)
    return extracted_links


def is_valid(url):
    try:    
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        not_pdf = not re.match(r"(.*\/pdf\/.*)" , parsed.path)
        ics_url_match = re.match(r"(.*\.ics\.uci\.edu.*)" , parsed.netloc)
        cs_url_match = re.match(r"(.*\.cs\.uci\.edu.*)"  , parsed.netloc)
        informatics_url_match = re.match(r"(.*\.informatics\.uci\.edu.*)" , parsed.netloc)
        stats_url_match = re.match(r"(.*\.stat\.uci\.edu.*)" , parsed.netloc)
        today_url_match = re.match(r"(today\.uci\.edu/department/information_computer_sciences.*)" , parsed.netloc)

        url_match = (cs_url_match or ics_url_match or informatics_url_match or stats_url_match or today_url_match) and not_pdf
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
