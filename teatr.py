__author__ = 'Константин'

from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox

from PIL import ImageTk, Image
from os import startfile

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from datetime import datetime

import pyodbc

global zal
global bilets
global color_mesto

cnxn = pyodbc.connect(
    'DRIVER={SQL Server};SERVER=(local);DATABASE={name_of_DB}')
cursor = cnxn.cursor()

date_now = (str(datetime.today().date())[5:7])
time_now = (str(datetime.today().time())[:5])


class Mesto:
    def __init__(self, _root, a, b, price, text="", width=3, height=1):
        self.but = Button(_root)
        self.but['text'] = text
        self.but.bind("<Button-1>", self.sell)
        self.but.bind("<Button-3>", self.bron)
        self.but['bg'] = color_mesto
        self.but['width'] = width
        self.but.a = str(a)
        self.but.b = str(b)
        self.but.price = price
        self.but['height'] = height
        self.but.grid(row=a, column=b, padx=5, pady=5)

    def sell(self, event):
        if self.but['bg'] != "gray" and self.but['bg'] != "darkblue":
            self.but['bg'] = "red"
            self.but['fg'] = "black"
            name = 'Ряд: ' + self.but.a + ' , Место: ' + str(
                self.but['text']) + ', Цена: ' + str(self.but.price)

            if name not in listshop.get(0, END):
                listshop.insert(END, name)
                lol = list(listshop.get(0, END))
                lab_co['text'] = len(lol)
                lab_s['text'] = str(int(lab_s['text']) + self.but.price)

    def bron(self, event):
        if self.but['bg'] != "gray" and self.but['bg'] != "darkblue":
            self.but['bg'] = "black"
            self.but['fg'] = "white"
            name = 'Ряд: ' + self.but.a + ' , Место: ' + str(
                self.but['text']) + ', Цена: ' + str(self.but.price)

            if name not in listshop.get(0, END):
                listshop.insert(END, name)
                lol = list(listshop.get(0, END))
                lab_co['text'] = len(lol)
                lab_s['text'] = str(int(lab_s['text']) + self.but.price)

    def delete(self):
        self.but.grid_forget()


class CreateHall():
    def __init__(self):
        self.all = []

    def create(self):
        num = 0
        parter1 = []

        for i in range(1, 3):
            for k in range(1, 21):
                num += 1
                parter1.append(Mesto(fr_par1, i, k, price=0, text=num))

        parter2 = []
        for i in range(3, 5):
            for k in range(1, 21):
                num += 1
                parter2.append(Mesto(fr_par2, i, k, price=0, text=num))

        parter3 = []
        for i in range(5, 7):
            for k in range(1, 21):
                if k in range(8, 14) and i == 5:
                    parter3.append(Mesto(fr_par3, i, k, price=0, text='0'))
                else:
                    num += 1
                    parter3.append(Mesto(fr_par3, i, k, price=0, text=num))

        for i in range(7, 13):
            parter3[i].delete()

        parter4 = []
        for i in range(7, 9):
            for k in range(1, 21):
                if k in range(5, 17) and i == 7:
                    parter4.append(Mesto(fr_par4, i, k, price=0, text='0'))
                else:
                    num += 1
                    parter4.append(Mesto(fr_par4, i, k, price=0, text=num))

        for i in range(4, 16):
            parter4[i].delete()

        for each in parter1, parter2, parter3, parter4:
            self.all.append(each)

    def return_all(self):
        return self.all

    def right_start(self, s, b):
        seans_id = str(select_q(
            "Select id from Seans where date = "
            + "'" + combo_date.get() + "'" + " and time ="
            + "'" + combo_time.get() + "'" + "and id_spek ="
            + str(select_q("Select id from Spektakl where name ="
                           + "'" + combobox.get() + "'")[0]))[0])
        one = select_q("select one from Seans where id=" + seans_id)[0]
        two = select_q("select two from Seans where id=" + seans_id)[0]
        three = select_q("select three from Seans where id=" + seans_id)[0]
        four = select_q("select four from Seans where id=" + seans_id)[0]

        for i in range(4):
            for each in self.all[i]:
                if i == 0:
                    each.but.price = one
                elif i == 1:
                    each.but.price = two
                elif i == 2:
                    each.but.price = three
                elif i == 3:
                    each.but.price = four

                if each.but['text'] in s:
                    each.but['bg'] = 'gray'

                elif each.but['text'] in b:
                    each.but['bg'] = 'darkblue'
                    each.but['fg'] = 'white'
                else:
                    each.but['bg'] = color_mesto
                    each.but['fg'] = 'black'
        price1['text'] = one
        price2['text'] = two
        price3['text'] = three
        price4['text'] = four

    def antibron(self, numbers):
        for i in range(4):
            for each in self.all[i]:
                if each.but['text'] in numbers:
                    name = 'Ряд: ' + each.but.a + ' , Место: ' + str(
                        each.but['text']) + ', Цена: ' + str(each.but.price)
                    if name not in listshop.get(0, END):
                        listshop.insert(END, name)
                        lol = list(listshop.get(0, END))
                        lab_co['text'] = len(lol)
                        lab_s['text'] = str(
                            int(lab_s['text']) + each.but.price)

    def antibron_true(self, numbers):
        bilets = []
        bilet = {}
        name_spek = combobox.get()
        data_spek = combo_date.get()
        time_spek = combo_time.get()
        try:
            for i in range(4):
                for each in zal.return_all()[i]:
                    for num in numbers:
                        if each.but['text'] == num:
                            bilet["nomer"] = each.but['text']
                            if i == 0 or i == 1:
                                bilet["ryad"] = each.but.a
                                bilet["mesto"] = "Партер"
                            elif i == 2:
                                bilet['ryad'] = each.but.a
                                bilet["mesto"] = "2 этаж"
                            elif i == 3:
                                bilet['ryad'] = each.but.a
                                bilet["mesto"] = "3 этаж"

                            bilet["price"] = each.but.price
                            bilet["spektakl"] = name_spek
                            bilet["data"] = data_spek
                            bilet["time"] = time_spek
                            bilets.append(bilet.copy())
                            bilet.clear()

            create_bilet(bilets)

            for i in range(4):
                for each in zal.return_all()[i]:
                    for num in numbers:
                        if each.but['text'] == num:
                            each.but['bg'] = 'gray'
                            each.but['fg'] = 'black'

                            insert_q(
                                "insert into Bilet(id_seans,nomer) values ("
                                + "'"
                                + str(select_q(
                                    "Select id from Seans where date = "
                                    + "'" + combo_date.get() + "'"
                                    + " and time =" \
                                    + "'" + combo_time.get() + "'"
                                    + "and id_spek =" \
                                    + str(select_q(
                                        "Select id from Spektakl where name ="
                                        + "'" + combobox.get() + "'")[0]))[
                                          0]) + "'" + "," + str(num) + ")")

                            delete_q("delete from Bron where id_seans = "
                                     + str(select_q(
                                "Select id from Seans where date = " + "'"
                                + combo_date.get() + "'" + " and time ="
                                + "'" + combo_time.get() + "'"
                                + "and id_spek ="
                                + str(select_q(
                                    "Select id from Spektakl where name ="
                                    + "'" + combobox.get() + "'")[
                                          0]))[0]) + " and nomer =" + str(num))
                            total(each.but.price)

            messagebox.showinfo('Success', 'Бронь снята и билеты проданы.')
            antibron_text.delete(0, END)
            startfile('bilets.pdf')
        except Exception as e:
            print(e)
            messagebox.showerror('Error',
                                 'Возникла ошибка. Закройте файл bilets.pdf')


