# -*- coding: utf-8 -*-
"""
Created on Mon May 16 12:35:44 2022

@author: guedesite
"""
import sys;
import feedparser;

def charge_urls(liste_url):
    Return = {};
    for url_rss in liste_url:
        try:
            parse = feedparser.parse(url_rss)
            Return[url_rss] = [];
            for key, entrie in parse.entries: 
                Return[url_rss].append(entrie);
        except:
            Return[url_rss] = None;
    return Return;
        
    
def display_charge_urls(liste_flux):
    for key in liste_flux.keys():
        print("-"*30);
        print(key);
        print("-"*30);
        index = 0;
        if liste_flux[key] is None:
            print("url error");
        else:
            for entries in liste_flux[key]:
                print("Item "+str(index));
                index +=1;
                for key, feed in entries:
                    print("\t "+str(key)+":"+str(entries[key]));
                    
def fusion_flux(liste_url, liste_flux):
    Return = [];
    for key in liste_flux.keys():
        if liste_flux[key] is not None:
            for entries in liste_flux[key]:
                for feed in entries:
                    entrie = {};
                    
    return Return;


def main():
    assert len(sys.argv) > 1;
    
    rss_urls = sys.argv;
    rss_urls.pop(0); # On supprime le fichier python de la liste des arguments
    
    liste_flux = charge_urls(rss_urls);
    
    display_charge_urls(liste_flux);
    
        
    
if __name__ == "__main__":
    main();