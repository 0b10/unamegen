import requests
from requests.exceptions import ConnectionError, ConnectTimeout, HTTPError

import cache

def config_get_wordlist(do_cache_lookup, timeout=5):
    assert (isinstance(timeout, int) or isinstance(timeout, float)) and timeout > 0, "Timout should be a number > 0"
    assert callable(do_cache_lookup), "The do_cache_lookup param should be a function"

    def get(url):
        assert url and isinstance(url, str), "The url param should be a non-empty string"

        try:
            return do_cache_lookup(url, lambda: requests.get(url, timeout=timeout).text.split())
        except ( ConnectTimeout, ConnectionError, HTTPError ) as e:
            return False, e

    return get

url = "https://raw.githubusercontent.com/jeanphorn/wordlist/master/usernames.txt"

do_cache_lookup = cache.factory()
get_wordlist = config_get_wordlist(do_cache_lookup)
print(get_wordlist(url))

# text = get("https://raw.githubusercontent.com/jeanphorn/wordlist/master/usernames.txt")
# print(text)


# populate_cache("baz", [1, 2, 3], setup_cache, make_hash)
# print(should_cache("baz", make_hash))
# do_cache("tesddwqiiat22", [1, 2, 3])!