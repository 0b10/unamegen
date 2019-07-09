import requests
from requests.exceptions import ConnectionError, ConnectTimeout, HTTPError

def make_wordlist(timeout=5, requests=requests):
    def get(url):
        try:
            return requests.get(url, timeout=timeout).text.split()
        except ( ConnectTimeout, ConnectionError, HTTPError ) as e:
            print(e)
            return False;
    return get


# get = make_wordlist()
# text = get("https://raw.githubusercontent.com/jeanphorn/wordlist/master/usernames.txt")
# print(text)