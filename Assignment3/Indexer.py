import re
from os import walk
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import json
from hashlib import sha224
import pickle

def get_tokens_in_page(content):
    #gets the list of tokens in the website content
    soup = BeautifulSoup(content, "html.parser")
    scripts = soup.find_all('script')
    for i in scripts:
        soup.script.extract()
    styles = soup.find_all('style')
    for i in styles:
        soup.style.extract()
    tokens_found = soup.get_text()
    tokens = [token.lower() for token in re.findall("[a-zA-Z]+", tokens_found)]
    return tokens

def get_hash(url):
    return sha224(url.encode("utf-8")).hexdigest()

def initialize_database():
    filename = "index"
    with open(filename, 'wb') as database:
        pickle.dump({"num_tokens":0}, database)


def store_index(index):
    filename = "index"
    with open(filename, 'rb') as database:
        old_index = pickle.load(database)
    with open(filename, 'wb') as database:
        for token, docs in index.items():
            if token == "num_tokens":
                continue
            if token in old_index:
                old_index[token]["num_docs"]+=docs["num_docs"]
                for doc_ID, doc_dict in docs.items():
                    if doc_ID == "num_docs":
                        continue
                    old_index[token][doc_ID] = doc_dict
            else:
                old_index[token] = docs
                old_index["num_tokens"] += 1
        
        pickle.dump(old_index, database)  

def main():
    initialize_database()
    index = {"num_tokens":0}
    num_docs = 0
    num_tokens = 0
    website_id = 0
    for (dirpath, dirnames, filenames) in walk('./DEV'):
        for file_name in filenames: #looping through files in the directory DEV
            num_docs+=1
            in_file = open(f"{dirpath}/{file_name}", "r")
            website = json.load(in_file) #load the json of each file which contains {url, content, encoding}
            tokens = get_tokens_in_page(website["content"]) # tokens are the list of words in the website loaded
            website_id += 1 # get_hash(website['url'])
            for token in tokens: 
                if token in index: # If the token is already in the index just add 1 
                    if website_id in index[token]: # if the website is inside the index, we increment the frequency of the token for that website
                        index[token][website_id]["tf_idf"] += 1
                    else: # if website is not inside the index, we add the website and initialize tf_idf as 1 for the current token
                        index[token]["num_docs"]+=1
                        index[token][website_id] = {"tf_idf": 1}
                else:
                    index[token] = { # If the specific token is NOT in the index, initialize the token
                        "num_docs":1, 
                        website_id: {
                            "tf_idf": 1
                        }
                    }
                    index["num_tokens"] += 1
                    num_tokens+=1
        store_index(index)  
        index.clear()
        index = {"num_tokens":0}
        #print(num_docs, num_tokens)
       
    print("number of documents: ",num_docs)
    #print(num_tokens)
    #store_index(index)  
    with open('index', 'rb') as database:
        index = pickle.load(database)
        print("number of tokens: ",index['num_tokens'])

    
main() 

