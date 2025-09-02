import sys
from config_init import flags_checker
from lets_scrap import hub


def main():
    try:
        config = flags_checker(sys.argv[1:])
        hub(config)
    except ValueError as e:
        print(f"Erreur de valeur dans les arguments : {e}")
    except IndexError as e:
        print(f"Argument manquant : {e}")
    except Exception:
        print("ERROR USER INPUT")
        sys.exit(1)


if __name__ == "__main__":
    main()