def clear(event):
    listshop.delete(0, END)
    lab_co['text'] = ''
    lab_s['text'] = '0'
    antibron_text.delete(0, END)
    for i in range(4):
        for each in zal.return_all()[i]:
            if each.but['bg'] == 'red' or each.but['bg'] == 'black':
                each.but['bg'] = color_mesto
                each.but['fg'] = 'black'
    input_name.place_forget()


def proverka(event, color):
    for i in range(4):
        for each in zal.return_all()[i]:
            if each.but['bg'] == color:
                clear(event)
                return 0
    else:
        return 1


def total(price):
    if str(select_q("select id from Sell where id_seans ="
                            + str(select_q("Select id from Seans where date = "
                                                   + "'" + combo_date.get()
                                                   + "'" + " and time ="
                                                    + "'" + combo_time.get()
                                                   + "'" + "and id_spek ="
                    + str(select_q(
                                        "Select id from Spektakl where name ="
                                                + "'" + combobox.get() + "'")[
                              0]))[0]))) == '[]':
        insert_q(
            "insert into Sell(id_seans,total_money,kol_biletov) values (" + "'" \
            + str(select_q(
                "Select id from Seans where date = " + "'" + combo_date.get() + "'" + " and time =" \
                + "'" + combo_time.get() + "'" + "and id_spek =" \
                + str(select_q("Select id from Spektakl where name =" \
                               + "'" + combobox.get() + "'")[0]))[
                      0]) + "'" + "," + "'0','0')")

    seans_id = str(select_q(
        "Select id from Seans where date = " + "'" + combo_date.get() + "'" + " and time =" \
        + "'" + combo_time.get() + "'" + "and id_spek =" \
        + str(select_q("Select id from Spektakl where name =" \
                       + "'" + combobox.get() + "'")[0]))[0])

    total_money = int(select_q(
        "select Sell.total_money from Sell,Seans where Seans.id = Sell.id_seans and Sell.id_seans=" + "'" + seans_id + "'")[
                          0]) + int(price)
    kol_biletov = int(select_q(
        "select Sell.kol_biletov from Sell,Seans where Seans.id = Sell.id_seans and Sell.id_seans=" + "'" + seans_id + "'")[
                          0]) + 1

    update_q("update sell set total_money =" + "'" + str(
        total_money) + "'" + ", kol_biletov=" + "'" + str(
        kol_biletov) + "'" + "where id_seans=" + "'" \
             + seans_id + "'")


def sell(event):
    bilets = []
    bilet = {}
    name_spek = combobox.get()
    data_spek = combo_date.get()
    time_spek = combo_time.get()
    if proverka(event, 'black') == 1:
        if messagebox.askokcancel('Подтверждение', 'Вы уверены?'):
            try:
                for i in range(4):
                    for each in zal.return_all()[i]:
                        if each.but['bg'] == 'red':
                            bilet["nomer"] = each.but['text']
                            if i == 0 or i == 1:
                                bilet["ryad"] = each.but.a
                                bilet["mesto"] = "Партер"
                            elif i == 2:
                                bilet['ryad'] = each.but.a
                                bilet["mesto"] = "2 этаж"
                            elif i == 3:
                                bilet['ryad'] = each.but.a
                                bilet["mesto"] = "3 этаж"

                            bilet["price"] = each.but.price
                            bilet["spektakl"] = name_spek
                            bilet["data"] = data_spek
                            bilet["time"] = time_spek
                            bilets.append(bilet.copy())
                            bilet.clear()

                create_bilet(bilets)

                for i in range(4):
                    for each in zal.return_all()[i]:
                        if each.but['bg'] == 'red':
                            s = "insert into Bilet(id_seans,nomer) values (" + "'" \
                                + str(select_q(
                                "Select id from Seans where date = " + "'" + combo_date.get() + "'" + " and time =" \
                                + "'" + combo_time.get() + "'" + "and id_spek =" \
                                + str(select_q(
                                    "Select id from Spektakl where name =" \
                                    + "'" + combobox.get() + "'")[0]))[
                                          0]) + "'" + "," + str(
                                each.but['text']) + ")"

                            insert_q(s)
                            total(each.but.price)
                            each.but['bg'] = 'gray'

                listshop.delete(0, END)
                lab_co['text'] = ''
                lab_s['text'] = '0'
                clear(event=1)
                if len(bilets) > 0:
                    messagebox.showinfo('Success',
                                        'Продажа прошла успешно!\nБилет сформирован и сохранён в bilets.pdf')
                    startfile('bilets.pdf')
            except Exception as e:
                print(e)
                messagebox.showerror('Error',
                                     'Ошибка при продаже билета.\nВозможно открыт файл с билетами.')
                listshop.delete(0, END)
                lab_co['text'] = ''
                lab_s['text'] = '0'
                clear(event=1)


def bron(event):
    if (input_name.place_info().__sizeof__()) == 264:
        input_name.place(x=5, y=245, anchor="w", width=87, height=35)
    else:
        if input_name.get() == '':
            clear(event=1)
        else:
            if proverka(event, 'red') == 1:
                for i in range(4):
                    for each in zal.return_all()[i]:
                        if each.but['bg'] == 'black':
                            s = "insert into Bron(id_seans,name,nomer) values (" + "'" \
                                + str(select_q(
                                "Select id from Seans where date = " + "'" + combo_date.get() + "'" + " and time =" \
                                + "'" + combo_time.get() + "'" + "and id_spek =" \
                                + str(select_q(
                                    "Select id from Spektakl where name =" \
                                    + "'" + combobox.get() + "'")[0]))[
                                          0]) + "'," + "'" + input_name.get() + "'," + str(
                                each.but['text']) + ")"
                            insert_q(s)
                            each.but['bg'] = 'darkblue'
                            listshop.delete(0, END)
                            lab_co['text'] = ''
                            lab_s['text'] = '0'
            input_name.place_forget()
            input_name.delete(0, END)


