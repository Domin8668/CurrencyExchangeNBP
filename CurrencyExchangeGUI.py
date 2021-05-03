from tkinter import *
import scraper
import os
import webbrowser
from datetime import datetime
import time


# optimised
def list_functions():
    label_header = Label(frame, text="Dostępne funkcje:", font=('Arial', 15, 'bold'))
    label_header.grid(row=0,
                     column=0,
                     columnspan=3,
                     sticky="w")

    button_1 = Button(frame, text="Kursy walut", width=15, command=lambda: load_from_file(data, FILES[0], directory))
    button_1.grid(row=1, column=0, sticky="w")
    label_1 = Label(frame, text=" - aktualne kursy walut wraz z porównaniem do ostatniego pliku")
    label_1.grid(row=1, column=1, sticky="w")

    button_2 = Button(frame, text="Kalkulator walut", width=15, command=lambda: converter_menu(data))
    button_2.grid(row=2, column=0, sticky="w")
    label_2 = Label(frame, text=" - konwersja walut według aktualnych kursów")
    label_2.grid(row=2, column=1, sticky="w")

    button_3 = Button(frame, text="Zapisz do pliku", width=15, command=lambda: save_to_file(data))
    button_3.grid(row=3, column=0, sticky="w")
    label_3 = Label(frame, text=" - zapisanie aktualnych kursów do pliku tekstowego")
    label_3.grid(row=3, column=1, sticky="w")

    button_4 = Button(frame, text="Wczytaj z pliku", width=15, command=lambda: compare_from_file(data))
    button_4.grid(row=4, column=0, sticky="w")
    label_4 = Label(frame, text=" - porównanie aktualnych kursów z tymi z wybranego pliku")
    label_4.grid(row=4, column=1, sticky="w")

    button_5 = Button(frame, text="Informacje", width=15, command=lambda: list_credits())
    button_5.grid(row=5, column=0, sticky="w")
    label_5 = Label(frame, text=" - informacje dotyczące programu")
    label_5.grid(row=5, column=1, sticky="w")

    button_6 = Button(frame, text="Wyjście", width=15, command=window.quit)
    button_6.grid(row=6, column=0, sticky="w")
    label_6 = Label(frame, text=" - zakończenie działania programu")
    label_6.grid(row=6, column=1, sticky="w")


# optimised
def load_from_file(data, filename, directory):
    for widget in frame.winfo_children(): # clears all widgets inside frame
        widget.destroy()
    loaded_data = []
    with open(directory + '/' + filename, 'r') as file:
        while True:
            line = file.readline()
            if not line:
                break
            comma_index = []
            j = 0
            for i in range(len(line)):
                if line[i] == ',':
                    comma_index.append(j)
                j += 1
            code = line[:comma_index[0]]
            name = line[comma_index[0]+2:comma_index[1]]
            rate = float(line[comma_index[1]+2:comma_index[2]])
            loaded_data.append({'code': code, 'name': name, 'rate': rate})

    add_diff(data, loaded_data, filename)


# optimised
def add_diff(sorted_data, loaded_data, filename):
    for i in range(len(sorted_data)):
        loaded_data[i]["new_rate"] = data[i]["rate"]
        loaded_data[i]["change"] = round(get_change(sorted_data[i]['rate'], loaded_data[i]['rate']), 2)
    show_table(loaded_data, filename)


# optimised
def get_change(current, previous):
    if current == previous:
        return float(0)
    try:
        result = (abs(current - previous) / previous) * 100.0
        if current > previous:
            return float(result)
        else:
            return float(-result)
    except ZeroDivisionError:
        return float('inf')


