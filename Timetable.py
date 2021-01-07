# -*- coding: utf-8 -*-

# Необходимые модули.
from io import StringIO
from lxml import etree
from re import sub


# Инициализация парсера.
tree = etree.parse(StringIO(open("MIIGAiK.html", "r").read()), parser=etree.HTMLParser())

# Массив с текущими днем и неделей.
today = [tree.xpath(f'//*[@class="left-content"]//strong/text(){[i]}') for i in range(2, 4)]  # День и неделя.
today = [today[0][0], today[1][0][9:-2:].lower()]  # Форматирование
# today = ['Вторник', "нижняя"]

# Массив с расписанием.
timetable = [x.xpath(".//td/text()") for x in tree.xpath('//*[@class="t"]/tr')]  # Со всем расписанием.
timetable = [item for item in timetable if (today[0] in item) and (today[1] in item)]  # С сегодняшним.
timetable = [item[1:2] + item[3:] for item in timetable]  # Без дня и недели.


for i in range(len(timetable)):

    timetable[i][-1] = (sub('[\n\xa0]', ' ', str(timetable[i][-1])).replace('  ', ' ').strip())

for item in timetable:
    print(item)
