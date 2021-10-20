from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import pandas as pd
import wikipediaapi


all_cities = pd.read_csv("frontend/worldcities.csv")


def main_page(request):
    if request.GET:
        city = request.GET.get('q', '')
        temp = get_weather_from_google(city)
        info = get_information_about_the_city(city)
        data = {'city': city, "temp": temp, 'auto_com': list(all_cities['city']), 'info': info}
        return render(request, 'frontend/main.html', data)
    else:
        return render(request, 'frontend/main.html',{'auto_com': list(all_cities['city'])})

def get_weather_from_google(city="Yerevan"):
    try:
        search = f"weather in {city}"
        url = f"https://www.google.com/search?q={search}"
        req = requests.get(url)
        sav = BeautifulSoup(req.text, 'html.parser')
        temp = sav.find("div", class_="BNeawe").text
        # to make sure there we have the temp we try to convert it to int
        check_flag = int((int(temp[:-2])-32)*5/9)
        return temp
    except ValueError:
        return "No Info"


def get_information_about_the_city(city="Yerevan"):

    wiki_wiki = wikipediaapi.Wikipedia(language='en', extract_format=wikipediaapi.ExtractFormat.WIKI)
    p_wiki = wiki_wiki.page(city)
    if "refer" in p_wiki.text:
        p_wiki = wiki_wiki.page(f"{city} City")
        return p_wiki.summary
    else:
        return p_wiki.summary
