import time
import random
import vk_advanced_api
import vkcoin
import json
import sys

from tkinter import *
from tkinter import messagebox, Frame
from threading import *

check_auth = False

version = ' v0.2'
balance = 0

window = Tk()  # Для tkinter'a
window.title("VKCoin Reborn" + version)  # Название GUI-окна.
window.geometry('370x440')  # Разрешение GUI-окна

# Строка: данные #
inform = Label(window, text='———  Ваши данные  ————————————————————')
inform.place(x=0, y=0)
# Строка: данные #

# Оформление с строкой для: Token VK #
tokenlabel = Label(window, text="Ваш токен ВКонтакте:")
tokenlabel.place(x=5, y=18)
tokentxt = Entry(window, width=37)
tokentxt.place(x=135, y=18)
# Оформление с строкой для: Token VK #

# Оформление с строкой для: API Key (RuCaptcha) #
rucaptchalabel = Label(window, text="API Key (RuCaptcha):")
rucaptchalabel.place(x=8, y=38)
rucaptchatxt = Entry(window, width=37)
rucaptchatxt.place(x=135, y=38)
# Оформление с строкой для: API Key (RuCaptcha) #

# Оформление с строкой для: API Key (VKCoin) #
vkcoinlabel = Label(window, text="API Key (VKCoin):")
vkcoinlabel.place(x=18, y=58)
vkcoinlabel = Entry(window, width=37)
vkcoinlabel.place(x=135, y=58)
# Оформление с строкой для: API Key (VKCoin) #

# Строка: информация #
informdate = Label(window, text='———  Информация  ————————————————————')
informdate.place(x=0, y=80)
# Строка: информация #

# Строка: функции #
informdate = Label(window, text='———  Функции   ——————————————————————')
informdate.place(x=0, y=120)


# Строка: функции #

def funcfirststart():
    global check_auth
    if check_auth == True:
        thread1.start()
        messagebox.showinfo(time.strftime("%H:%M:%S |") + " Уведомление", "Майнинг запущен успешно!")
    else:
        messagebox.showinfo(time.strftime("%H:%M:%S |") + " Уведомление",
                            "Майнинг не запущен, по скольку вы не авторизованы")


def funcstop():
    sys.exit()


def funcdrop():
    if check_auth:
        utils.messages.send(peer_id=-167822712, random_id=random.randint(0, 10000),
                            message='Вывести коины на кошелек VK Coins',
                            payload='"drop"')
        messagebox.showinfo(time.strftime("%H:%M:%S |") + " Уведомление",
                            "Коины успешно выведены и ждут Вас, на Вашем кошельке VKCoin.'")
    else:
        messagebox.showinfo(time.strftime("%H:%M:%S |") + " Уведомление",
                            "Требуется авторизоваться!")


def funcauth():
    global tokeninfo, rucaptchainfo, api, utils, useridnormal, vkcointoken, transferid, transfermoney, check_auth
    tokeninfo = tokentxt.get()
    rucaptchainfo = rucaptchatxt.get()
    transfermoney = transferlabelmoney.get()
    if tokeninfo != '' and rucaptchainfo != '' and vkcoinlabel.get() != '':
        api = vk_advanced_api.VKAPI(
            access_token=tokeninfo,
            captcha_key=rucaptchainfo,
            version=5.71,
            warn_level=1
        )
        utils = api.utils
        userid = utils.users.get()
        global useridnormal, merchant
        useridnormal = userid[0]['id']
        print(vkcoinlabel.get(), useridnormal)
        merchant = vkcoin.Merchant(user_id=int(useridnormal), key=vkcoinlabel.get())
        messagebox.showinfo(time.strftime("%H:%M:%S |") + " Уведомление",
                            "Авторизация прошла успешна, можете начинать майнинг.")
        check_auth = True
    else:
        messagebox.showinfo(time.strftime("%H:%M:%S |") + " Уведомление",
                            "Требуется ввести данные!")


def functransfer():
    if transferlabel.get() != '' and transferlabelmoney.get() != '':
        result = merchant.send(amount=int(transferlabelmoney.get()), to_id=int(transferlabel.get()))
    else:
        messagebox.showinfo(time.strftime("%H:%M:%S |") + " Уведомление",
                            "Требуется ввести данные!")