def antibron(event):
    q = select_q(
        "select nomer from Bron where name =" + "'"
        + antibron_text.get() + "'" + "and id_seans = "
        + str(select_q(
            "Select id from Seans where date = " + "'"
            + combo_date.get() + "'" + " and time ="
            + "'" + combo_time.get() + "'" + "and id_spek ="
            + str(select_q(
                "Select id from Spektakl where name ="
                + "'" + combobox.get() + "'")[
                      0]))[0]))

    if str(antibron_text.get()) == '':
        pass
    else:
        if str(listshop.get(0, END)) == '()':
            zal.antibron(q)
        else:
            listshop.delete(0, END)
            lab_co['text'] = ''
            lab_s['text'] = '0'
            zal.antibron_true(q)


def point(event):
    print('x =' + str(event.x) + ' y=' + str(event.y))


def update_zal(event):
    seans_id = str(select_q(
        "Select id from Seans where date = " + "'"
        + combo_date.get() + "'" + " and time ="
        + "'" + combo_time.get() + "'" + "and id_spek ="
        + str(select_q(
            "Select id from Spektakl where name ="
            + "'" + combobox.get() + "'")[
                  0]))[0])

    q = select_q(
        "select nomer from Bilet where id_seans = " + "'" + seans_id + "'")

    date_now = str(datetime.today().date())
    time_now = str(datetime.today().time())[:5]  # TIME FOR BRON !!!!!!!!! 30 MINUT
    
    if int(time_now[3:]) + 31 < 60:
        minute = int(time_now[3:]) + 31
        time_for_bron = time_now[:3] + str(minute)
    else:
        minute = (int(time_now[3:]) + 31) - 60
        hours = int(time_now[:2]) + 1
        if len(str(minute)) == 1:
            minute = "0" + str(minute)
        if len(str(hours)) == 1:
            hours = "0" + str(hours)

        time_for_bron = str(hours) + ":" + str(minute)

    k = select_q(
        "select Bron.nomer from Bron, Seans "
        "where Seans.id = Bron.id_seans and Bron.id_seans="
        + "'" + seans_id + "'" + "and Seans.date =" \
        + "'" + date_now + "'" + "and Seans.time  < " + "'"
        + time_for_bron + "'")

    if len(k) > 0:
        for i in k:
            delete_q(
                "delete from Bron where id_seans=" + "'" + seans_id
                + "'" + " and nomer=" + str(
                    i))

    k = select_q(
        "select nomer from Bron where id_seans=" + "'" + seans_id + "'")
    zal.right_start(q, k)
    clear(event=1)


def comboboxselected(event):
    combo_date.set('')
    combo_date['value'] = combobox_seans(date_time('date'))
    combo_date.current(0)
    combo_date_selected(event=1)
    update_zal(event=1)
    opisanie.config(state=NORMAL)
    opisanie.delete('1.0', END)
    opisanie.insert(1.0, select_q(
        "select opisanie from Spektakl where name =" + "'"
        + combobox.get() + "'")[0])
    opisanie.config(state=DISABLED)

    text_actors.config(state=NORMAL)
    text_actors.delete('1.0', END)
    text_actors.insert(1.0, select_q(
        "select actors from Spektakl where name =" + "'"
        + combobox.get() + "'")[0])
    text_actors.config(state=DISABLED)

    price1['text'] = zal.return_all()[0][0].but.price
    price2['text'] = zal.return_all()[1][0].but.price
    price3['text'] = zal.return_all()[2][0].but.price
    price4['text'] = zal.return_all()[3][0].but.price


def combo_date_selected(event):
    combo_time.set('')
    combo_time['value'] = date_time('time')
    combo_time.current(0)
    update_zal(event=1)


def select_q(query, k=0):
    l = []
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        l.append(row[k])
    return l


def insert_q(query):
    cursor.execute(query)
    cnxn.commit()


def update_q(query):
    cursor.execute(query)
    cnxn.commit()


def delete_q(query):
    cursor.execute(query)
    cnxn.commit()


def combobox_values():
    combobox['values'] = combobox_seans(
        select_q("Select Spektakl.name from Spektakl,Seans "
                 " where Seans.id_spek = Spektakl.id and Seans.date >= +"
                 + "'" + str(datetime.today().date())
                 + "'"))
    combobox.current(0)


def combobox_seans(a):
    b = []
    for i in a:
        if i not in b:
            b.append(i)
    return b


def date_time(s=''):
    clear(event=1)
    if s == 'date':
        return (select_q(
            "Select Seans.date from Seans,Spektakl "
            "where Seans.id_spek = Spektakl.id and Seans.date >= +"
            + "'" + str(
                datetime.today().date()) + "'" + " and Spektakl.name = "
            + "'" + combobox.get() + "'"))
    elif s == 'time':
        return select_q(
            "Select Seans.time from Seans,Spektakl "
            "where Seans.id_spek = Spektakl.id and Seans.date =" + "'"
            + combo_date.get() + "'" \
            + "and Spektakl.name = " + "'" + combobox.get() + "'")
    else:
        return ''


def form_spek():
    def adding_spek(event):
        formSpek.destroy()
        add_spek()

    def izmena_spek(event):
        formSpek.destroy()
        chose_name_izm()

    def delete_spek(event):
        formSpek.destroy()
        chose_name_izm('1')

    formSpek = Toplevel()
    formSpek.title('Работа с cпектаклями')
    formSpek.geometry('500x180+300+200')
    formSpek.bind('<Button-1>', point)
    spek_add = Button(formSpek, text='Добавить новый\n спектакль', font=15,
                      bd=5)
    spek_add.bind('<Button-1>', adding_spek)
    spek_izm = Button(formSpek, text='Изменить инфо о \nспектакле', font=15,
                      bd=5)
    spek_izm.bind('<Button-1>', izmena_spek)
    spek_del = Button(formSpek, text='Удалить', font=15, bd=5, height=2,
                      width=10)
    spek_del.bind('<Button-1>', delete_spek)
    help_spek = Label(formSpek,
                      text='Манипуляция с информацией связанной \n '
                           'с спектаклями в базе данных : ',
                      font=("Buxton Sketch", 22))

    help_spek.place(x=36, y=50, anchor='w')
    spek_add.place(x=29, y=130, anchor='w')
    spek_izm.place(x=189, y=130, anchor='w')
    spek_del.place(x=363, y=130, anchor='w')


