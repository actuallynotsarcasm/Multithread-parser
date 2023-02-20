import requests, json
from bs4 import BeautifulSoup
import time
import threading

def timer_thr(sec):
    t = time.time()
    while True:
        if time.time() - t > sec:
            l.release()
            break

def parsePage(page, headers, vacancies, responses, n):
    url = 'https://hh.ru/search/vacancy?text=python&page='
    vacancies_found = {}
    try:
        while True:
            resp = requests.get(url+str(page), headers=headers)
            if str(resp) != '<Response [400]>':
                break
        if str(resp) == '<Response [200]>':
            text = resp.text
            soup = BeautifulSoup(text, 'html.parser')
            others_json = soup.find('template', {'id': "HH-Lux-InitialState"}).text
            others_data = json.loads(others_json)
            vacancies_data = others_data['vacancySearchResult']
            vacancies_list = vacancies_data['vacancies']
            for vac in vacancies_list:
                vacancies_found[str(vac['links']['desktop'])] = str(vac['name'])
            page += 1
    except Exception as e:
        resp = 'No connection'
    s.acquire()
    vacancies.update(vacancies_found)
    responses[n] = str(resp)
    s.release()

def parseVacancy(link, headers, reqs, fault_links, responses, n):
    try:
        while True:
            s.acquire()
            l.acquire()
            timer = threading.Thread(target=timer_thr, args=(0.7, ))
            timer.start()
            s.release()
            resp = requests.get(link, headers=headers)
            if str(resp) != '<Response [400]>':
                break
        if str(resp) == '<Response [200]>':
            text = resp.text
            soup = BeautifulSoup(text, 'html.parser')
            try:
                description = soup.find('div', {'class': "vacancy-description"}).text.lower()
                s.acquire()
                for req in reqs:
                    reqs[req] += int(req in description)
                s.release()
            except Exception as ex:
                print(soup.find('body').text)
                s.acquire()
                fault_links.append(link)
                s.release()
        else:
            print(str(resp))
    except Exception as e:
        resp = 'No connection'
    s.acquire()
    responses[n] = str(resp)
    s.release()


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-encoding': 'gzip, deflate, br',
    'Accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-control': 'max-age=0',
    'Cookie': '__ddg1_=Akb3qVmcSvklfHkcEXua; _xsrf=89e71a46b25317f2f4a61fae9470d4f5; regions=1; region_clarified=NOT_SET; display=desktop; crypted_hhuid=12D9D2FFD5494D67B3CCE7F73ACC90109F556F7CFDABB9392993B376880A44F0; hhuid=t72IdJjng0P!FGPMQyg6ng--; GMT=3; _ym_uid=16743309241002624082; _ym_d=1674330924; iap.uid=cd5a89c4bff8486a8497bf0bfa629f1e; hhul=57d0ebf5451d54b80237b882acf7ee1cbd572dd5e71cb1e598e1a994999dbaef; _gid=GA1.2.2042412768.1676332687; __zzatgib-w-hh=MDA0dC0jViV+FmELHw4/aQsbSl1pCENQGC9LXzBebmYjYXldJnZVUXoqHBN3dChRCA5jQUNwdjFxZR9oOVURCxIXRF5cVWl1FRpLSiVueCplJS0xViR8SylEW1R/KBwUeHEpVn8QVy8NPjteLW8PKhMjZHYhP04hC00+KlwVNk0mbjN3RhsJHlksfEspNVVWMi4hRjJyKgo8FF5uQnB2L0MfHmZ7X1N4XE56KCFDem9YURALYnIzaWVpcC9gIBIlEU1HGEVkW0I2KBVLcU8cenZffSpBbCNiSlwgSVtUeSYVe0M8YwxxFU11cjgzGxBhDyMOGFgJDA0yaFF7CT4VHThHKHIzd2UxPWoiYEtdIjVRP0FaW1Q4NmdBEXUmCQg3LGBwVxlRExpceEdXeisgF3puJlANEWI9RGllbQwtUlFRS2IPHxo0aQteTA==BMRp8Q==; remember=0; lrp=""; lrr=""; hhrole=anonymous; hhtoken=uEe9Ti5_Z936PiRGcnh_kyc0TGvm; supernova_user_type=applicant; _ga=GA1.1.762960774.1674330924; _gid=GA1.1.2042412768.1676332687; _ym_isad=2; _ga_44H5WGZ123=GS1.1.23a9015ec02096c9360d1edeada0b4262bc493d61f4556bf8c8a658db0a0505b.12.1.1676456994.60.0.0; _gat_gtag_UA_11659974_2=1; _ga=GA1.2.762960774.1674330924; _gat_gtag_UA_11659974_2_DG=1; cfidsgib-w-hh=zyPNKgGn823tEuvfT/qdylJypWjg8WngHvZke69f3TjI/A340/2whr0FQ4e6UICDLS7xyoRzTxg2xiq/1KExj9qm/f51aRceaF2Hveu3BW8UcYHvOMgIy0shEAggA3SPBskIYegpIPSYM98Q1P6tJjJeIS3SedTc/mi6I10=; cfidsgib-w-hh=zyPNKgGn823tEuvfT/qdylJypWjg8WngHvZke69f3TjI/A340/2whr0FQ4e6UICDLS7xyoRzTxg2xiq/1KExj9qm/f51aRceaF2Hveu3BW8UcYHvOMgIy0shEAggA3SPBskIYegpIPSYM98Q1P6tJjJeIS3SedTc/mi6I10=; gsscgib-w-hh=FMScw/TwKxk6IbaBc7D/BvXjUS0x1LvRIl/uwG5ZzWj1fh/bgYcpcf7pykNyVkpj/Qz4xLhT9eSe9mIbjhlOb2OMl4+a02wdPp0pGI/LOedgU1QAf06Ce8fM3gNpYfaNfE9jUZNjJK/aaIkSo8Hmh/KO3L40LxptIorvStvLkUNw2uc5FQ9TVkBbxsnzNthB+luyBK+GtlXeO93CssioOvXiRYdU0CnWHiNcXU3BIq954UuW8y1+r+4SPXU+5i6/4g==; device_breakpoint=s; total_searches=23; fgsscgib-w-hh=PnMja8e0cc14c74bc331b3eb323100f65e259744',
    'Sec-ch-ua': '"Chromium";v="108", "Opera GX";v="94", "Not)A;Brand";v="99"',
    'Sec-ch-ua-mobile': '?0',
    'Sec-ch-ua-platform': "Windows",
    'Sec-fetch-dest': 'document',
    'Sec-fetch-mode': 'navigate',
    'Sec-fetch-site': 'none',
    'Sec-fetch-user': '?1',
    'Upgrade-insecure-requests': '1',
    'User-agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0 (Edition Yx GX)'),
    'Connection': 'keep-alive',
    'DNT': '1'
}
s = threading.Semaphore(1)
l = threading.Lock()
t = time.time()
num = 41
vacancies = {}
responses = [''] * num
page = 0
flag = True
threads = [threading.Thread()] * num

