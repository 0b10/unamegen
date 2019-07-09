import requests
from requests.exceptions import ConnectionError, ConnectTimeout, HTTPError
from random import randint

def make_get_wordlist(do_cache_lookup, timeout=5):
    assert (isinstance(timeout, int) or isinstance(timeout, float)) and timeout > 0, "Timout should be a number > 0"
    assert callable(do_cache_lookup), "The do_cache_lookup param should be a function"

    def get(url):
        assert url and isinstance(url, str), "The url param should be a non-empty string"

        try:
            return do_cache_lookup(url, lambda: requests.get(url, timeout=timeout).text.split()), None
        except ( ConnectTimeout, ConnectionError, HTTPError ) as e:
            return False, e

    return get

def make_get_word(sources, get_wordlist):
    assert sources and isinstance(sources, list), "The sources param must be a non-empty list"
    assert callable(get_wordlist), "The get_wordlist param should be a function"

    def _():
        for source in sources:
            word_list, error = get_wordlist(source)
            if not word_list:
                print(error)
            else:
                return word_list[randint(0, len(word_list) - 1)]
                break

    return _

def factory(do_cache_lookup, sources):
    assert callable(do_cache_lookup), "The do_cache_lookup param should be a function"
    assert sources and isinstance(sources, list), "The sources param should be a non-empty list"

    get_wordlist = make_get_wordlist(do_cache_lookup)
    return make_get_word(sources, get_wordlist)