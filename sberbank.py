# -*- coding: utf-8 -*-

# api docs: s.sber.ru/7wZSW
#           https://www.sberbank.ru/common/img/uploaded/files/pdf/mob_ruk2.pdf

import messaging, appuifw, os.path, contacts

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
        appuifw.note(msg)

def balans():
    send_message(u"BALANS")
    
def last_ops():
    last_card_digits = appuifw.query(u'Последние 4 цифры номера карты:', 'number')
    if last_card_digits is None:
        return
    
    send_message(u"История " + ("%04d" % (last_card_digits,)))
    
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
    

appuifw.app.title = u'Сбербанк'
if is_debug():
    appuifw.app.title += u' [TEST MODE]'
    
choices = [u'Баланс карты', u'Последние операции', u'Пополнить свой моб. тел.',
           u'Перевести деньги на карту по номеру телефона']
index = appuifw.selection_list(choices)
if index==0:
    balans()
elif index==1:
    last_ops()
elif index==2:
    tel_pay()
elif index==3:
    transfer_to_card_by_phonenumber()

