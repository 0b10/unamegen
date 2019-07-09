import cache
import config
import word

do_cache_lookup = cache.factory()
get_username = word.factory(do_cache_lookup, config.sources)

print(get_username())
