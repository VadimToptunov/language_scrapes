import os
import requests
from bs4 import BeautifulSoup


class GetFrenchVerbs:
    def __init__(self, filename, verb_list_file, uri):
        self.filename = filename
        self.verb_list_file = verb_list_file
        self.uri = uri


    def get_word_list(self):
        rsp = self.__send_request()
        self.__save_to_html(rsp)
        self.__save_to_verb_list()
        self.__cleanup_html()


    def __send_request(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }

        s = requests.Session()
        resp = s.get(self.uri, stream=True, headers=headers)
        return resp

    def __save_to_html(self, response):
        with open(self.filename, 'wb') as fd:
            for chunk in response.iter_content(1024):
                fd.write(chunk)


    def __save_to_verb_list(self):
        with open(self.filename, 'r') as fr:
            soup = BeautifulSoup(fr, 'html.parser')
            verb_list = soup.find_all('a', {"class": "cvplbd"})
            with open(self.verb_list_file, "w+") as fv:
                for verb in verb_list:
                    wr = str(verb.text) + "\n"
                    fv.writelines(wr)


    def __cleanup_html(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)
        else:
            print("Can not delete the file as it doesn't exists")


if __name__ == "__main__":
    filename = 'verb_conj.html'
    verb_list_file = 'french_verbs.txt'
    uri = 'https://www.lawlessfrench.com/verb-conjugations/'
    fv = GetFrenchVerbs(filename, verb_list_file, uri)
    fv.get_word_list()