def form_seans():
    def adding_seans(event):
        formSeans.destroy()
        add_seans()

    def izmena_seans(event):
        formSeans.destroy()
        izm_seans()

    def delete_seans(event):
        try:
            seans_id = select_q(
                "select Seans.id from Seans,Spektakl "
                "where Seans.id_spek = Spektakl.id and Spektakl.name ="
                + "'" + combobox.get() + "'" + \
                "and Seans.date =" + "'" + combo_date.get() + "'"
                + "and Seans.time=" + "'" + combo_time.get() + "'")
            if messagebox.askokcancel('Подтверждение', 'Вы уверены?'):
                delete_q("delete from Seans where id=" + str(seans_id[0]))
                combobox_values()
                comboboxselected(event=1)
        except Exception as e:
            print(e)
            messagebox.showerror("Error", "Невозможно удалить данный сеанс.")

    formSeans = Toplevel()
    formSeans.title('Работа с сеансами')
    formSeans.geometry('500x180+300+200')
    formSeans.bind('<Button-1>', point)
    seans_add = Button(formSeans, text='Добавить новый\n сеанс', font=15, bd=5)
    seans_add.bind('<Button-1>', adding_seans)
    seans_izm = Button(formSeans, text='Изменить инфо о \nсеансе', font=15,
                       bd=5)
    seans_izm.bind('<Button-1>', izmena_seans)
    seans_del = Button(formSeans, text='Удалить', font=15, bd=5, height=2,
                       width=10)
    seans_del.bind('<Button-1>', delete_seans)
    help_seans = Label(formSeans,
                       text='Манипуляция с информацией связанной \n '
                            'с сеансами в базе данных : ',
                       font=("Buxton Sketch", 22))

    help_seans.place(x=36, y=50, anchor='w')
    seans_add.place(x=29, y=130, anchor='w')
    seans_izm.place(x=189, y=130, anchor='w')
    seans_del.place(x=363, y=130, anchor='w')


def add_spek():
    def adding_spek():
        try:
            if name_spek_.get() == "":
                raise Exception
            insert_q(
                "insert into Spektakl(name,opisanie,actors) values("
                + "'" + name_spek_.get() + "'" + "," + "'" +
                opisanie_spek_.get("1.0", END).split('\n')[
                    0] + "'" + "," + "'" +
                actors_spek_.get("1.0", END).split('\n')[0] + "'" + ")")
            messagebox.showinfo("Добавлено",
                                "Новый спектакль успешно "
                                "добавлен в базу данных.")
            spek.destroy()
            combobox_values()
        except Exception as e:
            print(e)
            messagebox.showerror("Error",
                                 "Введите правильно информацию о спектакле.")
            spek.tkraise()

    spek = Toplevel()
    spek.title('Добавление нового спектакля')
    spek.geometry('500x300+500+200')
    spek.bind('<Button-1>', point)

    name_spek = Label(spek, text='Введите название\n спектакля : ')
    name_spek.place(x=22, y=30, anchor='w')

    opisanie_spek = Label(spek, text='Описание : ')
    opisanie_spek.place(x=22, y=75, anchor='w')

    actors_spek = Label(spek, text='Актеры : ')
    actors_spek.place(x=22, y=170, anchor='w')

    name_spek_ = Entry(spek, width=53)
    name_spek_.place(x=140, y=30, anchor='w')

    opisanie_spek_ = Text(spek, height=5, width=40, wrap=WORD)
    opisanie_spek_.place(x=140, y=58, anchor='nw')

    actors_spek_ = Text(spek, height=2, width=40, wrap=WORD)
    actors_spek_.place(x=140, y=155, anchor='nw')

    spek_ok = Button(spek, text='Добавить', command=adding_spek)
    spek_ok.place(x=85, y=251)
    spek_cancel = Button(spek, text='Отменить', command=spek.destroy)
    spek_cancel.place(x=350, y=251)


def chose_name_izm(s=''):
    def izm_names_selected(event):
        label_for_izm['text'] = izm_names.get()

    def izmenenie():
        if izm_names.get() == '':
            pass
        else:
            name_izm.destroy()
            izm_spek()

    def deleting():
        if messagebox.askokcancel('Подтверждение', 'Вы уверены?'):
            id_spek = select_q(
                "select id from Spektakl where name=" + "'" + izm_names.get()
                + "'")[0]
            delete_q(
                "delete from Seans where id_spek=" + "'" + str(id_spek) + "'")
            delete_q("delete from Spektakl where id=" + str(id_spek))
            name_izm.destroy()
            messagebox.showinfo('Удалено',
                                'Спектакль удалён с сеансами, '
                                'которые были связаны с ним.')
            combobox_values()
            comboboxselected(event=1)

    name_izm = Toplevel()
    name_izm.title('Спектакли')
    name_izm.geometry('500x300+500+200')
    name_izm.bind('<Button-1>', point)

    label_izm_text = Label(name_izm,
                           text='Выберите нужный спектакль\n '
                                'для изменения/удаления',
                           font=("Buxton Sketch", 22))
    label_izm_text.place(x=88, y=25, anchor='nw')
    izm_names = Combobox(name_izm,
                         values=select_q("Select Spektakl.name from Spektakl"),
                         height=1, state='readonly',
                         font=("Arial", 15, "bold"), width=35)
    izm_names.bind('<<ComboboxSelected>>', izm_names_selected)
    izm_names.place(x=47, y=118, anchor='w')
    if s == '1':
        spek_ok = Button(name_izm, text='Выбрать', command=deleting, font=15)
    else:
        spek_ok = Button(name_izm, text='Выбрать', command=izmenenie, font=15)
    spek_ok.place(x=85, y=251)
    spek_cancel = Button(name_izm, text='Отменить', command=name_izm.destroy,
                         font=15)
    spek_cancel.place(x=350, y=251)


def izm_spek():
    def izmenit_spek():
        try:
            update_q(
                "update Spektakl set name=" + "'" + name_spek_.get() + "'"
                + ",opisanie=" + "'" +
                opisanie_spek_.get("1.0", END).split('\n')[
                    0] + "'" + ",actors=" + "'" +
                actors_spek_.get("1.0", END).split('\n')[
                    0] + "'" + " where name=" + "'" + label_for_izm[
                    'text'] + "'" + ';')
            messagebox.showinfo("Изменено",
                                "Данные успешно обновлены "
                                "и добавлены в базу данных.")
            spek_imz.destroy()
            combobox_values()
            comboboxselected(event=1)
        except Exception as e:
            print(e)
            messagebox.showerror("Error",
                                 "Введите правильно информацию о спектакле.")
            spek_imz.tkraise()

    spek_imz = Toplevel()
    spek_imz.title('Изменение информации о спектакле')
    spek_imz.geometry('500x300+500+200')
    spek_imz.bind('<Button-1>', point)

    name_spek = Label(spek_imz, text='Измените название\n спектакля : ')
    name_spek.place(x=22, y=30, anchor='w')

    opisanie_spek = Label(spek_imz, text='Описание : ')
    opisanie_spek.place(x=22, y=75, anchor='w')

    actors_spek = Label(spek_imz, text='Актеры : ')
    actors_spek.place(x=22, y=170, anchor='w')

    name_spek_ = Entry(spek_imz, width=53)
    name_spek_.place(x=140, y=30, anchor='w')
    name_spek_.insert(0, label_for_izm['text'])

    opisanie_spek_ = Text(spek_imz, height=5, width=40, wrap=WORD)
    opisanie_spek_.place(x=140, y=58, anchor='nw')
    opisanie_spek_.insert(1.0, select_q(
        "select opisanie from Spektakl where name=" + "'" + label_for_izm[
            'text'] + "'")[0])

    actors_spek_ = Text(spek_imz, height=2, width=40, wrap=WORD)
    actors_spek_.place(x=140, y=155, anchor='nw')
    actors_spek_.insert(1.0, select_q(
        "select actors from Spektakl where name=" + "'" + label_for_izm[
            'text'] + "'")[0])

    spek_ok = Button(spek_imz, text='Изменить', command=izmenit_spek)
    spek_ok.place(x=85, y=251)
    spek_cancel = Button(spek_imz, text='Отменить', command=spek_imz.destroy)
    spek_cancel.place(x=350, y=251)