# optimised
def data_sort(data, key, bool_reverse_element, filename):
    global reverse_list
    if key == 0:
        sort_by = 'code'
        reverse_list[key] = not reverse_list[key]
    elif key == 1:
        sort_by = 'name'
        reverse_list[key] = not reverse_list[key]
    elif key == 2:
        sort_by = 'new_rate'
        reverse_list[key] = not reverse_list[key]
    elif key == 3:
        sort_by = 'rate'
        reverse_list[key] = not reverse_list[key]
    elif key == 4:
        sort_by = 'change'
        reverse_list[key] = not reverse_list[key]

    if sort_by == 'name':
        sorted_data = sorted(data, key=lambda a: a[sort_by].lower(), reverse=bool_reverse_element)
    else:
        sorted_data = sorted(data, key=lambda a: a[sort_by], reverse=bool_reverse_element)
    show_table(sorted_data, filename)


# optimised
def show_table(sorted_loaded_data, file):
    for widget in table_frame.winfo_children(): # clears all widgets inside table_frame
        widget.destroy()

    global reverse_list
    button_code = Button(frame,
                   width=5,
                   fg='black',
                   text='Kod',
                   font=('Arial', 10, 'bold'),
                   command=lambda: data_sort(sorted_loaded_data, 0, reverse_list[0], filename))
    button_code.grid(row=0, column=0, sticky="w")

    button_name = Button(frame,
                   width=35,
                   fg='black',
                   text='Nazwa',
                   font=('Arial', 10, 'bold'),
                   command=lambda: data_sort(sorted_loaded_data, 1, reverse_list[1], filename))
    button_name.grid(row=0, column=1, sticky="w")

    button_new_rate = Button(frame,
                   width=12,
                   fg='black',
                   text='Obecny kurs',
                   font=('Arial', 10, 'bold'),
                   command=lambda: data_sort(sorted_loaded_data, 2, reverse_list[2], filename))
    button_new_rate.grid(row=0, column=2, sticky="w")

    button_rate = Button(frame,
                   width=10,
                   fg='black',
                   text='Stary kurs*',
                   font=('Arial', 10, 'bold'),
                   command=lambda: data_sort(sorted_loaded_data, 3, reverse_list[3], filename))
    button_rate.grid(row=0, column=3, sticky="w")

    button_change = Button(frame,
                   width=10,
                   fg='black',
                   text='Zmiana',
                   font=('Arial', 10, 'bold'),
                   command=lambda: data_sort(sorted_loaded_data, 4, reverse_list[4], filename))
    button_change.grid(row=0, column=4, sticky="w")

    for i in range(len(sorted_loaded_data)):
        label_code = Label(table_frame,
                       width=5,
                       fg='blue',
                       text=sorted_loaded_data[i]['code'],
                       anchor="w",
                       font=('Arial', 10, 'bold'))
        label_code.grid(row=i, column=0, sticky="w")

        label_name = Label(table_frame,
                       width=35,
                       fg='blue',
                       text=sorted_loaded_data[i]['name'],
                       anchor="w",
                       font=('Arial', 10, 'bold'))
        label_name.grid(row=i, column=1, sticky="w")

        label_new_rate = Label(table_frame,
                       width=12,
                       fg='blue',
                       text=sorted_loaded_data[i]['new_rate'],
                       anchor="w",
                       font=('Arial', 10, 'bold'))
        label_new_rate.grid(row=i, column=2, sticky="w")

        label_rate = Label(table_frame,
                       width=10,
                       fg='blue',
                       text=sorted_loaded_data[i]['rate'],
                       anchor="w",
                       font=('Arial', 10, 'bold'))
        label_rate.grid(row=i, column=3, sticky="w")

        label_change = Label(table_frame,
                   width=10,
                   fg='blue',
                   text=str(sorted_loaded_data[i]['change']) + '%',
                   anchor="w",
                   font=('Arial', 10, 'bold'))
        label_change.grid(row=i, column=4, sticky="w")

    label_info = Label(table_frame,
                       fg='grey',
                       text=('*dane porównawcze z: '
                            + file[9:11]
                            + ':'
                            + file[11:13]
                            + ':'
                            + file[13:15]
                            + ' '
                            + file[6:8]
                            + '/'
                            + file[4:6]
                            + '/'
                            + file[:4]),
                       anchor="w",
                       font=('Arial', 8, 'bold'))
    label_info.grid(row=len(sorted_loaded_data)+1, column=0, columnspan=5, sticky="w")


