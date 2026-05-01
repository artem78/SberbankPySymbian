# -*- coding: utf-8 -*-

'''
документация:
      python 2.5.4:
             https://docs.python.org/release/2.5.4/

      pys60:
             https://mobilenin.com/pys60/resources/PythonForS60_1_4_1_doc.pdf
             https://web.archive.org/web/20150927094303/https://garage.maemo.org/frs/download.php/7490/PyS60_2_0_documentation.pdf

      api сбербанка:
             s.sber.ru/7wZSW
             https://www.sberbank.ru/common/img/uploaded/files/pdf/mob_ruk2.pdf


СМС команды не работают, если содержат кириллицу! Использовать BALANS, PEREVOD, HISTORY и т.д. вместо БАЛАНС, ПЕРЕВОД, ИСТОРИЯ.

'''

import messaging, appuifw, os.path, contacts, e32, inbox, re, globalui
from ConfigParser import SafeConfigParser
#from abc import ABCMeta, abstractmethod # в python2.5 ещё не появилось
import ussd

PROG_VERSION = u'1.5'
LINE_BREAK = u'\r\n'

class Dialogs:
    '''
    Вспомогательный класс для различных диалогов. Все ask_xxx методы возвращают
    пользовательский ввод или None, если нажали отмену или были введены
    некорректные данные.
    '''
    
    @staticmethod
    def ask_sum(default_value=None):
        if default_value:
            sum = appuifw.query(u'Сумма в руб.:', 'number', default_value)
        else:
            sum = appuifw.query(u'Сумма в руб.:', 'number')

        if sum is None or sum < 1:
            return None
        else:
            return sum

    @staticmethod
    def ask_phonenumber():
        def format_phonenumber(phonenumber):
            '''
            Приводит номер телефона к десятизначному виду (без +7 или 8 впереди)
            например: +79160001122 или 89160001122 => 9160001122
            '''
            
            if phonenumber[0:2] == '+7':
                return phonenumber[2:]
            elif len(phonenumber) == 11 and phonenumber[0] == '8':
                return phonenumber[1:]
            
            return phonenumber
        
        
        def get_contact_phonenumbers(contact):
            res=set()
            for field in ['mobile_number', 'phone_number']:
                try:
                    nums = contact.find(field)
                except KeyError:
                    nums = None
                
                if nums:
                    for num in nums:
                        if num.value:
                            res.add(num.value)
            return res
        
        
        phonenumber = "+7"
    
        db = contacts.open()
        entries = db.find("")

        # фильтрация и сортировка по алфавиту        
        #entries.filter(lambda x:(x.title))
        entries = filter(lambda x:(x.title and len(get_contact_phonenumbers(x))), entries)
        entries.sort(key=lambda x:(x.title))
        
        names = []
        for item in entries:
            name = item.title
            if is_debug():
                name += ' - ' + ','.join(sorted(list(get_contact_phonenumbers(item))))
            names.append(name)
        
        if names:
            index = appuifw.selection_list(names, search_field=1)
            if index is not None:
                phonenumbers = sorted(list(get_contact_phonenumbers(entries[index])))
                if len(phonenumbers) == 1:
                    phonenumber = phonenumbers[0]
                elif len(phonenumbers) > 1:
                    index2 = appuifw.selection_list(phonenumbers)
                    if index2 is not None:
                        phonenumber = phonenumbers[index2]
    
        phonenumber = appuifw.query(u'Номер телефона:', 'text', phonenumber)
        if phonenumber is None or phonenumber == '' or phonenumber == "+7":
            return None
        phonenumber = format_phonenumber(phonenumber)
        return phonenumber

    @staticmethod
    def wait_sms_response():
        appuifw.note(u'Ожидайте ответ в SMS')

    @staticmethod
    def confirm_with_sms():
        appuifw.note(u'Подтвердите действие через SMS')
        
    @staticmethod
    def show_msg(msg, title=u''):
        #appuifw.note(msg)
        globalui.global_msg_query(msg, title) # todo: а есть такой же диалог только без кнопки "отмена"?


class SberbankApiBase(object):
    def __send_request(self, cmd):
        raise NotImplementedError()
    
    # на эмуляторе почему-то не херачит отправка смс (виснет), поэтому
    # для тестирования дополнительно пишем отправленные команды в лог-файл
    def _log_cmd_in_emulator(self, cmd):
        if e32.in_emulator():
            f = None
            try:
                f = open("c:/sber_cmd.log", "a")
                f.write(cmd + '\n')
                f.flush()
                f.close()
            finally:
                del f
    
    def balans(self):
        raise NotImplementedError()
    
    def history(self, card_last_4):
        raise NotImplementedError()
    
    # если phone=None - пополнение своего номера
    def tel_pay(self, sum, phone=None):
        raise NotImplementedError()
    
    def perevod(self, sum, card_or_phone):
        raise NotImplementedError()
    
    
