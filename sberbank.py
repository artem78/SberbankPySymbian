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

import messaging, appuifw, os.path, contacts, e32
from ConfigParser import SafeConfigParser

PROG_VERSION = u'1.4.1'
LINE_BREAK = u'\r\n'
CONFIG_FILENAME = 'c:/data/sberpy.cfg'

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


cfg = SafeConfigParser({'last_ops_cardnumber': '0000'})
if os.path.exists(CONFIG_FILENAME):
    cfg.read(CONFIG_FILENAME)
else:
    cfg.add_section('main')

def is_debug():
    return os.path.exists("c:/sber.dbg")

def send_message(msg):
    msg = unicode(msg)
    if not is_debug():
        messaging.sms_send("900",msg)
    else:
        appuifw.note('>> ' + msg)

def balans():
    send_message(u"BALANS")
    Dialogs.wait_sms_response()
    
def last_ops():
    last_card_digits = cfg.getint('main', 'last_ops_cardnumber')
    last_card_digits = appuifw.query(u'Последние 4 цифры номера карты:', 'number',last_card_digits)
    if last_card_digits is None:
        return
    elif last_card_digits == 0 or last_card_digits > 9999:
        appuifw.note(u'Введите 4 цифры!', 'error')
        return

    send_message(u"HISTORY " + ("%04d" % (last_card_digits,)))
    Dialogs.wait_sms_response()

    # сохраняем в файл , если значение изменено
    if last_card_digits != cfg.getint('main', 'last_ops_cardnumber'):
        cfg.set('main', 'last_ops_cardnumber', str(last_card_digits))
        configfile = open(CONFIG_FILENAME, 'wb')
        cfg.write(configfile)
        del configfile
    
def tel_pay_own():
    sum = Dialogs.ask_sum()
    if not sum:
        return
    
    send_message(sum)
    
def tel_pay():
    phonenumber = Dialogs.ask_phonenumber()
    if not phonenumber:
        return
    
    sum = Dialogs.ask_sum()
    if not sum:
        return
    
    send_message(u"%s %d" % (phonenumber, sum))

    #Dialogs.confirm_with_sms()
    
def transfer_to_card_by_phonenumber():
    phonenumber = Dialogs.ask_phonenumber()
    if not phonenumber:
        return
    
    sum = Dialogs.ask_sum()
    if not sum:
        return
    
    send_message(u"PEREVOD %s %d" % (phonenumber, sum))

    Dialogs.confirm_with_sms()
    
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
    
    send_message(u"PEREVOD %s %d" % (card, sum))

    Dialogs.confirm_with_sms()
    
def show_about_dlg():
    txt = appuifw.Text()
    def_style = txt.style
    txt.style = appuifw.STYLE_BOLD
    txt.add(u'sberbank.py v' + PROG_VERSION + LINE_BREAK * 2)
    txt.style = def_style
    txt.add( u'Минималистичный клиент Сбербанка для symbian на питоне' + LINE_BREAK * 2)
    #txt.style = appuifw.STYLE_ITALIC
    txt.add(u'https://github.com/artem78/SberbankPySymbian' + LINE_BREAK * 2)
    txt.style = def_style
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
    send_message(u"PEREVOD %s %d" % (x, sum))

    Dialogs.confirm_with_sms()
    appuifw.note(u'Спасибо!')
    

appuifw.app.title = u'Сбербанк'
if is_debug():
    appuifw.app.title += u' [TEST MODE]'
appuifw.app.screen='normal'
    
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
