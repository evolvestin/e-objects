import os
import re
import sys
import time
import heroku3
import asyncio
import aiogram
import _thread
import telebot
import inspect
import calendar
import requests
import traceback
import unicodedata
from time import sleep
import concurrent.futures
from ast import literal_eval
from bs4 import BeautifulSoup
from datetime import datetime
from unidecode import unidecode
search_major_fails_pattern = 'The (read|write) operation timed out|Backend Error|is currently unavailable.'
search_minor_fails_pattern = 'Failed to establish a new connection|Read timed out.|ServerDisconnectedError'
week = {'Mon': 'Пн', 'Tue': 'Вт', 'Wed': 'Ср', 'Thu': 'Чт', 'Fri': 'Пт', 'Sat': 'Сб', 'Sun': 'Вс'}
search_retry_pattern = r'Retry in (\d+) seconds|"Too Many Requests: retry after (\d+)"'
sql_patterns = ['database is locked', 'disk image is malformed', 'no such table']
bot_error = telebot.TeleBot('580232743:AAEfqNw32ob_YkiM22GtcL68jDgP1ZJ_RMU')
bot_start = telebot.TeleBot('456171769:AAGVaAEZTE1n4YLa-RnRmsQ60O9C31otqiI')
idDevCentre = -1001312302092
log_file_name = 'log.txt'


def test():
    return 'test from github 0.0.5'


def bold(text):
    return '<b>' + str(text) + '</b>'


def under(text):
    return '<u>' + str(text) + '</u>'


def italic(text):
    return '<i>' + str(text) + '</i>'


def code(text):
    return '<code>' + str(text) + '</code>'


def html_secure(text):
    return re.sub('<', '&#60;', str(text))


def time_now():
    return int(datetime.now().timestamp())


def get_me_dict(token):
    me = str(telebot.TeleBot(token).get_me())
    return literal_eval(me)


def append_values(array, values):
    if type(values) != list:
        values = [values]
    array.extend(values)
    return array


def chunks(array, separate):
    separated = []
    d, r = divmod(len(array), separate)
    for i in range(separate):
        sep = (d+1)*(i if i < r else r) + d*(0 if i < r else i - r)
        separated.append(array[sep:sep+(d+1 if i < r else d)])
    return separated


def concurrent_functions(futures):
    if type(futures) != list:
        futures = [futures]
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as future_executor:
        futures = [future_executor.submit(future) for future in futures]
        for future in concurrent.futures.as_completed(futures):
            printer(future.result())


def stamper(date, pattern=None):
    if pattern is None:
        pattern = '%d/%m/%Y %H:%M:%S'
    try:
        stamp = int(calendar.timegm(time.strptime(date, pattern)))
    except IndexError and Exception:
        stamp = False
    return stamp


def send_dev_message(text, tag=code, good=False):
    bot = bot_error
    text = html_secure(text)
    bot_name, host = get_bot_name()
    if good:
        bot = bot_start
    if tag:
        text = tag(text)
    text = bold(bot_name) + ' (' + code(host) + '):\n' + text
    message = bot.send_message(idDevCentre, text, disable_web_page_preview=True, parse_mode='HTML')
    return message


def query(link, string):
    response = requests.get(link + '?embed=1')
    soup = BeautifulSoup(response.text, 'html.parser')
    is_post_not_exist = str(soup.find('div', class_='tgme_widget_message_error'))
    if str(is_post_not_exist) == 'None':
        raw = str(soup.find('div', class_='tgme_widget_message_text js-message_text')).replace('<br/>', '\n')
        text = BeautifulSoup(raw, 'html.parser').get_text()
        search = re.search(string, text, flags=re.DOTALL)
        return search
    else:
        return None


def start_message(token_main, stamp1, text=None):
    bot_name, host = get_bot_name()
    bot_username = str(get_me_dict(token_main).get('username'))
    head = '<a href="https://t.me/' + bot_username + '">' + \
        bold(bot_name) + '</a> (' + code(host) + '):\n' + \
        log_time(stamp1, code) + '\n' + log_time(tag=code)
    start_text = ''
    if text:
        start_text = '\n' + str(text)
    text = head + start_text
    message = bot_start.send_message(idDevCentre, text, disable_web_page_preview=True, parse_mode='HTML')
    return message


def get_bot_name():
    host = 'Unknown'
    app_name = 'Undefined'
    token = os.environ.get('api')
    if token:
        connection = heroku3.from_key(token)
        for app in connection.apps():
            app_name = app.name
            if app_name.endswith('first'):
                app_name = re.sub('-first', '', app_name, 1)
                host = 'One'
            if app_name.endswith('second'):
                app_name = re.sub('-second', '', app_name, 1)
                host = 'Two'
    return app_name, host


