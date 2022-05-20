# -*- coding: utf-8 -*-
"""
Created on Mon May 16 12:35:44 2022

@author: guedesite
"""
import sys;
import feedparser;

def charge_urls(liste_url):
    Return = [];
    for url_rss in liste_url:
        parse = feedparser.parse(url_rss)
        if parse.bozo is False:
            Return.append(parse.entries);
        else:
            Return.append(None);
    return Return;


def fusion_flux(liste_url, liste_flux):
    Return = [];
    for i in range(len(liste_url)):
        if liste_flux[i] is not None:
            for feed in liste_flux[i]:
                dic = {};
                dic["titre"] = feed["title"];
                dic["categorie"] = feed["tags"][0]["term"];
                dic["serveur"] = liste_url[i];
                dic["date_publi"] = feed["published"];
                dic["lien"] = feed["link"];
                dic["description"] = feed["summary"];
                Return.append(dic);
    return Return;

def genere_html(liste_evenements, chemin_html):


def main():
    assert len(sys.argv) > 1;

    rss_urls = sys.argv;
    rss_urls.pop(0); # On supprime le fichier python de la liste des arguments

    liste_flux = charge_urls(rss_urls);

    liste_evenements = fusion_flux(rss_urls, liste_flux);


if __name__ == "__main__":
    main();
