import os
import requests
import hashlib
from requests.exceptions import ConnectionError, ConnectTimeout, HTTPError

def make_wordlist(cache, timeout=5, requests=requests):
    def get(url):
        try:
            return requests.get(url, timeout=timeout).text.split()
        except ( ConnectTimeout, ConnectionError, HTTPError ) as e:
            print(e)
            return False;
    return get

def setup_cache(cache_dir="/tmp/username_generator/"):
    os.makedirs(cache_dir, exist_ok=True)

def populate_cache(target_file, contents, setup_cache, make_hash, cache_dir="/tmp/username_generator"):
    assert target_file and isinstance(target_file, str), "The target_file param is invalid"
    assert contents and isinstance(contents, list), "The contents to cache is invalid"
    assert setup_cache and callable(setup_cache), "The setup_cache param should be a function"
    assert make_hash and callable(make_hash), "The make_hash param should be a function"

    setup_cache(cache_dir)
    hashed_target_name = make_hash(target_file)
    target_file_path = os.path.join(cache_dir, hashed_target_name)

    with open(target_file_path, "w") as f:
        for line in contents:
            f.write(f"{line}\n")

    assert os.path.isfile(target_file_path), "The cache file was not created"

def make_hash(url, encoding="utf-8"):
    assert url and isinstance(url, str), "The url param should be a string"
    assert isinstance(encoding, str), "The encoding param should be a string"

    return hashlib.sha1(bytes(url, encoding=encoding)).hexdigest()



# get = make_wordlist()
# text = get("https://raw.githubusercontent.com/jeanphorn/wordlist/master/usernames.txt")
# print(text)


populate_cache("baz", [1, 2, 3], setup_cache, make_hash)