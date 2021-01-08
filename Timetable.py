# -*- coding: utf-8 -*-
""" Эта программа получает сегодняшнее расписание пар МИИГАиК. """


# Необходимые модули.
from time import monotonic
time_start = monotonic()  # Начало замера времени.

from io import StringIO
from lxml import etree
from requests import post
from re import sub


""" Данные для поучения HTML-кода страницы. """
url = "http://studydep.miigaik.ru/index.php"
# Заголовки.
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14\
    .0 Safari/605.1.15"
}
 # Необходимая информация для запроса.
payload = {
    "fak": "ГФ",
    "kurs": "1",
    "grup": "ГиДЗг I-1аб"
}

""" Данные для замены пар на время. """
schedule = {
    '1': '9:40 - 10:30',
    '2': '10:40 - 12:10',
    '3': '12:50 - 14:20',
    '4': '14:30 - 16:00',
    '5': '16:10 - 17:40',
    '6': '17:50 - 19:20',
    '7': '19:30 - 21:00'
}

""" Инициализация парсера. """
response = StringIO(post(url=url, data=payload, headers=headers, proxies=None).text)
tree = etree.parse(response, parser=etree.HTMLParser())
response.close()

""" Массив с текущими неделей и днём. """
# Число и год.
date = [tree.xpath('//*[@class="left-content"]//strong/text()')[0][11:]]
# День и неделя.
today = [tree.xpath(f'//*[@class="left-content"]//strong/text(){[i]}') for i in range(2, 4)]
today = [today[0][0], today[1][0][9:-4:].lower()]

""" Массив с распианием. """
# Массив со всем распианием.
timetable = [x.xpath(".//td/text()") for x in tree.xpath('//*[@class="t"]/tr')]
# Массив со сегодняшним расписанием.
timetable = [item for item in timetable if (today[0] in item) and (today[1] in item)]
# Массив со всем распианием без дней и недель.
timetable = [item[1:2] + item[3:] for item in timetable]
# Форматирование: пары, подгруппы, ссылки.
for i in range(len(timetable)):
    timetable[i][1] = (sub('[\xa0]', ' ', str(timetable[i][1])).replace('  ', ' ').strip())
    timetable[i][4] = timetable[i][4].replace("  ", "")
    timetable[i][-1] = (sub('[\n\xa0\r]', ' ', str(timetable[i][-1])).replace('   ', ' ').strip())
# Форматирование имен преподавателей.
for item in timetable:
    if len(item) != 8:
        item[3] = (item[3] + item[4]).replace('  ', '; ')
        del item[4]
# Замена "*-я пара" на время.
for item in timetable:
    item[0] = item[0].replace(f"{item[0][0]}-я пара", schedule[f"{item[0][0]}"])

"""Запись в файл."""
with open(f"schedule/Расписание на {date[0]}.txt", "w") as file:
    for item in timetable:
        for i in range(len(item)):
            if i != len(item)-1:
                file.write(item[i] + " | ")
            else:
                file.write("\n" + item[i])
        file.write("\n\n")

"""Вывод времени исполнения (в миллисекунлах). """
print("Расписание успешно получено и записано в файл.")
print(f"Затраченное время: {int((round((monotonic() - time_start), 3)) * 1000)} миллисекунд(ы/а).")