def add_seans():
    def adding_seans():
        try:
            if proverka_date(data_seans_.get()):
                insert_q(
                    "insert into Seans(id_spek,date,time,one,two,three,four) "
                    "values(" + str(
                        select_q(
                            "select id from Spektakl where name=" + "'"
                            + name_seans_.get() + "'")[
                            0]) + "," \
                    + "'" + str(data_seans_.get()) + "'," + "'" + str(
                        time_seans_.get()) + "'," + \
                    str(one_price_.get()) + "," + str(
                        two_price_.get()) + "," + str(
                        three_price_.get()) + "," + str(
                        four_price_.get()) + ")")

                messagebox.showinfo("Добавлено",
                                    "Новый сеанс успешно "
                                    "добавлен в базу данных.")
                combobox_values()
                comboboxselected(event=1)
                seans.destroy()
            else:
                messagebox.showinfo('Error',
                                    'Введите корректную дату\n'
                                    'Формат даты : гггг-мм-дд')
                seans.tkraise()
        except Exception as e:
            print(e)
            messagebox.showerror("Error",
                                 "Введите правильно информацию о сеансе.")
            seans.tkraise()

    seans = Toplevel()
    seans.title('Добавление нового сеанса')
    seans.geometry('350x330+500+200')
    seans.bind('<Button-1>', point)

    name_seans = Label(seans, text='Выберите название\n спектакля : ')
    name_seans.place(x=22, y=30, anchor='w')

    data_seans = Label(seans, text='Дата : ')
    data_seans.place(x=22, y=75, anchor='w')

    time_seans = Label(seans, text='Время : ')
    time_seans.place(x=22, y=125, anchor='w')

    price_label = Label(seans, text='Стоимость билетов ')
    price_label.place(x=115, y=170, anchor='w')

    one_price = Label(seans, text='1-2 ряд : ')
    one_price.place(x=22, y=200, anchor='w')

    two_price = Label(seans, text='3-4 ряд : ')
    two_price.place(x=22, y=242, anchor='w')

    three_price = Label(seans, text='2 этаж : ')
    three_price.place(x=180, y=200, anchor='w')

    four_price = Label(seans, text='3 этаж : ')
    four_price.place(x=180, y=242, anchor='w')

    name_seans_ = Combobox(seans, height=1, state='readonly',
                           values=
                           select_q("Select Spektakl.name from Spektakl"),
                           width=27)
    name_seans_.place(x=150, y=30, anchor='w')

    data_seans_ = Entry(seans, width=30)
    data_seans_.place(x=150, y=75, anchor='w')

    time_seans_ = Entry(seans, width=30)
    time_seans_.place(x=150, y=125, anchor='w')

    one_price_ = Entry(seans, width=7)
    one_price_.place(x=90, y=202, anchor='w')

    two_price_ = Entry(seans, width=7)
    two_price_.place(x=90, y=242, anchor='w')

    three_price_ = Entry(seans, width=7)
    three_price_.place(x=245, y=202, anchor='w')

    four_price_ = Entry(seans, width=7)
    four_price_.place(x=245, y=242, anchor='w')

    seans_ok = Button(seans, text='Добавить', command=adding_seans)
    seans_ok.place(x=35, y=280)
    seans_cancel = Button(seans, text='Отменить', command=seans.destroy)
    seans_cancel.place(x=230, y=280)


def izm_seans():
    def update_seans():
        try:
            if proverka_date(data_seans_.get()):
                update_q("update Seans set id_spek=" + str(select_q(
                    "select id from Spektakl where name=" + "'"
                    + name_seans_.get() + "'")[
                                                               0]) + ","
                         + "date=" + "'" + str(
                    data_seans_.get()) + "', time= " + "'" + str(
                    time_seans_.get()) + "'," \
                         + " one=" + str(one_price_.get()) + ",two=" + str(
                    two_price_.get()) + ",three=" + str(
                    three_price_.get()) + ",four=" + str(four_price_.get()) +
                         " where id=" + str(seans_id[0]))

                messagebox.showinfo("Изменено",
                                    "Данный сеанс успешно "
                                    "изменён в базе данных.")
                combobox_values()
                comboboxselected(event=1)
                seans.destroy()
            else:
                messagebox.showinfo('Error',
                                    'Введите корректную дату\n'
                                    'Формат даты : гггг-мм-дд')
                seans.tkraise()
        except Exception as e:
            print(e)
            messagebox.showerror("Error",
                                 "Введите правильно информацию о сеансе.")
            seans.tkraise()

    seans = Toplevel()
    seans.title('Изменение сеанса')
    seans.geometry('350x330+500+200')
    seans.bind('<Button-1>', point)

    name_seans = Label(seans, text='Выберите название\n спектакля : ')
    name_seans.place(x=22, y=30, anchor='w')

    data_seans = Label(seans, text='Дата : ')
    data_seans.place(x=22, y=75, anchor='w')

    time_seans = Label(seans, text='Время : ')
    time_seans.place(x=22, y=125, anchor='w')

    price_label = Label(seans, text='Стоимость билетов ')
    price_label.place(x=115, y=170, anchor='w')

    one_price = Label(seans, text='1-2 ряд : ')
    one_price.place(x=22, y=200, anchor='w')

    two_price = Label(seans, text='3-4 ряд : ')
    two_price.place(x=22, y=242, anchor='w')

    three_price = Label(seans, text='2 этаж : ')
    three_price.place(x=180, y=200, anchor='w')

    four_price = Label(seans, text='3 этаж : ')
    four_price.place(x=180, y=242, anchor='w')

    l = select_q("Select Spektakl.name from Spektakl")

    name_seans_ = Combobox(seans, height=1, state='readonly', values=l,
                           width=27)
    name_seans_.place(x=150, y=30, anchor='w')

    for i in l:
        if i == combobox.get():
            name_seans_.current(l.index(i))

    data_seans_ = Entry(seans, width=30)
    data_seans_.place(x=150, y=75, anchor='w')
    data_seans_.insert(1, combo_date.get())

    time_seans_ = Entry(seans, width=30)
    time_seans_.place(x=150, y=125, anchor='w')
    time_seans_.insert(1, combo_time.get())

    one_price_ = Entry(seans, width=7)
    one_price_.place(x=90, y=202, anchor='w')

    two_price_ = Entry(seans, width=7)
    two_price_.place(x=90, y=242, anchor='w')

    three_price_ = Entry(seans, width=7)
    three_price_.place(x=245, y=202, anchor='w')

    four_price_ = Entry(seans, width=7)
    four_price_.place(x=245, y=242, anchor='w')

    seans_id = select_q(
        "select Seans.id from Seans,Spektakl where Seans.id_spek = "
        "Spektakl.id and Spektakl.name =" + "'" + name_seans_.get() + "'" +
        "and Seans.date =" + "'" + data_seans_.get() + "'"
        + "and Seans.time=" + "'" + time_seans_.get() + "'")

    one_price_.insert(1, select_q(
        "select one from Seans where id=" + str(seans_id[0]))[0])
    two_price_.insert(1, select_q(
        "select two from Seans where id=" + str(seans_id[0]))[0])
    three_price_.insert(1, select_q(
        "select three from Seans where id=" + str(seans_id[0]))[0])
    four_price_.insert(1, select_q(
        "select four from Seans where id=" + str(seans_id[0]))[0])

    seans_ok = Button(seans, text='Изменить', command=update_seans)
    seans_ok.place(x=35, y=280)
    seans_cancel = Button(seans, text='Отменить', command=seans.destroy)
    seans_cancel.place(x=200, y=280)


