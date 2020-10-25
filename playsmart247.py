import requests
from bs4 import BeautifulSoup
import re
import os
import csv


def get_request():
    headers = {
        'User-Agent': 'Mozila/5.0',
    }

    res = requests.request("GET", base_url, headers=headers)
    return res


def parse(content):
    return BeautifulSoup(content, 'html5lib')


def write(lines):
    with open(file='result.txt', encoding='utf-8', mode='w') as file:
        for item in lines:
            file.write("%s\n" % item)


def main():
    numbers = []
    response = get_request()
    soup = parse(response.text)
    options = soup.find_all('script')
    for option in options:
        script_txt = str(option.text)
        if '#new-datatable' in script_txt:
            results = script_txt.split('data:')[1].split('ordering:')[0].split(',')
            for result in results:
                content = result.replace('["', '').replace('"]', '').replace(']', '')
                content_soup = BeautifulSoup(content)
                number_soup = content_soup.find(attrs={'class': 'num'})
                if number_soup is not None:
                    number = number_soup.text.strip()
                    numbers.append(number)
                    print(len(numbers))
    write(lines=numbers)



if __name__ == '__main__':
    base_url = 'https://playsmart247.com/auto-roulette/?spins=250'
    main()
