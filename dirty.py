import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from db import *
db = Database()

def load_brands():
    brands = [i[1] for i in db.get_table(Table.CAR)]
    print(brands)
    return brands


def create_db():
    conn = sqlite3.connect('cars.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS cars (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        brand TEXT,
                        model TEXT,
                        equipment TEXT,
                        quantity INTEGER)''')
    conn.commit()
    conn.close()

def add_car(brand, model, equipment, quantity):

    names = [i[0] for i in db.get_table(Table.SET)]
    index = names.index(equipment)



    db.add_car(brand, model, 300, index, quantity)



def update_quantity(car_id, quantity):
    db.update_car_num(car_id, quantity)


def update_price(car_id, price):
    db.update_car_cost(car_id, price)


# def get_all_cars():
#     conn = sqlite3.connect('cars.db')
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM cars')
#     rows = cursor.fetchall()
#     conn.close()
#     return rows

def show_cars_by_brand(selected_brand=None):


    if selected_brand:
        cursor.execute('SELECT * FROM cars WHERE brand = ?', (selected_brand,))
    else:
       cursor.execute('SELECT * FROM cars')
    rows = db.get_table(Table.CAR)
    for row in tree.get_children():
        tree.delete(row)
    for row in rows:
        tree.insert('', 'end', values=row)


def add_car_window():
    brand = brand_entry.get()
    model = model_entry.get()
    equipment = equipment_combobox.get()
    quantity = quantity_entry.get()
    if brand and model and equipment and quantity.isdigit():
        add_car(brand, model, equipment, int(quantity))
        show_cars_by_brand(selected_brand.get()) # Перезагружаем таблицу
    else:
        messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля корректно.")


create_db()

root = tk.Tk()
root.title("Таблица машин")

# Выбор марки
selected_brand = tk.StringVar()
brand_label = tk.Label(root, text="Выберите марку:")
brand_label.pack()

# ----------------------------------------------------------------------


brand_combobox = ttk.Combobox(root, textvariable=selected_brand, values=load_brands())
brand_combobox.pack()

# Кнопка для отображения машин по выбранной марке
show_button = tk.Button(root, text="Показать машины", command=show_cars_by_brand)
show_button.pack()

# Таблица
columns = ('ID', 'Марка', 'Модель', 'Комплектация', 'Кол-во')
tree = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col)
tree.pack()

# Заполняем таблицу при запуске
# all_cars = get_all_cars() # Получаем все записи из бд
for row in db.get_table(Table.CAR): # Заполняем таблицу данными
    tree.insert('', 'end', values=row)

# ВОТ ТУТ МЫ ОБНОВЛЯЕМ ДЕРЕВО ____________________________________________

def create_entry_with_placeholder(master, placeholder):
    entry = tk.Entry(master)
    entry.placeholder = placeholder
    entry.config(fg="grey") # Подсказка будет серым цветом
    entry.insert(0, placeholder) # По умолчанию пишем подсказку

    def focus_in(event):
       if entry.get() == entry.placeholder: # Если стоит подсказка
           entry.delete(0, tk.END) # Удалить подсказку
           entry.config(fg="black") # Цвет текста сделать черным

    def focus_out(event):
        if not entry.get(): # Если поле пустое
             entry.config(fg="grey") # Цвет текста сделать серым
             entry.insert(0, placeholder) # Записать подсказку обратно

    entry.bind("<FocusIn>", focus_in)
    entry.bind("<FocusOut>", focus_out)
    return entry

def load_set():
    brands = [i[1] for i in db.get_table(Table.SET)]
    print(brands)
    return brands


# Ввод для добавления автомобилей
brand_label = ttk.Label(root, text="Выберете комплектацию")

brand_entry = create_entry_with_placeholder(root, "бренд")

model_entry = create_entry_with_placeholder(root, "модель")

selected_brand = tk.StringVar()  # Создание StringVar
equipment_combobox = ttk.Combobox(root, values=load_set(), textvariable=selected_brand)


quantity_entry = create_entry_with_placeholder(root, "количество")

brand_entry.pack()
model_entry.pack()
brand_label.pack()
equipment_combobox.pack()
quantity_entry.pack()


add_button = tk.Button(root, text="Добавить", command=add_car_window)
add_button.pack()

# Кнопки для изменения количества и цены
update_quantity_button = tk.Button(root, text="Изменить количество", command=lambda: update_quantity(car_id_entry.get(), new_quantity_entry.get()))
update_quantity_button.pack()

update_price_button = tk.Button(root, text="Изменить цену", command=lambda: update_price(car_id_entry.get(), new_price_entry.get()))
update_price_button.pack()



root.mainloop()
db.close()
