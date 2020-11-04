from bs4 import BeautifulSoup
import requests
import re


url = "https://www.informatics.uci.edu"
page = requests.get(url)
soup = BeautifulSoup(page.text, "html.parser")
scripts = soup.find_all('script')
for i in scripts:
    soup.script.extract()
styles = soup.find_all('style')
for i in styles:
    soup.style.extract()
print(soup.html)
word_found = soup.get_text()


# word_found = soup.find_all(text=True)
# words = list()
# for text in word_found:
#     words.extend([word.lower() for word in re.findall("[a-zA-Z]+", text)])
# count = 0
# word_final = set()
# with open("stop_words.txt", 'r') as stopWordsFile:
#     stop_words = stopWordsFile.read()
#     for w in words:
#         if w not in stop_words:
#             word_final.add(w)
#             count += 1


# print(word_found.split())
words = [word.lower() for word in re.findall("[a-zA-Z]+", word_found)]
print(words)
with open("stop_words.txt", 'r') as stopWordsFile:
    stop_words = stopWordsFile.read()
    for w in words:
        if w not in stop_words:
            print(w)

# extracted_text = []
# for t in word_found:
#     if(t.parent.name not in blacklist):
#         extracted_text.append(t)

# word_list = []

# for text in extracted_text:
#     words = [word.lower() for word in re.findall("[a-zA-Z]+", text)]
#     for w in words:
#         word_list.append(w)

# print(word_list)
