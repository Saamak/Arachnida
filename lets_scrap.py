import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
import time
from termcolor import colored


def print_header(config):
    print(colored("\n---- Let's Scrap these images ----\n", attrs=["bold"]))
    print(colored(f"config : {config}\n", "yellow", attrs=["bold"]))


def hub(config):
    print_header(config)
    service = FirefoxService(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service)
    # Ajout d'un timeout pour éviter que le script ne se bloque indéfiniment
    driver.set_page_load_timeout(20)

    # --- Configuration de la récursion ---
    if config['recursive'] is True:
        max_depth = config['level']
    else:
        max_depth = 0

    # Liste des extensions d'images autorisées
    allowed_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')

    # urls_to_visit : notre "liste de choses à faire"
    # Chaque élément est une paire : (url, profondeur_actuelle)
    urls_to_visit = [(config['url'], 0)]
    
    # visited_urls : pour ne pas traiter deux fois la même page
    visited_urls = []
    
    # --- Boucle principale d'exploration ---
    while urls_to_visit:
        # On prend la première URL de la liste et sa profondeur
        current_url, current_depth = urls_to_visit.pop(0)

        # On vérifie si on doit ignorer cette URL
        if current_url in visited_urls or current_depth > max_depth:
            continue

        print(colored(f"\n[Profondeur {current_depth}] Traitement de : {current_url}", "cyan", attrs=["bold"]))
        visited_urls.append(current_url)

        try:
            # Navigue vers l'URL actuelle
            driver.get(current_url)
            
            # Attente simple pour laisser le JS se charger
            time.sleep(2)

            # Essayer de fermer le pop-up de cookies s'il y en a un
            try:
                accept_button = driver.find_element(By.ID, "didomi-notice-agree-button")
                if accept_button:
                    accept_button.click()
                    time.sleep(1) # Attendre que le pop-up disparaisse
            except:
                pass # Pas de bouton, on continue

            # --- Votre logique de recherche d'images ---
            print("Le site est ouvert. Recherche d'images...")
            imgs = driver.find_elements(By.TAG_NAME, 'img')
            imgs_urls = []
            for img in imgs:
                # On essaie l'attribut 'src', et s'il est vide, on essaie 'data-src'.
                # C'est pour gérer le "lazy loading" où l'URL de l'image est cachée.
                src = img.get_attribute('src') or img.get_attribute('data-src')

                # On ne garde que les URLs valides (qui commencent par http)
                if src and src.startswith(('http', 'https')):
                    # On reconstruit les URLs relatives (même si on filtre http, c'est une sécurité)
                    if not src.startswith(('http', 'https')):
                        from urllib.parse import urljoin
                        src = urljoin(current_url, src)
                    
                    # On évite d'ajouter des doublons
                    if src not in imgs_urls:
                        imgs_urls.append(src)
            
            # --- Votre logique de téléchargement ---
            output_folder = config['path']
            for i, img_url in enumerate(imgs_urls):
                try:
                    print(f"  -> Téléchargement de : {img_url}")
                    response = requests.get(img_url)
                    
                    file_ext = os.path.splitext(img_url.split('?')[0])[1]
                    if not file_ext in allowed_extensions:
                        file_ext = '.jpg'

                    file_name = os.path.join(output_folder, f"image_{len(visited_urls)}_{i}{file_ext}")
                    with open(file_name, 'wb') as f:
                        f.write(response.content)
                    print(colored(f"     Enregistrée sous : {file_name}", "green"))

                except Exception as e:
                    print(colored(f"     Erreur lors du téléchargement de {img_url}: {e}", "red"))

            # --- Logique pour la récursion : trouver de nouveaux liens ---
            if current_depth < max_depth:
                print(colored("  -> Recherche de nouveaux liens...", "yellow"))
                links = driver.find_elements(By.TAG_NAME, 'a')
                for link in links:
                    href = link.get_attribute('href')
                    # On ne garde que les liens valides qui appartiennent au même site
                    if href and href.startswith(config['url']):
                        
                        # On ignore les ancres (#) pour ne pas visiter la même page plusieurs fois
                        clean_href = href.split('#')[0]

                        if clean_href not in visited_urls:
                            # On vérifie aussi que l'URL n'est pas déjà dans la liste à visiter
                            # pour éviter les doublons dans la file d'attente.
                            is_already_in_queue = any(clean_href == url_in_queue[0].split('#')[0] for url_in_queue in urls_to_visit)
                            if not is_already_in_queue:
                                urls_to_visit.append((href, current_depth + 1))

        except Exception as e:
            print(colored(f"Erreur lors du traitement de la page {current_url}: {e}", "red"))

    # S'assure que le navigateur et le driver sont bien fermés à la fin
    print(colored("\nExploration terminée.", attrs=["bold"]))
    driver.quit()