# optimised
def compare_from_file(data):
    window.title("Plik")
    for widget in frame.winfo_children(): # clears all widgets inside frame
        widget.destroy()
    for widget in table_frame.winfo_children(): # clears all widgets inside table_frame
        widget.destroy()

    if not FILES:
        error_label = Label(frame, text="Błąd. Brak plików do wczytania.")
        error_label.grid(row=0,
                         column=0,
                         columnspan=3,
                         sticky="w")
    else:
        variable = StringVar(frame)
        variable.set(FILES[0])
        w = OptionMenu(frame, variable, *FILES)
        w.config(width=25)
        w.grid(row=0, column=0, sticky="w")

        button = Button(frame, text="OK", command=lambda: load_from_file(data, variable.get(), directory))
        button.grid(row=0, column=1, sticky="w")


def converter_menu(data):
    window.title("Opcje")
    for widget in frame.winfo_children(): # clears all widgets inside frame
        widget.destroy()
    for widget in table_frame.winfo_children(): # clears all widgets inside table_frame
        widget.destroy()

    variable = StringVar(frame)
    variable.set(OPTIONS[0])
    w = OptionMenu(frame, variable, *OPTIONS)
    w.config(width=37)
    w.grid(row=0, column=0, sticky="w")

    button = Button(frame, text="OK", command=lambda: show_converter(data, variable.get()[:3], False), width=3)
    button.grid(row=0, column=1, sticky="W")


def show_converter(data, currency_code, bool_swap):
    for widget in frame.winfo_children(): # clears all widgets inside frame
        widget.destroy()

    for currency in data:
        if currency['code'] == currency_code:
            currency_rate = currency['rate']
            break

    if not bool_swap:
        entry_currency = Entry(frame, width=10)
        label_currency = Label(frame, text=" " + currency_code)
        label_result = Label(frame, text=" PLN")
    else:
        entry_currency = Entry(frame, width=10)
        label_currency = Label(frame, text=" PLN")
        label_result = Label(frame, text=" "  + currency_code)

    entry_currency.grid(row=0, column=0, sticky="w")
    label_currency.grid(row=0, column=1, sticky="w")

    variable = StringVar(frame)
    variable.set("Konwertuj \N{RIGHTWARDS BLACK ARROW}")
    w = OptionMenu(frame,
                   variable,
                   "Konwertuj \N{RIGHTWARDS BLACK ARROW}",
                   "Zamień waluty \N{LEFTWARDS BLACK ARROW}",
                   "Zmień walutę \N{LEFT RIGHT DOUBLE ARROW}")
    w.config(width=15)
    w.grid(row=0, column=2, sticky="w")

    button = Button(frame,
                    text="OK",
                    command=lambda: convert_swap(data, entry_currency,
                                                 currency_rate, currency_code,
                                                 variable.get(), bool_swap,
                                                 label_result), width=3)
    button.grid(row=0, column=3, sticky="w")
    label_result.grid(row=0, column=4, sticky="w")


