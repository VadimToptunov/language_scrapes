import requests
from bs4 import BeautifulSoup

data = []
resp = requests.get('https://www.ef.ru/angliyskie-resursy/angliyskie-idiomy/')
# print(resp.text)
soup = BeautifulSoup(resp.content, 'html.parser')
all_tds = soup.find_all('tr')
# print(all_tds)
for td in all_tds:
    tds = td.find_all_next('td')
    d = {
        "eng" : tds[0].text.strip("\r\n\t\t\t\t"),
        "rus" : tds[1].text.strip("\r\n\t\t\t\t")
    }
    data.append(d)

print(data)