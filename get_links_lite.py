import sys
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

query = sys.argv[1]
url = "https://lite.duckduckgo.com/lite/"
data = urllib.parse.urlencode({'q': query}).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={"User-Agent": "Mozilla/5.0"})
html = urllib.request.urlopen(req).read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")
for a in soup.find_all("a", class_="result-url"):
    print(a.get("href"))
