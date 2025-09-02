from pathlib import Path


def flags_checker(inputs):
    '''
    Get user Input And config the program for the Scapping
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
                raise ValueError("-l requiert un argument")
            try:
                if config["recursive"] is True:
                    level = int(args[i + 1])
                    config["level"] = level
                    i += 2
                else:
                    print("activate the recursive to use -l")
                    i += 1
            except ValueError:
                raise ValueError(f"Invalid Argument for -l '{args[i+1]}'.")
        elif flag == "-p":
            if i + 1 >= len(args):
                raise ValueError("-p requiert un argument")
            config["path"] = args[i + 1]
            i += 2
        else:
            # l'argument ne commence pas par '-' et que l'URL n'est pas définie
            if not flag.startswith('-') and config["url"] is None:
                config["url"] = flag
                i += 1
            else:
                # C'est soit un flag inconnu, soit une deuxième URL.
                raise ValueError(f"Argument inconnu ou URL multiple : {flag}")
    if config["url"] is None:
        raise ValueError("Missing URL")
    
    try:
        path_obj = Path(config["path"])
        path_obj.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        raise ValueError(f"Need more Permissions'{config['path']}'.")
    except Exception:
        raise ValueError(f"Le chemin '{config['path']}' is not valid.")
    return config
