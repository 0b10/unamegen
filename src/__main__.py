import cache
import config
import word

def main():
    get_username = word.factory(cache.factory(), config.sources)
    print(get_username())

if __name__ == "__main__":
    main()