import os
import requests
import hashlib
import re
from requests.exceptions import ConnectionError, ConnectTimeout, HTTPError

def config_get_wordlist(do_cache, timeout=5):
    assert (isinstance(timeout, int) or isinstance(timeout, float)) and timeout > 0, "Timout should be a number > 0"
    assert callable(do_cache), "The do_cache param should be a function"

    def get(url):
        assert url and isinstance(url, str), "The url param should be a non-empty string"

        try:
            word_list = requests.get(url, timeout=timeout).text.split()
            do_cache(url, word_list)
        except ( ConnectTimeout, ConnectionError, HTTPError ) as e:
            return False, e
    return get

def setup_cache(cache_dir):
    def _():
        os.makedirs(cache_dir, exist_ok=True)
        assert os.path.isdir(cache_dir), "The cache directory was not created properly"
    return _

def populate_cache(cache_dir):
    def _(target_name, contents):
        assert target_name and isinstance(target_name, str), "The target_name param is invalid"
        assert contents and isinstance(contents, list), "The contents to cache is invalid"

        target_file_path = os.path.join(cache_dir, target_name)

        with open(target_file_path, "w") as f:
            for line in contents:
                f.write(f"{line}\n")

        assert os.path.isfile(target_file_path), "The cache file was not created"
        assert os.stat(target_file_path).st_size > 0, "The created cache file is empty"

    return _

def should_cache(cache_dir):
    def _(target_name):
        assert target_name and isinstance(target_name, str), "The target_name param should be a non-empty string"

        target = os.path.join(cache_dir, target_name)
        return not (os.path.exists(target) and os.path.isfile(target))

    return _

def make_hash(encoding):
    def _(url):
        assert url and isinstance(url, str), "The url param should be a string"

        result = hashlib.sha1(bytes(url, encoding=encoding)).hexdigest()

        assert isinstance(result, str), "The hashed file name result should be a string"
        assert re.fullmatch("^[0-9a-f]{40}$", result), f"The hash result does not match regex for sha1: {result}"

        return result

    return _

def make_get_cached(cache_dir):
    def get_cached(target_name):
        target_path = os.path.join(cache_dir, target_name)
        with open(target_path, "r") as f:
            result = f.read().split("\n")[:-1]

        assert result and isinstance(result, list), "The result from a cache read should be a non-empty list"
        return result
    return get_cached

def compose_cache(make_hash, setup_cache, populate_cache, should_cache, make_get_cached, cache_dir="/tmp/username_generator", encoding="utf-8"):
    assert cache_dir and isinstance(cache_dir, str), "The cache_dir should be a non-empty string"
    assert make_hash and callable(make_hash), "The make_hash param should be a function"
    assert setup_cache and callable(setup_cache), "The setup_cache param should be a function"
    assert populate_cache and callable(populate_cache), "The populate_cache param should be a function"
    assert should_cache and callable(should_cache), "The should_cache param should be a function"
    assert make_get_cached and callable(make_get_cached), "The make_get_cached param should be a function"
    assert encoding and isinstance(encoding, str), "The encoding param should be a non-empty string"

    make_hash = make_hash(encoding)
    populate_cache = populate_cache(cache_dir)
    setup_cache = setup_cache(cache_dir)
    should_cache = should_cache(cache_dir)
    get_cached = make_get_cached(cache_dir)

    def do_cache_(url, contents):
        hashed_url = make_hash(url)
        if should_cache(hashed_url):
            setup_cache()
            populate_cache(hashed_url, contents)

    def get_cached_(url):
        hashed_url = make_hash(url)
        if should_cache(hashed_url):
            return False # No cached
        else:
            return get_cached(hashed_url)

    return do_cache_, get_cached_

url = "https://raw.githubusercontent.com/jeanphorn/wordlist/master/usernames.txt"

do_cache, get_cached = compose_cache(make_hash, setup_cache, populate_cache, should_cache, make_get_cached)
get_wordlist = config_get_wordlist(do_cache)
get_wordlist(url)
print(get_cached(url))

# text = get("https://raw.githubusercontent.com/jeanphorn/wordlist/master/usernames.txt")
# print(text)


# populate_cache("baz", [1, 2, 3], setup_cache, make_hash)
# print(should_cache("baz", make_hash))
# do_cache("tesddwqiiat22", [1, 2, 3])