def funcautotransfer():
    while True:
        result = merchant.send(amount=int(transferlabelmoney.get()), to_id=int(transferlabel.get()))
        time.sleep(int(spinbox.get()) * 60)


def funcgetbal():
    global balancetrue
    balanceget = []
    balanceget.append(int(useridnormal))
    result = merchant.get_balance(user_ids=balanceget)
    json_data = json.dumps(result)
    parsed_json = json.loads(json_data)
    balancetrue = parsed_json['response'][str(useridnormal)] / 1000
    inform.config(text='Ваш баланс: ' + str(balancetrue) + ' VKCoins')


def startbot():
    counter = 0
    stringcounter = 'Клик (у тебя '
    stringcounter1 = '+ кликов)'
    while True:
        utils.messages.send(peer_id=-167822712, random_id=random.randint(0, 10000),
                            message=stringcounter + str(counter) + stringcounter1,
                            payload='"tap"')
        counter += 1
        funcgetbal()
        time.sleep(5)


# Строка: баланс #
inform = Label(window, text='Ваш баланс: ' + "0" + ' VKCoins')
inform.place(x=5, y=100)
# Строка: баланс #

# Кнопка: начать добывать коины #
btnstart = Button(window, text="Начать добывать коины", command=funcfirststart, width=50, height=0)
btnstart.grid(column=4, row=0)
btnstart.place(x=5, y=145)
# Кнопка: начать добывать коины #

# Кнопка: закрыть приложение #
btnstart = Button(window, text="Закрыть приложение", command=funcstop, width=50, height=0)
btnstart.grid(column=4, row=0)
btnstart.place(x=5, y=170)
# Кнопка: закрыть приложение #

# Кнопка: аутентификация #
btnstart = Button(window, text="Аутентификация", command=funcauth, width=50, height=0)
btnstart.grid(column=4, row=0)
btnstart.place(x=5, y=195)
# Аутентификация #

# Кнопка: вывод средств #
btnstart = Button(window, text="Вывод средств", command=funcdrop, width=50, height=0)
btnstart.grid(column=4, row=0)
btnstart.place(x=5, y=220)
# Кнопка: вывод средств #

# Строка: автоперевод #
automoneylabel = Label(window, text='———  Авто-перевод  ———————————————————')
automoneylabel.place(x=5, y=250)
# Строка: автоперевод #

# Строка: FAQ для автоперевода #
automoneylabel = Label(window, text='Интервал перевода (в минутах) │ ID пользователя ВКонтакте')
automoneylabel.place(x=5, y=268)
# Строка: FAQ для автоперевода #

# Строка: ID для перевода денег #
transferlabel = Entry(window, width=28)
transferlabel.grid(column=2, row=0)
transferlabel.place(x=191, y=290)
# Строка: ID для перевода денег #

# Строка: FAQ для автоперевода [x2] #
automoneylabel = Label(window, text='Количество VKCoinов которые перейдут другому пользователю')
automoneylabel.place(x=5, y=310)
# Строка: FAQ для автоперевода [x2] #

# Строка: кол-ва денег для авто-перевода #
transferlabelmoney = Entry(window, width=59)
transferlabelmoney.grid(column=2, row=0)
transferlabelmoney.place(x=5, y=332)
# Строка: кол-ва денег для авто-перевода #

# Спинбокс: ID аккаунта для перевода #
spinbox = Spinbox(window, width=28, from_=0, to=99999999)
spinbox.place(x=6, y=290)
# Спинбокс: ID аккаунта для перевода #

# Кнопка: перевести #
btntransfer = Button(window, text="Перевести", width=50, height=0, command=functransfer)
btntransfer.place(x=5, y=355)
# Кнопка: перевести #

# Чек-кпопка: включение авто-перевода #
check = Checkbutton(window, text=u'Включить авто-перевод', command=funcautotransfer)
check.place(x=2, y=382)
# Чек-кпопка: включение авто-перевода #

# Строка: пустая строка #
nolabel = Label(window, text='——————————————————————————————')
nolabel.place(x=5, y=402)
# Строка: пустая строка #

# Строка: Copyright #
copyright = Label(window,
                  text='                                                                    VKCoin Reborn Team‎ © 2019')
copyright.place(x=5, y=418)
# Строка: Copyright #

thread1 = Thread(target=startbot)  # Для потоков
window.resizable(False, False)  # Запрет на расширение окна
window.mainloop()  # Вывод окна