def start_main_bot(library, token):
    parameter = 'w'
    directory = os.listdir('.')
    text = 'Начало записи лога ' + log_time() + '\n' + \
        'Номер главного _thread: ' + str(_thread.get_ident()) + '\n' + '-' * 50
    if log_file_name in directory:
        parameter = 'a'
        text = '\n' + '-' * 50 + '\n' + text
    file = open(log_file_name, parameter)
    file.write(text)
    file.close()
    if library == 'async':
        return aiogram.Bot(token)
    else:
        return telebot.TeleBot(token)


def secure_sql(func, value=None):
    lock = True
    response = False
    while lock is True:
        lock = False
        try:
            if value:
                response = func(value)
            else:
                response = func()
        except IndexError and Exception as error:
            response = str(error)
            for pattern in sql_patterns:
                if pattern in str(error):
                    lock = True
                    sleep(1)
    return response


async def async_secure_sql(func, value=None):
    lock = True
    response = False
    while lock is True:
        lock = False
        try:
            if value:
                response = func(value)
            else:
                response = func()
        except IndexError and Exception as error:
            response = str(error)
            for pattern in sql_patterns:
                if pattern in str(error):
                    await asyncio.sleep(1)
                    lock = True
    return response


def log_time(stamp=None, tag=None, gmt=3, form=None):
    if stamp is None:
        stamp = int(datetime.now().timestamp())
    weekday = datetime.utcfromtimestamp(stamp + gmt * 60 * 60).strftime('%a')
    day = datetime.utcfromtimestamp(stamp + gmt * 60 * 60).strftime('%d')
    month = datetime.utcfromtimestamp(stamp + gmt * 60 * 60).strftime('%m')
    year = datetime.utcfromtimestamp(stamp + gmt * 60 * 60).strftime('%Y')
    hour = datetime.utcfromtimestamp(stamp + gmt * 60 * 60).strftime('%H')
    minute = datetime.utcfromtimestamp(stamp).strftime('%M')
    second = datetime.utcfromtimestamp(stamp).strftime('%S')
    response = week[weekday] + ' ' + day + '.' + month + '.' + year + ' ' + hour + ':' + minute + ':' + second
    if form == 'channel':
        response = day + '/' + month + '/' + year + ' ' + hour + ':' + minute + ':' + second
    elif form == 'normal':
        response = day + '.' + month + '.' + year + ' ' + hour + ':' + minute + ':' + second
    if tag:
        response = tag(response)
    if form is None:
        response += ' '
    return response


def printer(printer_text):
    parameter = 'w'
    thread_name = ''
    directory = os.listdir('.')
    stack = inspect.stack()
    if len(stack) <= 4:
        stack = list(reversed(stack))
    for i in stack:
        if i[3] not in ['<module>', 'printer']:
            thread_name += i[3] + '.'
            if len(stack) > 4:
                break
    thread_name = re.sub('[<>]', '', thread_name[:-1])
    log_print_text = thread_name + '() [' + str(_thread.get_ident()) + '] ' + str(printer_text)
    file_print_text = log_time() + log_print_text
    if log_file_name in directory:
        file_print_text = '\n' + file_print_text
        parameter = 'a'
    file = open(log_file_name, parameter)
    file.write(file_print_text)
    print(log_print_text)
    file.close()


def properties_json(sheet_id, limit, option=None):
    if option is None:
        option = []
    body = {
        'requests': [
            {
                'updateCells': {
                    'rows': [
                        {
                            'values': [
                                {
                                    'userEnteredValue': {'stringValue': option[i]},
                                    'userEnteredFormat': {'horizontalAlignment': 'CENTER'}
                                }
                            ]
                        } if len(option) - 1 >= i else {
                            'values': [
                                {
                                    'userEnteredValue': {'stringValue': ''},
                                    'userEnteredFormat': {'horizontalAlignment': 'CENTER'}
                                }
                            ]
                        } for i in range(0, limit)
                    ],
                    'fields': 'userEnteredValue, userEnteredFormat',
                    'range': {
                        'sheetId': sheet_id,
                        'startRowIndex': 0,
                        'endRowIndex': limit,
                        'startColumnIndex': 0,
                        'endColumnIndex': 1
                    }
                }
            },
            {
                'updateDimensionProperties': {
                    'range': {
                        'sheetId': sheet_id,
                        'dimension': 'COLUMNS',
                        'startIndex': 0,
                        'endIndex': 1
                    },
                    'properties': {
                        'pixelSize': 1650
                    },
                    'fields': 'pixelSize'
                }
            }
        ]
    }
    return body