def convert_swap(data,
                 entry_currency,
                 currency_rate,
                 currency_code,
                 mode,
                 bool_swap,
                 label_result):
    for widget in table_frame.winfo_children(): # clears all widgets inside table_frame
        widget.destroy()

    if mode == "Konwertuj \N{RIGHTWARDS BLACK ARROW}":
        try:
            currency_input = float(entry_currency.get())
        except ValueError:
            error_label = Label(table_frame, text="Błąd. Podaj prawidłową liczbę.")
            error_label.grid(row=1,
                            column=0,
                            columnspan=3,
                            sticky="w")
            entry_currency.delete(0, END)
        else:
            if currency_input < 0.01 and not bool_swap:
                error_label = Label(table_frame, text="Błąd. Podaj liczbę wiekszą niż 0.01.")
                error_label.grid(row=1,
                                column=0,
                                columnspan=3,
                                sticky="w")
                entry_currency.delete(0, END)
        
            elif currency_input / currency_rate < 0.01 and bool_swap:
                error_label = Label(table_frame, text="Błąd. Podaj liczbą większą niż " + str(round(max(100 * currency_rate), 0.01), 4) + '.')
                error_label.grid(row=1,
                                column=0,
                                columnspan=3,
                                sticky="w")
                entry_currency.delete(0, END)

            elif currency_input * currency_rate < 0.01 and not bool_swap:
                error_label = Label(table_frame, text="Błąd. Podaj liczbę większą niż " + str(round(max(0.01 / currency_rate), 0.01), 4) + '.')
                error_label.grid(row=1,
                                column=0,
                                columnspan=3,
                                sticky="w")
                entry_currency.delete(0, END)
            else:
                if not bool_swap:
                    result = currency_input * currency_rate
                    temp_string = " PLN"
                else:
                    result = currency_input / currency_rate
                    temp_string = " " + currency_code
                label_result['text'] = format(result, '.2f') + temp_string
    
    elif mode == "Zmień walutę \N{LEFT RIGHT DOUBLE ARROW}":
        converter_menu(data)
    elif mode == "Zamień waluty \N{LEFTWARDS BLACK ARROW}":
        bool_swap = not bool_swap
        entry_currency.delete(0, END)
        show_converter(data, currency_code, bool_swap)


# optimised
def save_to_file(data):
    for widget in frame.winfo_children(): # clears all widgets inside frame
        widget.destroy()
    for widget in table_frame.winfo_children(): # clears all widgets inside table_frame
        widget.destroy()

    now = datetime.now()
    file = now.strftime('%Y%m%d_%H%M%S')
    with open(directory + '/' + file + '.txt', 'w') as file:
        for i in range(len(data)):
            row = ''
            row += data[i]['code']
            row += ', '
            row += data[i]['name']
            row += ', '
            row += str(data[i]['rate'])
            row += ',\n'
            file.write(row)

    confirmation_label = Label(frame, text="Zapisano do pliku.")
    confirmation_label.grid(row=0, column=0, sticky="w")

    # global FILES
    FILES.clear()
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            FILES.append(filename)