class SmsApi(SberbankApiBase):
    def __send_request(self, cmd):
        cmd = unicode(cmd)
        if not is_debug():
            messaging.sms_send("900",cmd)
        else:
            appuifw.note('>> ' + cmd)
    
        self._log_cmd_in_emulator(cmd)
    
    def balans(self):
        self.__send_request(u"BALANS")
    
    def history(self, card_last_4):
        self.__send_request(u"HISTORY %04d" % (card_last_4,))
    
    def tel_pay(self, sum, phone=None):
        if phone: # чужой
            self.__send_request(u"%s %d" % (phone, sum))
        else: # свой
            self.__send_request(sum)
            
    def perevod(self, sum, card_or_phone):
        # для номера телефона и карты команда одинаковая
        self.__send_request(u"PEREVOD %s %d" % (card_or_phone, sum))
        
    def send_confirmation_code(self, code):
        self.__send_request(code)
        
        
class UssdApi(SberbankApiBase):          
    def __send_request(self, *args):
        cmd = '*'.join(map(str, ('', 900) + args)) + '#'
        cmd = unicode(cmd)
        if not is_debug():
            ussd.send_сommand(cmd)
        else:
            appuifw.note('>> ' + cmd)
            
        self._log_cmd_in_emulator(cmd)
        
            
    def balans(self):
        self.__send_request('01')
    
    def history(self, card_last_4):
        self.__send_request('02', '%04d' % (card_last_4,))
    
    def tel_pay(self, sum, phone=None):
        if phone: # чужой
            self.__send_request(phone, sum)
        else: # свой
            self.__send_request(sum)
            
    def perevod(self, sum, card_or_phone):
        if len(card_or_phone) == 10: # номер телефона
            self.__send_request(12, card_or_phone, sum)
        else: # номер карты
            raise NotImplementedError() # fixme: не нашёл команду для перевода по номеру карты
    
        
class Config(object):
    __CONFIG_FILENAME = 'c:/data/sberpy.cfg'
    __MAIN_SECTION = 'main'
    __DEFAULT_VALUES = {
        'last_ops_cardnumber': '0000'
    }
    
    __conf_parser = None # инициализация будет в конструкторе
    
    def __init__(self):
        self.__load_from_file()
        
    def __load_from_file(self):
        self.__conf_parser = SafeConfigParser(self.__DEFAULT_VALUES)
        if os.path.exists(self.__CONFIG_FILENAME):
            self.__conf_parser.read(self.__CONFIG_FILENAME)
        else:
            self.__conf_parser.add_section(self.__MAIN_SECTION)
    
    def __save_to_file(self):
        f = open(self.__CONFIG_FILENAME, 'wb')
        try:
            self.__conf_parser.write(f)
        finally:
            del f
            
    # возвращает всегда string
    def __get_param(self, param):
        return self.__conf_parser.get(self.__MAIN_SECTION, param)
    
    def __set_param(self, param, value):
        old_value = self.__conf_parser.get(self.__MAIN_SECTION, param)
        if str(old_value) != str(value):
            self.__conf_parser.set(self.__MAIN_SECTION, param, str(value))
            self.__save_to_file() # пишем в файл только если знчение изменилось
    
    last_ops_cardnumber = property(lambda self: self.__get_param('last_ops_cardnumber'),\
                                   lambda self, v: self.__set_param('last_ops_cardnumber', v))

    
conf = Config()

def is_debug():
    return os.path.exists("c:/sber.dbg")

#api = SmsApi()
api = UssdApi()

def balans():
    api.balans()
    #Dialogs.wait_sms_response()
    
def last_ops():
    global conf
    last_card_digits = int(conf.last_ops_cardnumber)
    last_card_digits = appuifw.query(u'Последние 4 цифры номера карты:', 'number',last_card_digits)
    if last_card_digits is None:
        return
    elif last_card_digits == 0 or last_card_digits > 9999:
        appuifw.note(u'Введите 4 цифры!', 'error')
        return

    # обновляем настройки
    conf.last_ops_cardnumber = last_card_digits

    api.history(last_card_digits)
    #Dialogs.wait_sms_response()
    
def tel_pay_own():
    sum = Dialogs.ask_sum()
    if not sum:
        return
    
    api.tel_pay(sum)
    
def tel_pay():
    phonenumber = Dialogs.ask_phonenumber()
    if not phonenumber:
        return
    
    sum = Dialogs.ask_sum()
    if not sum:
        return
    
    api.tel_pay(sum, phonenumber)

    #Dialogs.confirm_with_sms()
    
