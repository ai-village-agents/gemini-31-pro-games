import sys
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import re

query = sys.argv[1]
url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(query)
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
html = urllib.request.urlopen(req).read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")
for a in soup.find_all("a", class_="result__url"):
    print(a.get("href"))
