import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import json
from hashlib import sha224
def is_valid(url):
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        not_pdf = not re.match(r"(.*\/pdf\/.*)", parsed.path)
        ics_url_match = re.match(r"(.*\.ics\.uci\.edu.*)", parsed.netloc)
        cs_url_match = re.match(r"(.*\.cs\.uci\.edu.*)", parsed.netloc)
        informatics_url_match = re.match(
            r"(.*\.informatics\.uci\.edu.*)", parsed.netloc)
        stats_url_match = re.match(r"(.*\.stat\.uci\.edu.*)", parsed.netloc)
        today_url_match = re.match(
            r"(today\.uci\.edu/department/information_computer_sciences.*)", parsed.netloc)
        print(parsed.query.lower())
        url_match = (
            cs_url_match or ics_url_match or informatics_url_match or stats_url_match or today_url_match) and not_pdf
        file_type_match = not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|ppsx|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz|r|c|py|cpp|Z)$", url.lower())
        query_file_type_match = not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|ppsx|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz|r|c|py|cpp|Z)$", parsed.query.lower())
        path_file_type_match = not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|ppsx|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz|r|c|py|cpp|Z)$", parsed.path.lower())
          
          
        return url_match and file_type_match and query_file_type_match and path_file_type_match

    except TypeError:
        print("TypeError for ", parsed)

print(is_valid('http://sli.ics.uci.edu/Pubs/Pubs#hi.pdf'))
#http://sli.ics.uci.edu/Pubs/Pubs?action=download&upname=uai08.pdf