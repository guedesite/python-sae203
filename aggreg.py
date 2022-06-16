# -*- coding: utf-8 -*-
"""
Created on Mon May 16 12:35:44 2022

@author: guedesite
"""
import sys;
import feedparser;
import time;
import yaml;
from datetime import datetime;
from os.path import exists as file_exists

# Charge flux RSS des urls dans liste_url avec feedparser et renvois les entrées 
# ou None si l'url est inaténiable
def charge_urls(liste_url):
    Return = [];
    for url_rss in liste_url:
        parse = feedparser.parse(url_rss) # Chargement du flux RSS
        if parse.bozo is False: # On vérifie si il y a une erreur lors de la requête HTTP
            Return.append(parse.entries);
        else:
            Return.append(None);
    return Return;

# Génère la liste final des flux RSS en récupérant les informations qui nous interesse
def fusion_flux(liste_url, liste_flux, tri_chrono):
    Return = [];
    for i in range(len(liste_url)): # Boucle principal
        if liste_flux[i] is not None: # liste_flux[i] est "None" si il y a eu une erreur lors de la requête HTTP
            for feed in liste_flux[i]:
                dic = {};
                dic["titre"] = feed["title"];
                dic["category"] = feed["tags"][0]["term"];
                dic["serveur"] = liste_url[i];
                dic["date_publi"] = feed["published"];
                dic["lien"] = feed["link"];
                dic["description"] = feed["summary"];

                element = datetime.strptime(dic["date_publi"],"%a, %d %b %Y %H:%M");
                dic["time"] = int(datetime.timestamp(element));

                if(len(Return) > 0 and tri_chrono): # On commence par vérifier si l'option est activer et si la liste est vide
                    for i2 in range(len(Return)): # On fait une boucle de chaque entré dans la liste
                        if Return[i2]["time"] < dic["time"]: # On regarde a quel index notre entré actuel est plus grande
                            # On inseère notre entré à l'endroit dans la liste ou notre entré est plus grande que la précédente
                            # Pas besoin de vérifié si le suivant est plus petit ou non, il est obligatoirement égal ou plus grand
                            # De se fait une chronologie se créé au fur et à mesure
                            Return.insert(i2, dic);
                            break;
                else:
                    Return.append(dic);
    return Return;

# Génère la page HTML avec le flux RSS précédement traité
def genere_html(liste_evenements, chemin_html):
    output = "";

    chemin_css = "/".join(chemin_html.split("/")[:-1]) + "/theme.css"; 
    # récupère le chemin du fichier css
    # chemin_html.replace(chemin_html.split("/")[-1], "") marche mais il peut y avoir des conflits
    # si des dossiers du chemin on la même suite de caractère que le fichier .html

    with open('assets/model.html', "r") as f: #On charge notre page model
        content = f.read();

        parts = content.split("{boucle}"); # On découpe la page en trois partie
        # La première étant notre entête
        # La deuxième étant notre balise <article> a répéter avec les informations des flux RSS
        # La troisième le footer

        #Partie 1: header
        actualTime = time.strftime("%a, %d %b %Y %H:%M", time.localtime());
        output = parts[0].replace("{date-et-heure-actuelle}",actualTime);

        #Partie 2:articles
        for event in liste_evenements:
            # Pour chaque évènement de notre flux RSS on récupère notre deuxième partie 
                # pour lui attribué les données du flux correspondant avant de l'ajouter à la suite de la page HTML
            pre_output = parts[1];
            for key in event:
                # Pour chaque clef du dictionnaire de l'évènement, une balise lui est attribué dans le model avec le même nom
                pre_output = pre_output.replace("{"+str(key)+"}", str(event[key]));
            output += pre_output;

        #Partie 3:footer
        output += parts[2];
    with open(chemin_html, "w+") as f: # On finis par écrire notre fichier
        f.write(output);
    if not file_exists(chemin_css): # Si le fichier css n'éxiste pas on le créé
        with open('assets/theme.css', "r") as f: 
            with open(chemin_css, "w+") as f: 
                f.write(f.read());

# Charge la config stocker en yaml
def load_config():
    with open("assets/config.yaml", "r") as configs:
        return yaml.safe_load(configs);

# Génère les urls finaux, en additionnant les urls des serveurs et le nom du fichier contenant le flux RSS
def generate_rssurls(urls, name):
    Return = [];
    for url in urls:
        Return.append(url+"/"+name);
    return Return;


def main():

    configs = load_config(); # On charge la config

    urls_rss = generate_rssurls(configs["sources"], configs["rss-name"]); # On génère nos URLS finaux

    liste_flux = charge_urls(urls_rss); # On charge nos flux RSS

    liste_evenements = fusion_flux(configs["sources"], liste_flux, configs["tri-chrono"]); # On finalise la liste contenant nos évènements
 
    genere_html(liste_evenements, configs["destination"]); # On finit par générer notre page HTML

if __name__ == "__main__":
    main();
