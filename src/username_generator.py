import requests

def getDictionary(url):
    return requests.get(url).text.split()

text = getDictionary("https://raw.githubusercontent.com/jeanphorn/wordlist/master/usernames.txt")
print(text)