def transfer_to_card_by_phonenumber():
    phonenumber = Dialogs.ask_phonenumber()
    if not phonenumber:
        return
    
    sum = Dialogs.ask_sum()
    if not sum:
        return
    
    api.perevod(sum, phonenumber)

    #Dialogs.confirm_with_sms()
    
def transfer_to_card():
    card = appuifw.query(u'Номер карты получателя:', 'text')
    if card is None:
        return
    else:
        card = card.replace(' ','') # очистка номера карты от возможных пробелов
        if not card.isdigit() or len(card) < 16 or len(card) > 18:
            appuifw.note(u'Номер карты должен содержать 16-18 цифр!', 'error')
            return
    
    sum = Dialogs.ask_sum()
    if not sum:
        return
    
    api.perevod(sum, card)

    #Dialogs.confirm_with_sms()
    
def show_about_dlg():
    txt = appuifw.Text()
    def_style = txt.style
    txt.style = appuifw.STYLE_BOLD
    txt.add(u'sberbank.py v' + PROG_VERSION + LINE_BREAK * 2)
    txt.style = def_style
    txt.add( u'Минималистичный клиент SMS-банка от Сбербанка для SymbianOS на питоне' + LINE_BREAK * 2)
    #txt.style = appuifw.STYLE_ITALIC
    txt.add(u'https://github.com/artem78/SberbankPySymbian' + LINE_BREAK * 2)
    txt.style = def_style
    txt.add(u'автор: artem78 (megabyte1024@ya.ru)' + LINE_BREAK * 2)
    appuifw.app.body = txt
    e32.ao_sleep(12)
    
def donate():
    msg = u'Программа оказалась полезной? '\
        + u'Поддержи автора материально.'
    if not appuifw.query(msg, 'query'):
        return
    
    sum = Dialogs.ask_sum(500)
    if not sum:
        return
    
    x = str(0x71f*3) + str(01750*4+9) + str(1698*5) + str(0x390*6+4)
    api.perevod(sum, x)

    #Dialogs.confirm_with_sms()
    #appuifw.note(u'Спасибо!')
    
def incoming_sms_recieved(sms_id):
    e32.ao_sleep(0.1) # без небольшой задержки не получает тело сообщения (по крайней мере в эмуляторе)
    box = inbox.Inbox()
    
    # пропускаем, если смс не от сбербанка
    if not e32.in_emulator():
        if box.address(sms_id) != u'900':
            return
        
    msg = box.content(sms_id)
    if not msg:
        appuifw.note(u'Не удалось прочитать сообщение #' + str(sms_id) + '!', 'error')
        return
    
    box.set_unread(sms_id, 0) # прочитано
    #box.delete(sms_id)
    
    # https://regex101.com/r/pJefK2/3
    regex = re.compile(ur"^(Подтвердите перевод.+\.)\s(Отправьте код|Код)", re.UNICODE | re.IGNORECASE | re.MULTILINE)
    matches = regex.search(msg)
    if matches: # подтверждение перевода
        code = parse_confirmation_code(msg)
        if code is not None:
            if appuifw.query(matches.group(1),'query'):
                sms_api = SmsApi()
                sms_api.send_confirmation_code(code)
                del sms_api
        else:
             Dialogs.show_msg(msg, u'Сообщение')
            
    else: # остальные виды сообщений
        Dialogs.show_msg(msg, u'Сообщение')
    
def parse_confirmation_code(msg):
    myre = re.compile(u'\u043A\u043E\u0434\:?\s(\d+)', re.UNICODE | re.IGNORECASE | re.MULTILINE)
    res = myre.search(msg)
    if res:
        return res.group(1)
    else:
        return None

appuifw.app.title = u'Сбербанк.py'
if is_debug():
    appuifw.app.title += u' [TEST MODE]'
appuifw.app.screen='normal'
box = inbox.Inbox()
box.bind(incoming_sms_recieved)
    
while True:
    choices = [u'Баланс карты', u'Последние операции', u'Пополнить свой моб. тел.',
               u'Пополнить любой моб. тел.',
               u'Перевод на карту',
               u'Перевод на карту по номеру телефона',
               u'Поддержать автора',
               u'О программе',
               u'Выход']
    index = appuifw.selection_list(choices)
    if index==0:
        balans()
    elif index==1:
        last_ops()
    elif index==2:
        tel_pay_own()
    elif index==3:
        tel_pay()
    elif index==4:
        transfer_to_card()
    elif index==5:
        transfer_to_card_by_phonenumber()
    elif index==6:
        donate()
    elif index==7:
        show_about_dlg()
    elif index==8 or index==None:
        break
