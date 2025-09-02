from pathlib import Path

def flags_checker(inputs):
    print(inputs)
    i = 0
    args = inputs[:]
    config = {
        "recursive" : False,
        "level" : 5,
        "path" : "./data/",
        "url" : None
    }
    while i < len(args):
        flag = args[i]
        if flag == "-r":
            config["recursive"] = True
            print("RECURSIVE ACTIVATED")
            i += 1
        elif flag == "-l":
            if i + 1 >= len(args):
                raise ValueError("-l requiert un argument")
            try:
                if config["recursive"] == True:
                    level = int(args[i + 1])
                    config["level"] = level
                    i += 2
                else:
                    print("activate the recursive to use -l")
                    i += 1
            except ValueError:
                raise ValueError(f"L'argument pour -l doit être un nombre, mais a reçu '{args[i+1]}'.")
        elif flag == "-p":
            if i + 1 >= len(args):
                raise ValueError("-p requiert un argument")
            config["path"] = args[i + 1]
            i += 2
        else:
            # Si l'argument ne commence pas par '-' et que l'URL n'est pas encore définie
            if not flag.startswith('-') and config["url"] is None:
                config["url"] = flag
                i += 1
            else:
                # C'est soit un flag inconnu, soit une deuxième URL. Dans les deux cas, c'est une erreur.
                raise ValueError(f"Argument inconnu ou URL multiple : {flag}")
    if config["url"] == None:
        raise ValueError(f"Missing URL")
    
    try:
        path_obj = Path(config["path"])
        path_obj.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        raise ValueError(f"Permissions insuffisantes pour créer ou écrire dans le dossier '{config['path']}'.")
    except Exception:
        raise ValueError(f"Le chemin '{config['path']}' n'est pas un dossier valide.")
    return config
