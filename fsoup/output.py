import requests
from bs4 import BeautifulSoup

url = "https://rasp.omgtu.ru/group/show/11138"

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

schedule_table = soup.select('.table-responsive-md > table')[1]

for row in schedule_table.find_all('tr'):
    cells = row.find_all('td')
    if cells:
        time = cells[0].text.strip()
        subject = cells[1].text.strip()
        lecturer = cells[2].text.strip()
        room = cells[3].text.strip()
        print(time, subject, lecturer, room)