# optimised
def list_credits():
    for widget in frame.winfo_children():  # clears all widgets inside frame
        widget.destroy()
    for widget in table_frame.winfo_children():  # clears all widgets inside table_frame
        widget.destroy()

    author_label = Label(frame, text="Autor: ", font=('Arial', 15, 'bold'))
    author_label.grid(row=0,
                    column=0,
                    pady=5,
                    rowspan=2,
                    sticky="w")
    author_link_label = Label(frame,
                              text="Dominik Sigulski",
                              font=('Arial', 15, 'bold'),
                              cursor="hand2")
    author_link_label.grid(row=0,
                    column=1,
                    pady=5,
                    rowspan=2,
                    sticky="w")
    author_link_label.bind("<Button-1>", lambda a: callback("https://github.com/Domin8668/"))

    header_label = Label(frame, text="Zbudowane dzięki:", font=('Arial', 10, 'bold'))
    header_label.grid(row=2,
                    column=0,
                    columnspan=2,
                    pady=3,
                    sticky="w")

    link1 = Label(frame,
                  text="stackoverflow.com",
                  fg="blue",
                  font=('Arial', 10, 'bold'),
                  borderwidth=2,
                  relief="raised",
                  cursor="hand2")
    link1.grid(row=3,
               column=0,
               columnspan=2,
               pady=3,
               sticky="w")
    link1.bind("<Button-1>", lambda a: callback("https://stackoverflow.com/"))

    link2 = Label(frame,
                  text="w3schools.com",
                  fg="blue",
                  font=('Arial', 10, 'bold'),
                  borderwidth=2,
                  relief="raised",
                  cursor="hand2")
    link2.grid(row=4,
               column=0,
               columnspan=2,
               pady=3,
               sticky="w")
    link2.bind("<Button-1>", lambda a: callback("https://www.w3schools.com/"))

    link3 = Label(frame,
                  text="geeksforgeeks.org",
                  fg="blue",
                  font=('Arial', 10, 'bold'),
                  borderwidth=2,
                  relief="raised",
                  cursor="hand2")
    link3.grid(row=5,
               column=0,
               columnspan=2,
               pady=3,
               sticky="w")
    link3.bind("<Button-1>", lambda a: callback("https://www.geeksforgeeks.org/"))

    link4 = Label(frame,
                  text="programiz.com",
                  fg="blue",
                  font=('Arial', 10, 'bold'),
                  borderwidth=2,
                  relief="raised",
                  cursor="hand2")
    link4.grid(row=6,
               column=0,
               columnspan=2,
               pady=3,
               sticky="w")
    link4.bind("<Button-1>", lambda a: callback("https://www.programiz.com/"))

    link5 = Label(frame,
                  text="pythonforbeginners.com",
                  fg="blue",
                  font=('Arial', 10, 'bold'),
                  borderwidth=2,
                  relief="raised",
                  cursor="hand2")
    link5.grid(row=7,
               column=0,
               columnspan=2,
               pady=3,
               sticky="w")
    link5.bind("<Button-1>", lambda a: callback("https://www.pythonforbeginners.com/"))

    link6 = Label(frame,
                  text="tutorialspoint.com",
                  fg="blue",
                  font=('Arial', 10, 'bold'),
                  borderwidth=2,
                  relief="raised",
                  cursor="hand2")
    link6.grid(row=8,
               column=0,
               columnspan=2,
               pady=3,
               sticky="w")
    link6.bind("<Button-1>", lambda a: callback("https://www.tutorialspoint.com/"))

    link7 = Label(frame,
                  text="python.org",
                  fg="blue",
                  font=('Arial', 10, 'bold'),
                  borderwidth=2,
                  relief="raised",
                  cursor="hand2")
    link7.grid(row=9,
               column=0,
               columnspan=2,
               pady=3,
               sticky="w")
    link7.bind("<Button-1>", lambda a: callback("https://www.python.org/"))


# optimised
def callback(url):
    webbrowser.open_new(url)


# scraper scraping data from https://www.nbp.pl/home.aspx?f=/kursy/kursya.html
data = scraper.nbp_scraper()

# finding available .txt files to load from them
FILES = []
directory = "Files"
for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        FILES.append(filename)
FILES = sorted(FILES, reverse=True)

# finding available options to show in a menu
OPTIONS = []
for currency in data:
    OPTIONS.append(currency['code'] + ' [' + currency['name'] + ']')

reverse_list = [False] * 5
reverse_list[0] = True

# creating a tkinter window and setting its properties
window = Tk()
window.title("Kalkulator")
window.geometry("720x900")

# creating 2 frames that will contain widgets
frame = Frame(window)
frame.pack()
table_frame = Frame(window)
table_frame.pack()

menubar = Menu(window)

filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Kursy walut", command=lambda: load_from_file(data, FILES[0], directory))
filemenu.add_command(label="Kalkulator walut", command=lambda: converter_menu(data))
filemenu.add_separator()
filemenu.add_command(label="Wyjście", command=window.quit)
menubar.add_cascade(label="Opcje", menu=filemenu)

filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Zapisz do pliku", command=lambda: save_to_file(data))
filemenu.add_command(label="Porównaj z pliku", command=lambda: compare_from_file(data))
menubar.add_cascade(label="Plik", menu=filemenu)

credits_menu = Menu(menubar, tearoff=0)
credits_menu.add_command(label="Informacje", command=lambda: list_credits())
menubar.add_cascade(label="Extra", menu=credits_menu)

window.config(menu=menubar)

list_functions()

window.mainloop()