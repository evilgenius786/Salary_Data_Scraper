import json

from bs4 import BeautifulSoup


def getData(url):
    with open('payscale.html', 'r') as f:
        soup = BeautifulSoup(f, 'html.parser')
    perc_chart = soup.find_all('div', {'class': 'percentile-chart__label'})
    data = {
        'title': soup.find('h1').text,
        'salary': soup.find('span', {'class': 'paycharts__value'}).text,
        'duration': soup.find('div', {'class': 'Dropdown-placeholder'}).text,
        "low%": perc_chart[0].find_all('div')[0].text,
        "low": perc_chart[0].find_all('div')[1].text,
        "median%": perc_chart[2].find_all('div')[0].text,
        "median": perc_chart[2].find_all('div')[1].text,
        "high%": perc_chart[4].find_all('div')[0].text,
        "high": perc_chart[4].find_all('div')[1].text,
        "perc_desc": soup.find('p', {'class': "paycharts__percentile--desc"}).text,
        'paycharts_footer': soup.find('div', {'class': 'paycharts__footer'}).text,
    }
    for row in soup.find_all("div", {"class": "tablerow"}):
        data[row.find_all("div")[0].text] = row.find("div", {'class': 'tablerow__value'}).text
    for div in soup.find_all('div', {'class': 'healthbenefits__item'}):
        name = div.find('div', {'class': 'healthbenefits__item-name'}).text
        value = div.find('div', {'class': 'healthbenefits__item-value'}).text
        data[name] = value
    for div in soup.find_all('div', {'class': 'gender__item'}):
        data[div.find("div").text] = div.find_all("div")[1].text
    for div in soup.find_all('div', {'class': 'entry'}):
        data[div.find("div").text] = div.find("div", {'class': 'arrow'}).text[3:]
    script = json.loads(soup.find('script', {'id': '__NEXT_DATA__'}).text)
    for row in script["props"]["pageProps"]["pageData"]["byDimension"]["Job by Experience"]["rows"]:
        data[row["name"]] = row["range"]['50']
    # with open('payscale.json', 'w') as f:
    #     json.dump(script, f, indent=4)
    print(json.dumps(data, indent=4))


def main():
    getData('https://www.payscale.com/research/SA/Job=Accountant/Salary')


if __name__ == '__main__':
    main()
