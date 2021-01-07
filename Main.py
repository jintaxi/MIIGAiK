# -*- coding: utf-8 -*-
""" Эта программа получает сегодняшнее расписание пар МИИГАиК. """
# Необходимые модули.
from io import StringIO
from lxml import etree
from requests import post

# Данные для поучения HTML-кода страницы.
URL = "http://studydep.miigaik.ru/index.php"
payload = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14\
    .0 Safari/605.1.15",
    "fak": "ГФ",
    "kurs": "1",
    "grup": "ГиДЗг I-1аб"
}

# Инициализация парсера.
tree = etree.parse(StringIO(post(URL, payload).text), parser=etree.HTMLParser())

# Массив с текущими неделей и днём.
today: list = [tree.xpath(f'//*[@class="left-content"]//strong/text(){[i]}') for i in range(2, 4)]
today: list = [today[0][0], today[1][0][9:-4:].lower()]

# Массив с расписанием.
timetable: list = [x.xpath(".//td/text()") for x in tree.xpath('//*[@class="t"]/tr')]
timetable: list = [item for item in timetable if (today[0] in item) and (today[1] in item)]
timetable = [item[1:2] + item[3:] for item in timetable]