while flag:
    for i in range(num):
        if not threads[i].is_alive():
            if responses[i] == '' or responses[i] == '<Response [200]>':
                threads[i] = threading.Thread(target=parsePage, args=(page, headers, vacancies, responses, i))
                threads[i].start()
                print('Page:', page)
                page += 1
            else:
                print(responses[i])
                for th in threads:
                    if th.is_alive():
                        th.join()
                flag = False
                break

print('\n')
print(len(vacancies))
print(time.time() - t)

t = time.time()
num = 20
responses = [''] * num
fault_links = []
reqs = {
    'django': 0,
    'fastapi': 0,
    'flask': 0
}
threads = [threading.Thread()] * num
n = 1

for link in vacancies:
    wait = True
    while wait:
        for i in range(num):
            if not threads[i].is_alive():
                wait = False
                if responses[i] == '' or responses[i] == '<Response [200]>':
                    if responses[i] == '<Response [200]>':
                        print(str(n)+'.', vacancies[link])
                        n += 1
                    threads[i] = threading.Thread(target=parseVacancy, args=(link, headers, reqs, fault_links, responses, i))
                    threads[i].start()
                else:
                    print(responses[i])
                    for th in threads:
                        if th.is_alive():
                            th.join()
                    flag = True
                break
    if flag:
        break
for th in threads:
    if th.is_alive():
        th.join()

print('\n')
print(reqs)
print('\n')
print(time.time() - t)
print('\n')
print('Fault links: ')
for i in fault_links:
    print(i)