def create_bilet(bilets):
    c = canvas.Canvas("bilets.pdf", pagesize=(607, 265))
    for i in bilets:
        c.drawImage(image="template.png", x=0, y=0)
        pdfmetrics.registerFont(TTFont('font', 'Arial.TTF'))
        pdfmetrics.registerFont(TTFont('test', 'BuxtonSketch.ttf'))
        c.setFont("font", 20)
        c.drawString(288, 190, i["mesto"])  # PARTER
        c.drawString(328, 155, str(i["ryad"]))  # РЯД
        c.drawString(427, 155, str(i["nomer"]))  # МЕСТО
        c.drawString(238, 115, i["spektakl"])  # name spektakl
        c.setFont("font", 16)
        c.drawString(248, 75, i["data"])  # DATE
        c.drawString(415, 75, i["time"])  # TIME
        c.setFont("font", 20)
        c.drawString(95, 46, str(i["price"]))

        c.showPage()

    c.save()


def design():
    def painting():
        try:
            if color_fon1.get() == "":
                color1 = color('fon')
            else:
                color1 = color_fon1.get()

            if color_mesta1.get() == "":
                color2 = color('center')
            else:
                color2 = color_mesta1.get()

            if color_free1.get() == "":
                color3 = color('mesta')
            else:
                if str(color_free1.get()).lower() == "red" or str(
                        color_free1.get()).lower() == "black" or str(
                        color_free1.get()).lower() == "gray":
                    messagebox.showerror("Error",
                                         "Этот цвет использовать нельзя.")
                    desing_form.tkraise()
                    color3 = "Lawn green"
                else:
                    color3 = color_free1.get()

            main['bg'] = color1
            top_frame['bg'] = color1
            frame_scena['bg'] = color1
            lab['bg'] = color1
            left_frame['bg'] = color1
            zakraska_odin_left_frame['bg'] = color1
            zakraska_dva_left_frame['bg'] = color1
            left_label['bg'] = color1
            left_label2['bg'] = color1
            left_label3['bg'] = color1
            left_label4['bg'] = color1
            bottom_frame['bg'] = color1
            v_glavnoi_roli['bg'] = color1
            right_frame['bg'] = color1
            shopping_cart['bg'] = color1
            shopping_cart_frame['bg'] = color1
            shopp['bg'] = color1
            list_frame['bg'] = color1
            lab_co['bg'] = color1
            lab_count['bg'] = color1
            lab_s['bg'] = color1
            lab_sum['bg'] = color1
            price_frame['bg'] = color1
            price1['bg'] = color1
            price2['bg'] = color1
            price3['bg'] = color1
            price4['bg'] = color1
            parter_label['bg'] = color1
            ryad_label['bg'] = color1
            ryad2_label['bg'] = color1
            etazh_label['bg'] = color1
            etazh2_label['bg'] = color1

            center_frame['bg'] = color2
            fr_par1['bg'] = color2
            fr_par2['bg'] = color2
            fr_par3['bg'] = color2
            fr_par4['bg'] = color2
            test['bg'] = color2
            test2['bg'] = color2
            if not color3:
                color3 = color('mesto')
            global color_mesto
            color_mesto = color3

            global zal

            del zal
            zal = CreateHall()
            zal.create()
            update_zal(event=1)

            try:
                f = open('color.colors', 'w')
                f.write(color3 + ',' + color1 + ',' + color2)
            except Exception as e:
                print(e)
                messagebox.showerror("Error", "Сохранить не удалось.")
                desing_form.tkraise()
        except Exception as e:
            print(e)
            messagebox.showerror("Error", "Введите правильно название цвета.")
            desing_form.tkraise()

    desing_form = Toplevel()
    desing_form.title('Изменение дизайна')
    desing_form.geometry('340x200+400+200')
    desing_form.bind('<Button-1>', point)

    color_fon = Label(desing_form, text='Цвет основного фона : ')
    color_fon.place(x=22, y=30, anchor='w')

    color_mesta = Label(desing_form, text='Цвет фона с местами : ')
    color_mesta.place(x=22, y=75, anchor='w')

    color_fon1 = Entry(desing_form, width=15)
    color_fon1.place(x=210, y=30, anchor='w')

    color_mesta1 = Entry(desing_form, width=15)
    color_mesta1.place(x=210, y=75, anchor='w')

    color_free = Label(desing_form, text="Цвет мест\n(зеленый по умолчанию)")
    color_free.place(x=22, y=125, anchor='w')

    color_free1 = Entry(desing_form, width=15)
    color_free1.place(x=210, y=125, anchor='w')

    button = Button(desing_form, text='Accept', command=painting, width=20,
                    border=3)
    button.place(x=105, y=170, anchor='w')


def context(event):
    menu.tk_popup(event.x_root, event.y_root, 0)


def color(col):
    try:
        with open('color.colors') as f:
            content = f.readline().split(',')
        if len(content) > 2:
            if col == 'mesto':
                return content[0]
            elif col == 'fon':
                return content[1]
            elif col == 'center':
                return content[2]
        else:
            raise Exception
    except Exception as e:
        print(e)
        if col == 'mesto':
            return 'Lawn green'
        elif col == 'fon':
            return 'white'
        elif col == 'center':
            return 'white'


def proverka_date(date):
    try:
        datetime.strptime(date, '%Y-%m-%d')
        return True
    except Exception as e:
        print(e)
        return False


