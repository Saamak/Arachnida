import sys
from config_init import flags_checker
from lets_scrap import hub


def main():
    try:
        config = flags_checker(sys.argv[1:])
        hub(config)
    except ValueError as e:
        print(f"Value error in arguments: {e}")
        sys.exit(1)
    except IndexError as e:
        print(f"Missing argument: {e}")
        sys.exit(1)
    except Exception:
        print("ERROR: Bad user input or Bad URL")
        sys.exit(1)


if __name__ == "__main__":
    main()