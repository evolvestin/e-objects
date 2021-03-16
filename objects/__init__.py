import os
import re
import sys
import time
import base64
import codecs
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

host = 'Unknown'
app_name = 'Undefined'
log_file_name = 'log.txt'
sql_patterns = ['database is locked', 'disk image is malformed', 'no such table']
search_retry_pattern = r'Retry in (\d+) seconds|"Too Many Requests: retry after (\d+)"'
week = {'Mon': 'Пн', 'Tue': 'Вт', 'Wed': 'Ср', 'Thu': 'Чт', 'Fri': 'Пт', 'Sat': 'Сб', 'Sun': 'Вс'}
search_major_fails_pattern = 'The (read|write) operation timed out|Backend Error|is currently unavailable.'
search_minor_fails_pattern = 'Failed to establish a new connection|Read timed out.|ServerDisconnectedError' \
                             '|Message_id_invalid|Connection aborted'


if os.environ.get('api'):
    for app in heroku3.from_key(os.environ.get('api')).apps():
        if app.name.endswith('first'):
            host = 'One'
        if app.name.endswith('second'):
            host = 'Two'
        app_name = re.sub('-first|-second', '', app.name, 1)


def bold(text):
    return '<b>' + str(text) + '</b>'


def under(text):
    return '<u>' + str(text) + '</u>'


def italic(text):
    return '<i>' + str(text) + '</i>'


def code(text):
    return '<code>' + str(text) + '</code>'


def time_now():
    return int(datetime.now().timestamp())


def html_link(link, text):
    return '<a href="' + str(link) + '">' + str(text) + '</a>'


def sql_divide(array):
    return [array[i:i + 1000] for i in range(0, len(array), 1000)]


def html_secure(text):
    response = re.sub('<', '&#60;', str(text))
    response = re.sub('[{]', '&#123;', response)
    return re.sub('[}]', '&#125;', response)


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


def environmental_files(python=False, return_all_json=True):
    created_files = []
    directory = os.listdir('.')
    for key in os.environ.keys():
        key = key.lower()
        if key.endswith('.json'):
            if return_all_json:
                created_files.append(key)
            if key not in directory:
                file = open(key, 'w')
                file.write(os.environ.get(key))
                if return_all_json in [False, None]:
                    created_files.append(key)
                file.close()
        if key.endswith('.py') and python is True:
            with codecs.open(key, 'w', 'utf-8') as file:
                file.write(base64.b64decode(os.environ.get(key)).decode('utf-8'))
                file.close()
    return created_files


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
    if form in ['b_channel', 'channel']:
        response = day + '/' + month + '/' + year + ' ' + hour + ':' + minute
    elif form in ['au_normal', 'normal']:
        response = day + '.' + month + '.' + year + ' ' + hour + ':' + minute
    if form in ['channel', 'normal']:
        response += ':' + second
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


class AuthCentre:
    def __init__(self, token, dev_chat_id=None):
        self.token = token
        self.dev_chat_id = -1001312302092
        if dev_chat_id:
            self.dev_chat_id = dev_chat_id
        self.bot = telebot.TeleBot(token)
        self.get_me = literal_eval(str(self.bot.get_me()))

    def send_dev_message(self, text, tag=code):
        if tag:
            text = tag(html_secure(text))
        text = bold(app_name) + ' (' + code(host) + '):\n' + text
        message = self.bot.send_message(self.dev_chat_id, text, disable_web_page_preview=True, parse_mode='HTML')
        return message

    def start_message(self, stamp, text=None):
        bot_linked_name = html_link('https://t.me/' + str(self.get_me.get('username')), bold(app_name))
        head = bot_linked_name + ' (' + code(host) + '):\n' + \
            log_time(stamp, code) + '\n' + log_time(tag=code)
        start_text = ''
        if text:
            start_text = '\n' + str(text)
        text = head + start_text
        message = self.bot.send_message(self.dev_chat_id, text, disable_web_page_preview=True, parse_mode='HTML')
        return message

    def start_main_bot(self, library):
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
            return aiogram.Bot(self.token)
        else:
            return telebot.TeleBot(self.token)

    def edit_dev_message(self, old_message, text):
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
            message = self.bot.edit_message_text(new_text, old_message.chat.id, old_message.message_id,
                                                 disable_web_page_preview=True, parse_mode='HTML')
        except IndexError and Exception:
            new_text += italic('\nНе смог отредактировать сообщение. Отправлено новое')
            message = self.bot.send_message(self.dev_chat_id, new_text, parse_mode='HTML')
        return message

    # =============================================================================================================
    # ================================================  EXECUTIVE  ================================================
    # =============================================================================================================

    def executive(self, logs):
        retry = 100
        func = None
        func_locals = []
        stack = inspect.stack()
        name = re.sub('[<>]', '', str(stack[-1][3]))
        exc_type, exc_value, exc_traceback = sys.exc_info()
        full_name = bold(app_name) + '(' + code(host) + ').' + bold(name + '()')
        error_raw = traceback.format_exception(exc_type, exc_value, exc_traceback)
        printer('Вылет ' + re.sub('<.*?>', '', full_name) + ' ' + re.sub('\n', '', error_raw[-1]))
        error = 'Вылет ' + full_name + '\n\n'
        for i in error_raw:
            error += html_secure(i)
        search_retry = re.search(search_retry_pattern, str(error))
        search_minor_fails = re.search(search_minor_fails_pattern, str(error))
        search_major_fails = re.search(search_major_fails_pattern, str(error))
        if search_retry:
            retry = int(search_retry.group(1)) + 10
        if search_minor_fails:
            logs = None
            retry = 10
            error = ''
        if search_major_fails:
            logs = None
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
        self.send_json(logs, name, error)
        return retry, func, func_locals, full_name

    def send_json(self, logs, name, error):
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
            self.bot.send_document(self.dev_chat_id, doc, caption=caption, parse_mode='HTML')
        if (json_text == '' and 0 < len(error) <= 1024) or (1024 < len(error) <= 4096):
            self.bot.send_message(self.dev_chat_id, error, parse_mode='HTML')
        elif len(error) > 4096:
            separator = 4096
            split_sep = len(error) // separator
            split_mod = len(error) / separator - len(error) // separator
            if split_mod != 0:
                split_sep += 1
            for i in range(0, split_sep):
                split_error = error[i * separator:(i + 1) * separator]
                if len(split_error) > 0:
                    self.bot.send_message(self.dev_chat_id, split_error, parse_mode='HTML')

    def thread_exec(self, logs=None):
        retry, func, func_locals, full_name = self.executive(logs)
        sleep(retry)
        if func:
            try:
                _thread.start_new_thread(func, (*func_locals,))
            except IndexError and Exception as error:
                self.send_dev_message(full_name + ':\n' + error, code)
        if retry >= 100:
            self.bot.send_message(self.dev_chat_id, 'Запущен ' + full_name, parse_mode='HTML')
        _thread.exit()

    async def async_exec(self, logs=None):
        retry, func, func_locals, full_name = self.executive(logs)
        await asyncio.sleep(retry)
        if retry >= 100:
            self.bot.send_message(self.dev_chat_id, 'Запущен ' + full_name, parse_mode='HTML')