def edit_dev_message(old_message, text):
    entities = old_message.entities
    text_list = list(html_secure(old_message.text))
    if entities:
        position = 0
        used_offsets = []
        for i in text_list:
            true_length = len(i.encode('utf-16-le')) // 2
            while true_length > 1:
                text_list.insert(position + 1, '')
                true_length -= 1
            position += 1
        for i in reversed(entities):
            end_index = i.offset + i.length - 1
            if i.offset + i.length >= len(text_list):
                end_index = len(text_list) - 1
            if i.type != 'mention':
                tag = 'code'
                if i.type == 'bold':
                    tag = 'b'
                elif i.type == 'italic':
                    tag = 'i'
                elif i.type == 'text_link':
                    tag = 'a'
                elif i.type == 'underline':
                    tag = 'u'
                elif i.type == 'strikethrough':
                    tag = 's'
                if i.offset + i.length not in used_offsets or i.type == 'text_link':
                    text_list[end_index] += '</' + tag + '>'
                    if i.type == 'text_link':
                        tag = 'a href="' + i.url + '"'
                    text_list[i.offset] = '<' + tag + '>' + text_list[i.offset]
                    used_offsets.append(i.offset + i.length)
    new_text = ''.join(text_list) + text
    try:
        message = bot_start.edit_message_text(new_text, old_message.chat.id, old_message.message_id,
                                              disable_web_page_preview=True, parse_mode='HTML')
    except IndexError and Exception:
        new_text += italic('\nНе смог отредактировать сообщение. Отправлено новое')
        message = bot_start.send_message(idDevCentre, new_text, parse_mode='HTML')
    return message


def send_json(logs, name, error):
    json_text = ''
    if type(logs) is str:
        for character in logs:
            replaced = unidecode(str(character))
            if replaced != '':
                json_text += replaced
            else:
                try:
                    json_text += '[' + unicodedata.name(character) + ']'
                except ValueError:
                    json_text += '[???]'
    if json_text:
        doc = open(name + '.json', 'w')
        doc.write(json_text)
        doc.close()
        caption = None
        if len(error) <= 1024:
            caption = error
        doc = open(name + '.json', 'rb')
        bot_error.send_document(idDevCentre, doc, caption=caption, parse_mode='HTML')
    if (json_text == '' and 0 < len(error) <= 1024) or (1024 < len(error) <= 4096):
        bot_error.send_message(idDevCentre, error, parse_mode='HTML')
    elif len(error) > 4096:
        separator = 4096
        split_sep = len(error) // separator
        split_mod = len(error) / separator - len(error) // separator
        if split_mod != 0:
            split_sep += 1
        for i in range(0, split_sep):
            split_error = error[i * separator:(i + 1) * separator]
            if len(split_error) > 0:
                bot_error.send_message(idDevCentre, split_error, parse_mode='HTML')


def executive(logs):
    retry = 100
    func = None
    func_locals = []
    stack = inspect.stack()
    bot_name, host = get_bot_name()
    name = re.sub('[<>]', '', str(stack[-1][3]))
    exc_type, exc_value, exc_traceback = sys.exc_info()
    full_name = bold(bot_name) + '(' + code(host) + ').' + bold(name + '()')
    error_raw = traceback.format_exception(exc_type, exc_value, exc_traceback)
    printer('Вылет ' + re.sub('<.*?>', '', full_name) + ' ' + error_raw[-1])
    error = 'Вылет ' + full_name + '\n\n'
    for i in error_raw:
        error += html_secure(i)
    search_retry = re.search(search_retry_pattern, str(error))
    search_minor_fails = re.search(search_minor_fails_pattern, str(error))
    search_major_fails = re.search(search_major_fails_pattern, str(error))
    if search_retry:
        retry = int(search_retry.group(1)) + 10
    if search_minor_fails:
        retry = 10
        error = ''
    if search_major_fails:
        retry = 99
        error = ''

    if logs is None:
        caller = inspect.currentframe().f_back.f_back
        func_name = inspect.getframeinfo(caller)[2]
        for a in caller.f_locals:
            if a.startswith('host'):
                func_locals.append(caller.f_locals.get(a))
        func = caller.f_locals.get(func_name, caller.f_globals.get(func_name))
    else:
        retry = 0
    send_json(logs, name, error)
    return retry, func, func_locals, full_name


def send_starting_function(retry, name):
    if retry >= 100:
        bot_error.send_message(idDevCentre, 'Запущен ' + name, parse_mode='HTML')


def thread_exec(logs=None):
    retry, func, func_locals, full_name = executive(logs)
    sleep(retry)
    if func:
        try:
            _thread.start_new_thread(func, (*func_locals,))
        except IndexError and Exception as error:
            send_dev_message(full_name + ':\n' + error, code)
    send_starting_function(retry, full_name)
    _thread.exit()


async def async_exec(logs=None):
    retry, func, func_locals, full_name = executive(logs)
    await asyncio.sleep(retry)
    send_starting_function(retry, full_name)
