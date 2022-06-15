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


def charge_urls(liste_url):
    Return = [];
    for url_rss in liste_url:
        parse = feedparser.parse(url_rss)
        if parse.bozo is False:
            Return.append(parse.entries);
        else:
            Return.append(None);
    return Return;


def fusion_flux(liste_url, liste_flux, trichrono):
    Return = [];
    for i in range(len(liste_url)):
        if liste_flux[i] is not None:
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

                if(len(Return) > 0 and trichrono):
                    for i2 in range(len(Return)):
                        if Return[i2]["time"] < dic["time"]:
                            Return.insert(i2, dic);
                            break;
                else:
                    Return.append(dic);
    return Return;

def genere_html(liste_evenements, chemin_html):
    output = "";
    with open('assets/model.html', "r") as f:
        content = f.read();

        parts = content.split("{boucle}");

        #Partie 1: header
        actualTime = time.strftime("%a, %d %b %Y %H:%M", time.localtime());
        output = parts[0].replace("{date-et-heure-actuelle}",actualTime);

        #Partie 2:articles
        for event in liste_evenements:
            pre_output = parts[1];
            for key in event:
                pre_output = pre_output.replace("{"+str(key)+"}", str(event[key]));
            output += pre_output;

    with open(chemin_html, "w+") as f:
        f.write(output);

def load_config():
    with open("assets/config.yaml", "r") as configs:
        return yaml.safe_load(configs);

def generate_rssurls(urls, name):
    Return = [];
    for url in urls:
        Return.append(url+"/"+name);
    return Return;


def main():

    configs = load_config();


    urls_rss = generate_rssurls(configs["sources"], configs["rss-name"]);

    liste_flux = charge_urls(urls_rss);

    liste_evenements = fusion_flux(configs["sources"], liste_flux, configs["tri-chrono"]);

    genere_html(liste_evenements, configs["destination"]);

if __name__ == "__main__":
    main();
