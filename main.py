import requests
from bs4 import BeautifulSoup
import json
import time

headers = {
    "user-agent":
    "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Mobile Safari/537.36"
}
main_url = 'https://www.skiddle.com'

def get_pages():
    for i in range(0, 265, 24):
        url = f'https://www.skiddle.com/festivals/search/?ajaxing=1&sort=0&fest_name=&from_date=&to_date=&maxprice=500&o={i}&bannertitle=May'
        res = requests.get(url=url, headers=headers)
        json_data = json.loads(res.content)
        html_response = json_data['html']

        with open(f'index_{i}.html', 'a', encoding='utf-8') as f:
            f.write(html_response)


def get_links():
    for i in range(0, 265, 24):
        with open(f'index_{i}.html', encoding='utf-8') as f:
            html = f.read()
            soup = BeautifulSoup(html, 'lxml')
            links = []
            titles = soup.find_all('h3', class_='card-title')

            for title in titles:
                links.append(title.find('a').get('href'))

            with open('links.txt', 'a', encoding='utf-8') as t:
                for link in links:
                    t.write(main_url + link + '\n')


def get_html(url):
    res = requests.get(url = url, headers=headers)
    return res.content
    
def main():
    json_data = []
    
    with open('links.txt', encoding='utf-8') as f:
        counter = 1
        for url in f:
        
            html = get_html(url.strip())
            soup = BeautifulSoup(html, 'lxml')
            try:
                info = soup.find('div', class_='top-info-cont')
                name = info.find('h1', class_='tc-white').text.strip()
                date = info.find('h3', class_='tc-white').text.strip()
                address_link = main_url + info.find('a').get('href').strip()
                
                data = {
                    'Festival name': name,
                    'Festival date': date
                }
                
                html = get_html(address_link)
                soup = BeautifulSoup(html, 'lxml')
                contact_details = soup.find('h2', string="Venue contact details and info").find_next()
                items = [item.text for item in contact_details.find_all('p')]
                contacts_info = {}
                for item in items:
                    contact_detail = item.split(': ')
                    detail_name = contact_detail[0]
                    detail_info = ''.join(contact_detail[1:])
                    contacts_info[detail_name] = detail_info
                data['Contacts info'] = contacts_info
                json_data.append(data)
                print(f'Iteration #{counter} completed')
                counter += 1
                time.sleep(1)
            except:
                print('Error')

    with open('festivals_data.json', 'a', encoding='utf-8') as file:
        json.dump(json_data, file, indent=4, ensure_ascii=False) 
                


if __name__ == '__main__':
    main()