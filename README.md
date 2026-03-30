# <img src="icon.svg" width="48"/> sberbank.py

Минималистичный СМС-клиент Сбербанка для Symbian (s60v3 - s60v5) на питоне.

![](Snap4244.jpg)

*( ! ) Для работы требуется подключённый к номеру SMS-банк (http://s.sber.ru/7wZSW).*

# Возможности
- Просмотр баланса карты
- Просмотр последних операций по карте (мини-выписка)
- Пополнение телефона
- Перевод на другую карту
- Не требует наличие интернета (достаточно сотовой сети для отправки SMS-запросов)

# Установка

Установить пакет [sberbank_vX_X_X.sis](https://github.com/artem78/SberbankPySymbian/releases/latest)

## Альтернативный вариант

1) Установить [Python for Symbian (PyS60)](https://sourceforge.net/projects/pys60/files/pys60/1.4.5/) -  PythonForS60_xxx.sis и PythonScriptShell_xxx.SIS ([инструкция](https://www.mobilenin.com/pys60/pys60_installation_resources.php))
2) Сохранить файл sberbank.py в папку e:/data/python на телефоне
3) Запустить PythonScriptShell
4) Options -> Run script и выбрать файл e:sberbank.py

# Использование

Программа работает путём отправки sms сообщений на короткий номер 900 ([sms-банк Сбербанка](https://www.sberbank.ru/common/img/uploaded/files/pdf/mob_ruk2.pdf])). Например, перевод на карту с номером 0000 1111 2222 3333 суммы в 2500 рублей производится отправкой следующего сообщения:

```
PEREVOD 0000111122223333 2500
```

Ответ (мини-выписка, баланс) также приходит в виде sms.

[Примеры смс запросов и ответов.](/sms_samples/samples.md)

*Для некоторых действий (например, перевод на карту) потребуется вручную отправить подтверждение через sms*.