def report_form():
    def report():
        if data1.get() == "" or data2.get() == "":
            messagebox.showerror('error', 'Введите нужные даты.')
            reportForm.tkraise()
        else:
            if proverka_date(data1.get()) and proverka_date(data2.get()):
                ids = select_q(
                    "select Seans.id from Seans,Sell "
                    "where Sell.id_seans=Seans.id and Seans.date>='"
                    + data1.get() + "' and Seans.date<='" + data2.get() + "'")
                seanses = []
                seans = {}
                for i in ids:
                    seans["name_spek"] = select_q(
                        "select Spektakl.name from Seans,Spektakl "
                        "where Seans.id_spek=Spektakl.id and Seans.id="
                        + str(i))
                    seans["date"] = select_q(
                        "select date from Seans where id=" + str(i))
                    seans["time"] = select_q(
                        "select time from Seans where id=" + str(i))
                    seans["kol"] = select_q(
                        "select kol_biletov from Sell where id_seans="
                        + str(i))
                    seans["money"] = select_q(
                        "select total_money from Sell where id_seans="
                        + str(i))
                    seanses.append(seans.copy())
                    seans.clear()
                try:
                    c = canvas.Canvas("report.pdf")
                    pdfmetrics.registerFont(TTFont('font', 'Arial.TTF'))
                    pdfmetrics.registerFont(TTFont('test', 'BuxtonSketch.ttf'))
                    c.setFont("test", 20)
                    c.drawString(160, 800, 'Отчет по продаже билетов театра')
                    c.line(50, 780, 550, 780)
                    c.line(50, 50, 550, 50)
                    y = 740
                    k = 1
                    index = 1
                    for i in seanses:
                        if k == 6:
                            c.showPage()
                            c.setFont("test", 20)
                            c.drawString(160, 800,
                                         'Отчет по продаже билетов театра')
                            c.line(50, 780, 550, 780)
                            c.line(50, 50, 550, 50)
                            k = 1
                            y = 740
                        c.drawString(50, y, str(index))
                        c.drawString(100, y, str(i['name_spek'][0]))
                        c.drawString(160, y - 25, 'Дата сеанса :')
                        c.drawString(160, y - 50, 'Время сеанса :')
                        c.drawString(160, y - 75,
                                     'Количество проданных билетов : ')
                        c.drawString(160, y - 100, 'Общая выручка : ')
                        c.drawString(465, y - 25, str(i['date'][0]))
                        c.drawString(465, y - 50, str(i['time'][0]))
                        c.drawString(465, y - 75, str(i['kol'][0]))
                        c.drawString(465, y - 100, str(i['money'][0]) + " грн")
                        y -= 140
                        k += 1
                        index += 1

                    c.save()
                    c.showPage()
                    messagebox.showinfo('Success',
                                        'Отчет успешно создан '
                                        'и сохранёй в файл report.pdf')
                    reportForm.destroy()
                    startfile('report.pdf')
                except Exception as e:
                    print(e)
                    messagebox.showerror('error',
                                         'Невозможно создать новый отчет, '
                                         'так как старый всё ещё '
                                         'используется.')
                    reportForm.tkraise()

            else:
                messagebox.showerror('error',
                                     'Проверьте правильность введенной даты.\n'
                                     'Формат даты : гггг-мм-дд')
                reportForm.tkraise()

    reportForm = Toplevel()
    reportForm.title('Работа с отчетом')
    reportForm.geometry('500x180+300+200')
    reportForm.bind('<Button-1>', point)

    Label(reportForm, text='Введите начальную дату : ',
          font=("Buxton Sketch", 22)).place(x=16, y=50, anchor='w')
    Label(reportForm, text='Введите вторую дату : ',
          font=("Buxton Sketch", 22)).place(x=16, y=100, anchor='w')

    data1 = Entry(reportForm, width=15)
    data1.place(x=350, y=50, anchor='w')

    data2 = Entry(reportForm, width=15)
    data2.place(x=350, y=100, anchor='w')

    Button(reportForm, text='Создать отчет', command=report, font='15',
           bd=5).place(x=250, y=150, anchor='center')


color_mesto = color('mesto')
color_fon = color('fon')
color_center = color('center')

root = Tk()
root.geometry("1215x667+0+0")
root.iconphoto(True, ImageTk.PhotoImage(Image.open("icon.png")))
root.title("Театр")
root.resizable(0, 0)
main = Frame(root, width="1200", height="800", bg=color_fon)
main.pack()
root.bind('<Button-1>', point)

top_frame = Frame(main, width="1220", height=10,
                  bg=color_fon)  # ALL FOR TOP FRAME
top_frame.grid(row=0, column=0, columnspan=50)

label_for_izm = Label(root)

test = Label(main, text="")
# ALL FOR SCENA BLOCK
frame_scena = Frame(main, width="850", height="50", bg=color_fon)
lab = Label(frame_scena, text="Областной театр юного зрителя",
            font=("Buxton Sketch", 27), bg=color_fon)
frame_scena.grid(row=1, column=1, columnspan=40)

menu = Menu(lab, tearoff=0)
menu.add_command(label="Работа с сеансами", command=form_seans)
menu.add_command(label="Работа со спектаклями", command=form_spek)
menu.add_separator()
menu.add_command(label="Работа с дизайном", command=design)
menu.add_separator()
menu.add_command(label="Работа с отчетом по билетам", command=report_form)

lab.place(x=330, y=25, anchor='center')
lab.bind('<Button-3>', context)

left_frame = Frame(main, width="150", height="460", bg=color_fon)
left_frame.grid(row=1, column=0, rowspan=10)  # ALL FOR LEFT BLOCK

zakraska_odin_left_frame = Frame(left_frame, width="150", height="60",
                                 bg=color_fon)
zakraska_odin_left_frame.place(x=0, y=0)

zakraska_dva_left_frame = Frame(left_frame, width="150", height="30",
                                bg=color_fon)
zakraska_dva_left_frame.place(x=0, y=430, anchor="nw")

left_label = Label(left_frame, text="Ряды 1-2 : ",
                   font=("Buxton Sketch", 20),
                   bg=color_fon)
left_label.place(x=142, y=122, anchor="e")

left_label2 = Label(left_frame, text="Ряды 3-4 : ",
                    font=("Buxton Sketch", 20),
                    bg=color_fon)
left_label2.place(x=142, y=222, anchor="e")

left_label3 = Label(left_frame, text="2-ой этаж: ",
                    font=("Buxton Sketch", 20),
                    bg=color_fon)
left_label3.place(x=142, y=293, anchor="e")

left_label4 = Label(left_frame, text="3-ий этаж: ",
                    font=("Buxton Sketch", 20),
                    bg=color_fon)
left_label4.place(x=142, y=385, anchor="e")

right_frame = Frame(main, width="200", height="460", bg=color_fon)
right_frame.grid(row=1, column=20, rowspan=10)  # ALL FOR RIGHT BLOCK

shopping_cart_frame = Frame(right_frame, width="190", height="260",
                            bg=color_fon)
shopping_cart_frame.place(x=95, y=0, anchor="n")

image = ImageTk.PhotoImage(Image.open("cart2.png"))
shopping_cart = Label(shopping_cart_frame, image=image, bg=color_fon)
shopping_cart.place(x=40, y=0, anchor="n")
shopp = Label(shopping_cart_frame, text="Корзина",
              font=("Buxton Sketch", 20),
              bg=color_fon)
shopp.place(x=117, y=21, anchor="center")

