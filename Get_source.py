# -*- coding: utf-8 -*-

# Необходимые модули.
from requests import post


# Данные для поучения HTML-кода страницы.
url = "http://studydep.miigaik.ru/index.php"
payload = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14\
    .0 Safari/605.1.15",
    "fak": "ГФ",
    "kurs": "1",
    "grup": "ГиДЗг I-1аб"
}

# Запись HTML-кода страницы в локальный файл.
open("MIIGAiK.html", "w").write(post(url, payload).text)
