from bs4 import BeautifulSoup
import pandas as pd
import requests 

base_url = "https://twitter.com/search?q=(from%3A{username})%20lang%3A{language}}&src=typed_query"
username = "sanhabot"
languages = ["ko"]

with open("index.html") as fp:
    soup = BeautifulSoup(fp, 'lxml')

soup = BeautifulSoup("<html>a web page</html>", 'lxml')

