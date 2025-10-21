import pandas as pd
import psycopg2
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import subprocess  # Для выполнения системных команд

class MeterTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Учет показателей счетчиков")

        # Устанавливаем размер окна
        self.root.geometry("1500x600")  # Устанавливаем нужный размер окна

        # Подключение к базе данных PostgreSQL
        self.db_config = {
            "dbname": "db_home",  # Название вашей базы данных
            "user": "postgres",    # Ваше имя пользователя PostgreSQL
            "password": "8468",    # Ваш пароль
            "host": "localhost",   # Адрес вашего сервера (localhost для локальной базы)
            "port": "5432"         # Порт PostgreSQL
        }
        self.conn = None  # Инициализируем conn как None
        self.cursor = None  # Инициализируем cursor как None
        self.connect_db()

        # Создание фреймов для формы и таблицы
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Вкладка для ввода данных
        self.create_input_tab()

        # Вкладка для отчетности
        self.create_table_display()

    def connect_db(self):
        # Проверка, запущена ли база данных, если нет - запускаем
        if not self.is_db_running():
            self.start_postgres()

        try:
            # Попытка подключиться к базе данных
            self.conn = psycopg2.connect(**self.db_config)
            self.cursor = self.conn.cursor()  # Инициализируем курсор после подключения
            self.conn.set_client_encoding('UTF8')  # Устанавливаем кодировку соединения
            print("Подключение к базе данных установлено")
        except psycopg2.OperationalError as e:
            print(f"Ошибка подключения к базе данных: {e}")
            messagebox.showerror("Ошибка", f"Ошибка подключения к базе данных: {e}")
            self.root.quit()

    def is_db_running(self):
        # Проверка, работает ли база данных
        try:
            connection = psycopg2.connect(**self.db_config)
            connection.close()
            return True
        except psycopg2.OperationalError:
            return False

    def start_postgres(self):
        # Запуск службы PostgreSQL на Windows
        try:
            subprocess.run(['net', 'start', 'postgresql'], check=True)
            print("Служба PostgreSQL запущена")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Ошибка", f"Не удалось запустить PostgreSQL: {e}")
            self.root.quit()

    def create_input_tab(self):
        # Вкладка для ввода данных
        self.input_frame = ttk.Frame(self.main_frame)
        self.input_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        # Поля для ввода данных
        self.entries = {}

        # Месяц
        ttk.Label(self.input_frame, text="Месяц").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.month_combo = ttk.Combobox(self.input_frame, values=["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"])
        self.month_combo.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.entries["Месяц"] = self.month_combo

        # Счетчик ХВС
        ttk.Label(self.input_frame, text="Счетчик ХВС").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.water_hvs = ttk.Entry(self.input_frame)
        self.water_hvs.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.entries["Счетчик ХВС"] = self.water_hvs

        # Счетчик ГВС
        ttk.Label(self.input_frame, text="Счетчик ГВС").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.water_gvs = ttk.Entry(self.input_frame)
        self.water_gvs.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        self.entries["Счетчик ГВС"] = self.water_gvs

        # Тариф Т1
        ttk.Label(self.input_frame, text="Тариф Т1").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.tariff_t1 = ttk.Entry(self.input_frame)
        self.tariff_t1.grid(row=3, column=1, padx=10, pady=10, sticky="ew")
        self.entries["Тариф Т1"] = self.tariff_t1

        # Тариф Т2
        ttk.Label(self.input_frame, text="Тариф Т2").grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.tariff_t2 = ttk.Entry(self.input_frame)
        self.tariff_t2.grid(row=4, column=1, padx=10, pady=10, sticky="ew")
        self.entries["Тариф Т2"] = self.tariff_t2

        # Дата подачи (ввод вручную)
        ttk.Label(self.input_frame, text="Дата подачи показаний (YYYY-MM-DD)").grid(row=5, column=0, padx=10, pady=10, sticky="w")
        self.date_submission = ttk.Entry(self.input_frame)
        self.date_submission.grid(row=5, column=1, padx=10, pady=10, sticky="ew")
        self.entries["Дата подачи показаний"] = self.date_submission

        # Дата оплаты (ввод вручную)
        ttk.Label(self.input_frame, text="Дата оплаты (YYYY-MM-DD)").grid(row=6, column=0, padx=10, pady=10, sticky="w")
        self.date_payment = ttk.Entry(self.input_frame)
        self.date_payment.grid(row=6, column=1, padx=10, pady=10, sticky="ew")
        self.entries["Дата оплаты"] = self.date_payment

        # Банк оплаты
        ttk.Label(self.input_frame, text="Банк оплаты").grid(row=7, column=0, padx=10, pady=10, sticky="w")
        self.bank_payment = ttk.Combobox(self.input_frame, values=["Сбербанк", "Альфа-Банк", "Тинькофф"])
        self.bank_payment.grid(row=7, column=1, padx=10, pady=10, sticky="ew")
        self.entries["Банк оплаты"] = self.bank_payment

        # Общий платеж
        ttk.Label(self.input_frame, text="Общий платеж").grid(row=8, column=0, padx=10, pady=10, sticky="w")
        self.total_payment = ttk.Entry(self.input_frame)
        self.total_payment.grid(row=8, column=1, padx=10, pady=10, sticky="ew")
        self.entries["Общий платеж"] = self.total_payment

        # Кнопки
        ttk.Button(self.input_frame, text="Добавить данные", command=self.submit_data).grid(row=9, column=0, columnspan=2, pady=15, sticky="ew")
        ttk.Button(self.input_frame, text="Очистить форму", command=self.clear_form).grid(row=10, column=0, columnspan=2, pady=10, sticky="ew")
        ttk.Button(self.input_frame, text="Экспорт в Excel", command=self.export_to_excel).grid(row=11, column=0, columnspan=2, pady=10, sticky="ew")
        ttk.Button(self.input_frame, text="Удалить данные", command=self.delete_data).grid(row=12, column=0, columnspan=2, pady=10, sticky="ew")

    def create_table_display(self):
        # Создание таблицы для отображения данных из базы на основной вкладке
        self.table_frame = ttk.Frame(self.main_frame)
        self.table_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # Создание таблицы для отображения данных из базы
        self.tree = ttk.Treeview(self.table_frame, columns=("month", "cold_water", "hot_water", "t1", "t2", "submission_date", "payment_date", "payment_bank", "total_payment"), show="headings")

        # Установка заголовков для столбцов
        self.tree.heading("month", text="Месяц")
        self.tree.heading("cold_water", text="Счетчик ХВС")
        self.tree.heading("hot_water", text="Счетчик ГВС")
        self.tree.heading("t1", text="Тариф Т1")
        self.tree.heading("t2", text="Тариф Т2")
        self.tree.heading("submission_date", text="Дата подачи")
        self.tree.heading("payment_date", text="Дата оплаты")
        self.tree.heading("payment_bank", text="Банк оплаты")
        self.tree.heading("total_payment", text="Общий платеж")

        # Устанавливаем ширину столбцов
        self.tree.column("month", width=100)
        self.tree.column("cold_water", width=100)
        self.tree.column("hot_water", width=100)
        self.tree.column("t1", width=100)
        self.tree.column("t2", width=100)
        self.tree.column("submission_date", width=150)
        self.tree.column("payment_date", width=150)
        self.tree.column("payment_bank", width=120)
        self.tree.column("total_payment", width=120)

        # Добавляем полосу прокрутки для Treeview
        self.scrollbar_y = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.scrollbar_y.pack(side="right", fill="y", padx=10, pady=10)
        self.tree.configure(yscrollcommand=self.scrollbar_y.set)

        self.scrollbar_x = ttk.Scrollbar(self.table_frame, orient="horizontal", command=self.tree.xview)
        self.scrollbar_x.pack(side="bottom", fill="x", padx=10, pady=10)
        self.tree.configure(xscrollcommand=self.scrollbar_x.set)

        self.tree.pack(fill="both", expand=True)

        # Загружаем данные из базы данных
        self.load_data()

    def load_data(self):
        # Загружаем данные из базы данных
        try:
            query = "SELECT * FROM meters;"
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            # Очищаем старые данные в таблице
            for row in self.tree.get_children():
                self.tree.delete(row)

            # Заполняем таблицу новыми данными
            for row in rows:
                self.tree.insert("", "end", values=row)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при загрузке данных из базы: {str(e)}")

    def submit_data(self):
        # Получение данных из полей ввода и добавление в таблицу базы данных
        data = {}
        print("Получаем данные из формы...")  # Отладочный вывод

        for col, entry in self.entries.items():
            if isinstance(entry, ttk.Combobox):  # Если это выпадающий список
                data[col] = entry.get()
            elif isinstance(entry, ttk.Entry):  # Если это обычное поле ввода
                data[col] = entry.get()

        # Печать полученных данных для отладки
        print("Данные для вставки:", data)

        # Проверка, что все поля заполнены
        if "" in data.values():
            messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля")
            return

        try:
            # Вставка данных в таблицу meters
            self.cursor.execute("""
                INSERT INTO meters (month, cold_water, hot_water, t1, t2, submission_date, payment_date, payment_bank, total_payment)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                data["Месяц"],
                float(data["Счетчик ХВС"]),
                float(data["Счетчик ГВС"]),
                float(data["Тариф Т1"]),
                float(data["Тариф Т2"]),
                data["Дата подачи показаний"],
                data["Дата оплаты"],
                data["Банк оплаты"],
                float(data["Общий платеж"])
            ))

            # Завершаем транзакцию для вставки данных в таблицу meters
            self.conn.commit()
            messagebox.showinfo("Успех", "Данные успешно добавлены")

            # Обновляем таблицу
            self.load_data()

        except Exception as e:
            # Если произошла ошибка, откатываем изменения
            self.conn.rollback()
            messagebox.showerror("Ошибка", f"Ошибка при добавлении данных: {str(e)}")

    def delete_data(self):
        # Получение выбранной строки из таблицы и удаление данных
        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите строку для удаления")
            return

        # Получаем ID строки
        item_data = self.tree.item(selected_item)["values"]
        month = item_data[0]  # Месяц как уникальный идентификатор

        # Убедимся, что month - это строка
        month = str(month)

        # Удаляем данные из базы данных
        try:
            self.cursor.execute("DELETE FROM meters WHERE month = %s", (month,))
            self.conn.commit()

            # Удаляем строку из таблицы
            self.tree.delete(selected_item)
            messagebox.showinfo("Успех", f"Данные за {month} успешно удалены")

        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Ошибка", f"Ошибка при удалении данных: {str(e)}")

    def export_to_excel(self):
        # Извлечение данных из базы данных и экспорт в Excel
        try:
            query = "SELECT * FROM meters;"
            df = pd.read_sql_query(query, self.conn)
            df.to_excel("meters_data.xlsx", index=False)
            messagebox.showinfo("Успех", "Данные успешно сохранены в Excel")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при экспорте данных в Excel: {str(e)}")

    def clear_form(self):
        # Очистить все поля ввода
        for entry in self.entries.values():
            if isinstance(entry, (ttk.Entry, ttk.Combobox)):
                entry.delete(0, tk.END)

# Создание окна
root = tk.Tk()
app = MeterTrackerApp(root)
root.mainloop()
