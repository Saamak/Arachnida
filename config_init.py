from pathlib import Path


def flags_checker(inputs):
    '''
    Parses user input to configure the scraping process.
    '''
    i = 0
    args = inputs[:]
    config = {
        "recursive": False,
        "level": 5,
        "path": "./data/",
        "url": None
    }
    while i < len(args):
        flag = args[i]
        if flag == "-r":
            config["recursive"] = True
            i += 1
        elif flag == "-l":
            if i + 1 >= len(args):
                raise ValueError("-l requires an argument")
            try:
                if config["recursive"] is True:
                    level = int(args[i + 1])
                    config["level"] = level
                    i += 2
                else:
                    print("activate recursive to use -l")
                    i += 1
            except ValueError:
                raise ValueError(f"Invalid Argument for -l '{args[i+1]}'.")
        elif flag == "-p":
            if i + 1 >= len(args):
                raise ValueError("-p requires an argument")
            config["path"] = args[i + 1]
            i += 2
        else:
            # The argument does not start with '-' and the URL is not defined
            if not flag.startswith('-') and config["url"] is None:
                config["url"] = flag
                i += 1
            else:
                # It's either an unknown flag or a second URL.
                raise ValueError(f"Unknown argument or multiple URLs: {flag}")
    if config["url"] is None:
        raise ValueError("Missing URL")
    try:
        path_obj = Path(config["path"])
        path_obj.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        raise ValueError(f"Need more Permissions for '{config['path']}'.")
    except Exception:
        raise ValueError(f"The path '{config['path']}' is not valid.")
    return config
