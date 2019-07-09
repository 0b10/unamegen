import cache
import config
import sys
import word

def help_menu():
    print("Usage unamegen [OPTION]...")
    print("Generate a random username from configured sources.\n")
    print("Options")
    print("--debug\t\t\tprint connection errors")
    print("--help:\t\t\tdisplay help")

def main():
    if "--help" in sys.argv:
        help_menu()
        return

    debug = "--debug" in sys.argv

    get_username = word.factory(cache.factory(), config.sources, debug)
    print(get_username())

if __name__ == "__main__":
    main()