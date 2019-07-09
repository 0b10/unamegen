import hashlib
import os
import re

def make_setup_cache(cache_dir):
    def _():
        os.makedirs(cache_dir, exist_ok=True)
        assert os.path.isdir(cache_dir), "The cache directory was not created properly"
    return _

def make_populate_cache(cache_dir):
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

def make_should_cache(cache_dir):
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

def compose_cache(make_hash, make_setup_cache, make_populate_cache, make_should_cache, make_get_cached, cache_dir="/tmp/username_generator", encoding="utf-8"):
    assert cache_dir and isinstance(cache_dir, str), "The cache_dir should be a non-empty string"
    assert make_hash and callable(make_hash), "The make_hash param should be a function"
    assert make_setup_cache and callable(make_setup_cache), "The make_setup_cache param should be a function"
    assert make_populate_cache and callable(make_populate_cache), "The make_populate_cache param should be a function"
    assert make_should_cache and callable(make_should_cache), "The make_should_cache param should be a function"
    assert make_get_cached and callable(make_get_cached), "The make_get_cached param should be a function"
    assert encoding and isinstance(encoding, str), "The encoding param should be a non-empty string"

    make_hash = make_hash(encoding)
    populate_cache = make_populate_cache(cache_dir)
    setup_cache = make_setup_cache(cache_dir)
    should_cache = make_should_cache(cache_dir)
    get_cached = make_get_cached(cache_dir)

    def do_cache_lookup_(url, get):
        assert callable(get), "The get param should be a function"

        hashed_url = make_hash(url)
        if should_cache(hashed_url):
            contents = get()
            setup_cache()
            populate_cache(hashed_url, contents)
            return contents
        else:
            return get_cached(hashed_url)

    return do_cache_lookup_

def factory():
    return compose_cache(make_hash, make_setup_cache, make_populate_cache, make_should_cache, make_get_cached)