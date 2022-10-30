import json

import requests
from bs4 import BeautifulSoup


def getData(url):
    # with open('glassdoor.html', 'r',encoding='utf8') as f:
    #     soup = BeautifulSoup(f, 'lxml')
    soup = BeautifulSoup(requests.get(url).text, 'lxml')
    print(soup.prettify())
    base_pay = soup.find('div', {'data-test': "base-pay"})
    if not base_pay:
        base_pay = soup.find('span', {"data-test": "pay-period-MONTHLY-label"})
    total_pay = soup.find('div', {'data-test': "total-pay"})
    if not total_pay:
        total_pay = soup.find('div', {"data-test": "pay-period-label"})
    additional_pay = soup.find('div', {'data-test': "additional-pay-breakdown-all"})
    if not additional_pay:
        additional_pay = soup.find_all('span', {"data-test": "pay-period-MONTHLY-label"})[1]
    data = {
        "title": soup.find('title').text.split('Salaries')[0].strip(),
        "total_pay": total_pay.text.strip(),
        "base_pay": base_pay.text.strip().split('Base')[0],
        "additional_pay": additional_pay.text.strip().split('All')[0],
    }
    print(json.dumps(data, indent=4))


def main():
    getData('https://www.glassdoor.com/Salary/Motorola-Solutions-Software-Engineer-Salaries-E427189_D_KO19,36.htm')


if __name__ == '__main__':
    main()
