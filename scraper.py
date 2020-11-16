def nbp_scraper():
    from bs4 import BeautifulSoup
    import requests
    import os
    import math

    def parse_row(row):
        name = row.find_all("td")[0].text.strip()
        code = row.find_all("td")[1].text.strip()
        rate = float(row.find_all("td")[2].text.replace(',', '.'))

        i = 0
        for char in code:
            i += 1
            if char == ' ':
                temp = code[:i-1]
                code = code[i:]
                rate = round(rate/float(temp), int(4+math.log(int(temp), 10)))

        return {
            'code': code,
            'name': name,
            'rate': rate
                }
    
    url = "https://www.nbp.pl/home.aspx?f=/kursy/kursya.html"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find("table", {"class": "pad5"})
    rows = table.find_all('tr')[1:]
    
    data = []
    for row in rows:
        data.append(parse_row(row))
    
    data = sorted(data, key=lambda a: a['code'])
    
    return data