list_frame = Frame(shopping_cart_frame, width="170", height="100",
                   bg=color_fon)
list_frame.place(x=97, y=91, anchor="center")
scrollbar = Scrollbar(list_frame, orient=VERTICAL)
listshop = Listbox(list_frame, bd=2, height=5, width="27",
                   yscrollcommand=scrollbar.set)
scrollbar.config(command=listshop.yview)
listshop.pack(side=LEFT, fill=BOTH, expand=1)
scrollbar.pack(side=RIGHT, fill=Y)

lab_count = Label(shopping_cart_frame, text="Количество : ",
                  bg=color_fon,
                  font=("Buxton Sketch", 14))
lab_count.place(x=60, y=150, anchor="center")
lab_co = Label(shopping_cart_frame, text='', bg=color_fon,
               font=("Buxton Sketch", 16))
lab_co.place(x=135, y=150, anchor="center")

lab_sum = Label(shopping_cart_frame, text='Общая сумма : ',
                bg=color_fon,
                font=("Buxton Sketch", 14))
lab_sum.place(x=60, y=175, anchor='center')
lab_s = Label(shopping_cart_frame, text='0', bg=color_fon,
              font=("Buxton Sketch", 16))
lab_s.place(x=135, y=175, anchor="center")

clear_but = Button(shopping_cart_frame, text="Очистить корзину",
                   width=25)
clear_but.place(x=97, y=210, anchor="center")
clear_but.bind('<Button-1>', clear)

sell_but = Button(shopping_cart_frame, text="Продать", width=11)
sell_but.bind('<ButtonRelease-1>', sell)

input_name = Entry(shopping_cart_frame)
input_name['bd'] = 5

bron_but = Button(shopping_cart_frame, text="Забронировать")

bron_but.bind('<Button-1>', bron)

sell_but.place(x=5, y=245, anchor="w")
bron_but.place(x=142, y=245, anchor="center")

price_frame = Frame(right_frame, width="190", height="197", bg=color_fon)
price_frame.place(x=95, y=262, anchor="n")

parter_label = Label(price_frame, text='Партер:', bg=color_fon,
                     font=("Buxton Sketch", 16))
parter_label.place(x=10, y=15, anchor="w")

ryad_label = Label(price_frame, text='Ряд 1-2:', bg=color_fon,
                   font=("Buxton Sketch", 16))
ryad_label.place(x=36, y=40, anchor="w")

price1 = Label(price_frame, bg=color_fon, font=("Buxton Sketch", 20))
price1.place(x=111, y=40, anchor='w')

ryad2_label = Label(price_frame, text='Ряд 3-4:', bg=color_fon,
                    font=("Buxton Sketch", 16))
ryad2_label.place(x=36, y=68, anchor="w")

price2 = Label(price_frame, bg=color_fon, font=("Buxton Sketch", 20))
price2.place(x=111, y=68, anchor='w')

etazh_label = Label(price_frame, text='2-ой этаж : ', bg=color_fon,
                    font=("Buxton Sketch", 16))
etazh_label.place(x=10, y=104, anchor='w')

price3 = Label(price_frame, bg=color_fon, font=("Buxton Sketch", 20))
price3.place(x=115, y=104, anchor='w')

etazh2_label = Label(price_frame, text='3-ий этаж: ', bg=color_fon,
                     font=("Buxton Sketch", 16))
etazh2_label.place(x=10, y=144, anchor='w')

price4 = Label(price_frame, bg=color_fon, font=("Buxton Sketch", 20))
price4.place(x=115, y=144, anchor='w')

ramka_bot = Frame(main, width="1220", height="200", bg="black", bd=3)
ramka_bot.grid(row=20, column=0, columnspan=47)

bottom_frame = Frame(ramka_bot, width="1200", height="190", bg=color_fon,
                     bd=20)

bottom_frame.pack()  # ALL FOR BOTTOM BLOCK

opisanie = Text(bottom_frame, height=7, width=80, font=8, wrap=WORD)
opisanie.place(x=1, y=27, anchor="nw")

combobox = Combobox(bottom_frame, height=5, state='readonly',
                    font=("Arial", 15, "bold"), width=35,
                    values=combobox_seans(
                        select_q("Select Spektakl.name from Spektakl,Seans "
                                 " where Seans.id_spek = Spektakl.id "
                                 "and Seans.date >= +"
                                 + "'" + str(datetime.today().date()) + "'")))

combobox.place(x=750, y=15, anchor="w")
combobox.bind('<<ComboboxSelected>>', comboboxselected)

combo_date = Combobox(bottom_frame, height=1, state='readonly',
                      font=("Arial", 15, "bold"), width=16)
combo_date.place(x=749, y=65, anchor="w")
combo_date.bind('<<ComboboxSelected>>', combo_date_selected)

combo_time = Combobox(bottom_frame, height=1, state='readonly',
                      font=("Arial", 15, "bold"), width=15)
combo_time.place(x=972, y=65, anchor="w")
combo_time.bind('<<ComboboxSelected>>', update_zal)

antibron_but = Button(bottom_frame, text='Разбронировать', font=15, width=20)
antibron_but.place(x=1067, y=140, anchor="center")
antibron_but.bind('<ButtonRelease-1>', antibron)

antibron_text = Entry(bottom_frame, font=15)
antibron_text['bd'] = 3
antibron_text.place(x=847, y=140, anchor="center", height=30, width=200)

v_glavnoi_roli = Label(bottom_frame, text='В главной роли :',
                       font=("Buxton Sketch", 16), bg=color_fon)
v_glavnoi_roli.place(x=0, y=0, anchor="w")

text_actors = Text(bottom_frame, height=1, width=65, font=10)
text_actors.place(x=137, y=0, anchor="w")

# ALL FOR CENTER BLOCK

poloska = Frame(main, width="850", height="400", bg="black", bd=3)
poloska.grid(row=3, column=2)

center_frame = Frame(poloska, width="850", height="400", bg=color_center,
                     bd=20)
center_frame.pack()

fr_par1 = Frame(center_frame, width="400", bg=color_center)
fr_par1.grid(row=4, column=1)
test = Label(center_frame, text="", bg=color_center)
test.grid(row=5, column=1)
fr_par2 = Frame(center_frame, width="400", bg=color_center)
fr_par2.grid(row=6, column=1)
fr_par3 = Frame(center_frame, width="400", bg=color_center)  # ALL FOR PARTER
fr_par3.grid(row=7, column=1)
test2 = Label(center_frame, text="", bg=color_center)
test2.grid(row=8, column=1)
fr_par4 = Frame(center_frame, width="400", bg=color_center)
fr_par4.grid(row=9, column=1)

if __name__ == '__main__':
    zal = CreateHall()
    zal.create()

    combobox.current(0)
    comboboxselected(event=1)
    combo_date.current(0)

    # delete_q("delete from Bilet")
    # delete_q("delete from Sell")
    # delete_q("delete from Bron")

    root.mainloop()
