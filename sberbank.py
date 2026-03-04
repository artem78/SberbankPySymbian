# -*- coding: utf-8 -*-

# документация:
#      python 2.5.4:
#             https://docs.python.org/release/2.5.4/
#
#      pys60:
#             https://mobilenin.com/pys60/resources/PythonForS60_1_4_1_doc.pdf
#             https://web.archive.org/web/20150927094303/https://garage.maemo.org/frs/download.php/7490/PyS60_2_0_documentation.pdf
#
#      api сбербанка:
#             s.sber.ru/7wZSW
#             https://www.sberbank.ru/common/img/uploaded/files/pdf/mob_ruk2.pdf

import messaging, appuifw, os.path, contacts

PROG_VERSION = u'1.0'

def is_debug():
    return os.path.exists("c:/sber.dbg")

def format_phonenumber(phonenumber):
    # drop leading +7 or 8 ( +79160001122 or 89160001122 to 9160001122 )
    if phonenumber[0:2] == '+7':
        return phonenumber[2:]
    elif len(phonenumber) == 11 and phonenumber[0] == '8':
        return phonenumber[1:]
    
    return phonenumber

def send_message(msg):
    if not is_debug():
        messaging.sms_send("900",msg)
    else:
        appuifw.note('>> ' + msg)

def balans():
    send_message(u"BALANS")
    appuifw.note(u'Ожидайте ответа в SMS')
    
def last_ops():
    last_card_digits = appuifw.query(u'Последние 4 цифры номера карты:', 'number')
    if last_card_digits is None:
        return
    
    send_message(u"История " + ("%04d" % (last_card_digits,)))
    appuifw.note(u'Ожидайте ответа в SMS')
    
def tel_pay():
    sum = appuifw.query(u'Сумма в руб.:', 'number')
    if sum is None or sum < 1:
        return
    
    send_message(str(sum))
    
def transfer_to_card_by_phonenumber():
    phonenumber = "+7"
    
    db = contacts.open()
    entries = db.find("")
    names = []
    for item in entries:
        names.append(item.title)
    if names:
        index = appuifw.selection_list(names, search_field=1)
        if index:
            num = entries[index].find('mobile_number')
            if num:
                phonenumber = num[0].value
    
    phonenumber = appuifw.query(u'Номер телефона:', 'text', phonenumber)
    if phonenumber is None or phonenumber == '' or phonenumber == "+7":
        return
    phonenumber = format_phonenumber(phonenumber)
    
    sum = appuifw.query(u'Сумма в руб.:', 'number')
    if sum is None or sum < 1:
        return
    
    send_message(u"PEREVOD %s %d" % (phonenumber, sum))

    appuifw.note(u'Подтвердите действие через SMS')
    
def transfer_to_card():
    card = appuifw.query(u'Номер карты получателя:', 'text')
    if card is None:
        return
    if not card.isdigit() or len(card) < 16 or len(card) > 18:
        appuifw.note(u'Номер карты должен содержать 16-18 цифр!', 'error')
        return
    
    sum = appuifw.query(u'Сумма в руб.:', 'number')
    if sum is None or sum < 1:
        return
    
    send_message(u"PEREVOD %s %d" % (card, sum))

    appuifw.note(u'Подтвердите действие через SMS')
    
def show_about_dlg():
    msg = u'sberbank.py v' + PROG_VERSION + u'\r\n'\
        + u'Минималистичный клиент Сбербанка для symbian на питоне'
    appuifw.note(msg)
    

appuifw.app.title = u'Сбербанк'
if is_debug():
    appuifw.app.title += u' [TEST MODE]'
    
while True:
    choices = [u'Баланс карты', u'Последние операции', u'Пополнить свой моб. тел.',
               u'Перевод на карту',
               u'Перевод на карту по номеру телефона', u'О программе',
               u'Выход']
    index = appuifw.selection_list(choices)
    if index==0:
        balans()
    elif index==1:
        last_ops()
    elif index==2:
        tel_pay()
    elif index==3:
        transfer_to_card()
    elif index==4:
        transfer_to_card_by_phonenumber()
    elif index==5:
        show_about_dlg()
    elif index==6:
        break
