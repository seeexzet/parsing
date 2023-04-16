import requests
import fake_headers
from bs4 import BeautifulSoup
import json

def get_headers():
    return fake_headers.Headers(browser='chrome', os='win').generate()

HOST = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'

response = requests.get(HOST, headers=get_headers())

soup = BeautifulSoup(response.text, features='lxml')
vacancies = soup.find_all(class_='vacancy-serp-item-body')
print(len(vacancies))

parsed = []

for vacancy in vacancies:
    vacancy_parsed = vacancy.find(class_='serp-item__title')
    name = vacancy_parsed.text
    next_link = vacancy_parsed['href']
    response = requests.get(next_link, headers = get_headers())
    hh_article = BeautifulSoup(response.text, features='lxml')
    vacancy_description = hh_article.find(class_="g-user-content").text
    if ('Django' in vacancy_description or 'Flask' in vacancy_description):
        company_name = vacancy.find(class_="bloko-text").text
        salary = hh_article.find(class_="bloko-header-section-2 bloko-header-section-2_lite").text
        city = vacancy.find_all(class_="bloko-text")[1].text
        item = {
            'name': name,
            'link': next_link,
            'salary': salary,
            'company_name': company_name,
            'city': city
        }
        parsed.append(item)

with open('hh_vacancy.json', 'w', encoding='utf8') as file:
    json.dump(parsed, file, indent=5, ensure_ascii=False)
    print('Запись в файл выполнена')