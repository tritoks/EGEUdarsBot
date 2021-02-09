# EGEUdarsBot
Бот, который поможет тебе подготовиться к Заданиям на ударения в ЕГЭ

## Как запустить?
1. Открыть конфиг (там же можно указать пути для хранения файлов)
1. В переменной token указать token бота ТГ
1. Установить Python3
1. Установить telebot (`pip install pyTelegramBotAPI`)
1. Установить loguru (`pip install loguru`)
1. Запустить main.py
1. УСПЕХ!

## Как использовать?
Сразу после запуска он напишет вам случайное слово, которое нужно будет угадать (появляются кнопки).
После ответа оценит его верность и даст следующее слово.
Бот помнит, как вы отвечали, поэтому будет давать в первую очередь малознакомые слова.

## Что это за файлы?
- main.py - основная программа бота
- config.py - конфиг бота
- udars.json - список слов, которые будет кидать бот + варианты ответа в  JSON'e
- udars.py - генерирует udars.json из udars.txt
- udars.txt - текстовый файл, где на каждой новой строчке указано новое слово. Ударение обозначается заглавной буквой, примечания указываются после символа открытой скобки.
- db.json - база, где хранится статистика по всем пользователям, на основе ее и выбирается наименее знакомое (для пользователя) слово
