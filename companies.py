import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb
#import sqlite3

# импортируем свои модули
import __general_procedures as gp
import companies_db as companies_db  # БД для форм компаний


# Словарь фильтров
# companies_filter_dict = {'company_name': '', 'company_description': ''}
companies_filter_dict = {}


class Companies(tk.Frame):
    """ Базовый класс для компаний, меню и список компаний """
    def __init__(self, root, main):
        super().__init__(root)

        self.root = root  # frm_content_all
        self.main = main  # Main

        self.companies_db = companies_db.CompaniesDB()  # Подключаем БД компаний

        self.init_companies()
        self.show_companies()  # Загружаем данные на форму

    def init_companies(self):
        # для отображения на полное окно
        self.pack(fill=tk.BOTH, expand=True)

        # Общая рамка для модуля
        # frm_companies = ttk.Frame(app.frm_content_all, relief=tk.RAISED, borderwidth=3)
        frm_companies = ttk.Frame(self, relief=tk.RAISED, borderwidth=0)
        frm_companies.pack(fill=tk.BOTH, expand=True)

        # Рамка верхнего toolbar
        frm_top_toolbar = ttk.Frame(frm_companies, relief=tk.RAISED, borderwidth=0)
        frm_top_toolbar.pack(fill=tk.X)

        # Кнопки
        # 1
        self.btn_open_filter = tk.Button(frm_top_toolbar, text='Фильтр', **self.main.btn_style,
                                         command=self.open_company_filter)
        self.btn_open_filter.pack(side=tk.LEFT, **self.main.btn_pack_padding)
        # 2
        btn_open_company_new = tk.Button(frm_top_toolbar, text='Добавить', **self.main.btn_style,
                                         command=self.open_new_company)
        btn_open_company_new.pack(side=tk.LEFT, **self.main.btn_pack_padding)
        # 3
        btn_open_company_update = tk.Button(frm_top_toolbar, text='Редактировать', **self.main.btn_style,
                                            command=self.open_update_company)
        btn_open_company_update.pack(side=tk.LEFT, **self.main.btn_pack_padding)
        # 4
        btn_open_company_delete = tk.Button(frm_top_toolbar, text='Удалить', **self.main.btn_style,
                                            command=self.delete_companies)
        btn_open_company_delete.pack(side=tk.LEFT, **self.main.btn_pack_padding)

        # контент модуля
        frm_companies_content = ttk.Frame(frm_companies, relief=tk.RAISED, borderwidth=0)
        frm_companies_content.pack(fill=tk.BOTH, expand=True)

        # список Treeview
        self.companies_table = ttk.Treeview(frm_companies_content, columns=('id_company', 'company_name',
                                                                            'company_description'),
                                            height=10, show='headings')
        # параметры столбцов
        self.companies_table.column("id_company", width=40, anchor=tk.CENTER)
        self.companies_table.column("company_name", width=150, anchor=tk.CENTER)
        self.companies_table.column("company_description", width=355, anchor=tk.CENTER)
        # названия столбцов
        self.companies_table.heading('id_company', text='ID')
        self.companies_table.heading('company_name', text='Наименование')
        self.companies_table.heading('company_description', text='Описание')
        # вывод с выравниванием по левой стороне
        self.companies_table.pack(fill="both", side='left', expand=True)
        # вешаем контекстное меню на ЛКМ
        self.companies_table.bind('<Button-3>', self.show_context_menu)

        # полоса прокрутки для списка
        scroll = tk.Scrollbar(frm_companies_content, command=self.companies_table.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.companies_table.configure(yscrollcommand=scroll.set)

        # контекстное меню для копирования
        self.context_menu = tk.Menu(self.companies_table, tearoff=0)
        self.context_menu.add_command(
            label='Копировать наименование', command=self.copy_name)
        self.context_menu.add_command(
            label='Копировать описание', command=self.copy_description)
        self.context_menu.add_command(
            label='Копировать все', command=self.copy_all)

    def show_context_menu(self, event):
        """ Процедура вывода контекстного меню
        :param event:
        :return:
        """
        if self.companies_table.focus() != '':
            self.companies_table.identify_row(event.y)
            self.context_menu.post(event.x_root, event.y_root)

    def copy_name(self):
        """ Процедура копирования в буфер обмена """
        self.root.clipboard_clear()
        self.root.clipboard_append(self.companies_table.set(self.companies_table.selection()[0], '#2'))

    def copy_description(self):
        """ Процедура копирования в буфер обмена """
        self.root.clipboard_clear()
        self.root.clipboard_append(self.companies_table.set(self.companies_table.selection()[0], '#3'))

    def copy_all(self):
        """ Процедура копирования в буфер обмена """
        self.root.clipboard_clear()
        self.root.clipboard_append(self.companies_table.set(self.companies_table.selection()[0], '#2') + '\n' +
                                   self.companies_table.set(self.companies_table.selection()[0], '#3'))

    def show_companies(self):
        """ Процедура вывода списка компаний согласно данных БД и фильтров """
        self.color_btn_filter()  # Цвет кнопки фильтра
        [self.companies_table.delete(i) for i in self.companies_table.get_children()]  # Очистка таблицы
        data = self.companies_db.get_company_list_by_filter(companies_filter_dict)
        [self.companies_table.insert('', 'end', values=row) for row in data]

    def delete_companies(self):
        """ Процедура удаления выбранных компаний """
        if self.companies_table.focus() != '':
            answer = mb.askyesno(title='Запрос действия',
                                 message="Хотите удалить выбранные элементы?")
            if answer:  # если Да = True
                # Цикл удаление нескольких записей
                # [ids.append(row) for row in self.companies_table.selection()]
                ids = []  # кортеж id выделенных элементов
                for selection_item in self.companies_table.selection():
                    ids.append(self.companies_table.set(selection_item, '#1'),)
                self.companies_db.delete_companies(ids)
                self.show_companies()  # перезагружаем список

                ## Запятая (self.tree.set(select, '#1'),)) - для удаление при более 10 записей
                #for selection_item in self.companies_table.selection():
                #    self.db.c_sqlite3.execute(
                #        '''DELETE FROM companies WHERE id_company=?''', (self.companies_table.set(selection_item, '#1'),)
                #    )
                #self.db.conn_sqlite3.commit()
        else:
            mb.showwarning('Предупреждение', 'Выберите компанию')

    def open_new_company(self):
        """ Открываем окно ввода данных новой компании """
        NewCompany(self)

    def open_update_company(self):
        """ Открываем окно обновления выбранной компании """
        if self.companies_table.focus() != '':
            UpdateCompany(self, self.companies_table.set(self.companies_table.selection()[0], '#1'))
        else:
            mb.showwarning('Предупреждение', 'Выберите компанию')

    def open_company_filter(self):
        """ Открываем окно фильтров """
        FilterCompany(self)

    def color_btn_filter(self):
        """ Процедкра смены цвета кнопки Фильтр """
        if companies_filter_dict:  # Если есть фильтры
            self.btn_open_filter.configure(bg='#A9A9A9')
        else:
            self.btn_open_filter.configure(bg='#f0f0f0')

    def apply_company_filter(self, company_name, company_description):
        """ Процедура фильтрации по введенной компании и описанию
        :param company_name: Название компании
        :param company_description: Описание для компании
        :return none
        """
        companies_filter_dict.clear()  # чистим словарь
        # пересоздаем словарь
        if company_name:
            companies_filter_dict['company_name'] = company_name
        if company_description:
            companies_filter_dict['company_description'] = company_description
        self.show_companies()  # список компаний

    def clear_company_filter(self):
        """ Очищаем фильтр компаний """
        # for key in companies_filter_dict:
        #    companies_filter_dict[key] = ''  # обнуляем ключи
        #    self.show_companies()     # перезегружаем список компаний
        companies_filter_dict.clear()
        self.show_companies()  # перезегружаем список компаний


class Company(tk.Toplevel):
    """ Базовый класс формы компании """
    def __init__(self, parent=None):
        super().__init__()

        self.parent = parent  # Передаем класс Main
        self.companies_db = companies_db.CompaniesDB()  # Подключаем БД компаний

        self.init_company()

        self.clear_company()

    def init_company(self):
        self.title('Добавить компанию')
        self.geometry('415x200+400+300')
        self.resizable(False, False)

        # Добавляем функции модального, прехватываем фокус не нем до закрытия
        self.grab_set()
        self.focus_set()

        # Создаем поля формы
        lbl_company_name = tk.Label(self, text='Название компании')
        lbl_company_name.place(x=50, y=20)
        self.ent_company_name = ttk.Entry(self)
        self.ent_company_name.place(x=200, y=20, width=180)
        self.ent_company_name.bind("<Control-KeyPress>", gp.keys)
        self.ent_company_name.focus()

        lbl_company_description = tk.Label(self, text='Описание')
        lbl_company_description.place(x=50, y=50)
        self.txt_company_description = tk.Text(self)
        self.txt_company_description.place(x=200, y=50, width=180, height=100)
        self.txt_company_description.bind("<Control-KeyPress>", gp.keys)

        # Полоса прокрутки
        scroll = tk.Scrollbar(self, command=self.txt_company_description.yview)
        # scroll.pack(side=tk.RIGHT, fill=tk.Y)
        scroll.place(x=380, y=50, height=100)
        self.txt_company_description.configure(yscrollcommand=scroll.set)

        self.btn_cancel = ttk.Button(self, text='Отмена', command=self.destroy)
        self.btn_cancel.place(x=305, y=160)

    def clear_company(self):
        """ Очищаем поля формы """
        self.ent_company_name.delete(0, tk.END)
        self.txt_company_description.delete(1.0, tk.END)

    def check_empty(self):
        """ Процедура проверки на пустые поля формы
        :return: True/False
        """
        if len(self.ent_company_name.get()) == 0:
            mb.showwarning('Предупреждение', 'Введите компанию')
            return False
        return True

    def check_exists(self):
        """ Процедура проверки дублей по введенным данным
        :return: True/False
        """
        company_name = self.ent_company_name.get()
        data = self.companies_db.get_company_name_by_name(company_name)
        if data:
            mb.showwarning('Предупреждение', 'Дубль компании <' + data + '>')
            return False
        return True


class NewCompany(Company):
    """ Класс формы добавления компании """
    def __init__(self, parent):  # Конструктор
        super().__init__()

        self.parent = parent  # Main

        self.init_new_company()

    def init_new_company(self):
        self.title('Добавить компанию')

        btn_save = ttk.Button(self, text='Сохранить', command=self.save_new_company)
        btn_save.place(x=220, y=160)
        #btn_save.bind('<Button-1>', lambda event: self.main.save_new_company(
        #    self.ent_company_name.get(), self.txt_company_description.get('1.0', tk.END)
        # ))

    def save_new_company(self):
        """ Процедура сохранения нового логина """
        if self.check_empty() and self.check_exists():  # проверка на пустые поля и дубль
            # Получаем поля с формы
            company_name = self.ent_company_name.get()
            company_description = self.txt_company_description.get('1.0', tk.END)
            self.companies_db.insert_new_company(company_name, company_description)  # сохраняем
            self.parent.show_companies()  # выводим на форму
            self.btn_cancel.invoke()  # имитация клика по "Отмена"


class UpdateCompany(Company):
    """ Класс формы обновления компании """
    def __init__(self, parent, id_company):  # Конструктор
        super().__init__()

        self.parent = parent  # Main
        self.id_company = id_company

        self.init_update_company()
        self.get_company_for_update()

    def init_update_company(self):
        self.title('Обновить компанию')
        btn_update = ttk.Button(self, text='Обновить', command=self.update_company)
        btn_update.place(x=220, y=160)
        # # пример bind через lambda
        # btn_save.bind('<Button-1>', lambda event: self.companies_db.update_company_by_id(
        #    self.app.companies.companies_table.set(self.app.companies.companies_table.selection()[0], '#1'),
        #    self.ent_company_name.get(), self.txt_company_description.get('1.0', tk.END)
        # ))
        # btn_save.bind('<Button-1>', lambda event: self.app.companies.show_companies(),
        #              add='+')  # вешаем еще событие на кнопку
        # btn_save.bind('<Button-1>', lambda event: self.destroy(), add='+')  # вешаем еще событие на кнопку

    def get_company_for_update(self):
        """ Процедура получения и вывода на форму данных выделенной компании """
        data = self.companies_db.get_company_by_id(self.id_company)
        # Выводим значения в поля формы
        self.ent_company_name.insert(0, data[1])
        self.txt_company_description.insert(1.0, data[2])

    def update_company(self):
        """ Процедура сохранения новой компании """
        if self.check_empty():  # проверка на пустые поля
            # получаем поля с формы
            company_name = self.ent_company_name.get()
            company_description = gp.get_text_in_one_line(self.txt_company_description.get('1.0', tk.END))
            self.companies_db.update_company_by_id(self.id_company, company_name, company_description)  # обновляем
            self.parent.show_companies()  # выводим на форму
            self.btn_cancel.invoke()  # имитация клика по "Отмена"


class FilterCompany(tk.Toplevel):
    """ Класс формы фильльтра для отображения списка компаний """
    def __init__(self, parent):
        super().__init__()

        self.parent = parent  # Main

        self.init_filter_company()
        self.companies = Companies

    def init_filter_company(self):
        self.title('Фильтр компаний')
        self.geometry('350x125+400+300')
        self.resizable(False, False)

        # Добавляем функции модального, прехватываем фокус до закрытия
        self.grab_set()
        self.focus_set()

        lbl_company_name = tk.Label(self, text='Компания')
        lbl_company_name.place(x=50, y=20)
        self.ent_company_name = ttk.Entry(self)
        self.ent_company_name.place(x=120, y=20, width=180)
        self.ent_company_name.insert(0, companies_filter_dict.get('company_name', ''))  # Имя
        self.ent_company_name.bind("<Control-KeyPress>", gp.keys)
        self.ent_company_name.focus()

        lbl_company_description = tk.Label(self, text='Описание')
        lbl_company_description.place(x=50, y=50)
        self.ent_company_description = ttk.Entry(self)
        self.ent_company_description.place(x=120, y=50, width=180)
        self.ent_company_description.insert(0, companies_filter_dict.get('company_description', ''))  # Описание
        self.ent_company_description.bind("<Control-KeyPress>", gp.keys)

        btn_clear_company_filter = ttk.Button(self, text='Сбросить')
        btn_clear_company_filter.place(x=65, y=85)
        btn_clear_company_filter.bind('<Button-1>', lambda event: self.parent.clear_company_filter())
        btn_clear_company_filter.bind('<Button-1>', lambda event: self.destroy(), add='+')  # второе событие

        btn_apply_company_filter = ttk.Button(self, text='Применить')
        btn_apply_company_filter.place(x=145, y=85)
        btn_apply_company_filter.bind('<Button-1>', lambda event: self.parent.apply_company_filter(
            self.ent_company_name.get(), self.ent_company_description.get()))
        btn_apply_company_filter.bind('<Button-1>', lambda event: self.destroy(), add='+')  # второе событие

        btn_closed_company_filter = ttk.Button(self, text='Отмена', command=self.destroy)
        btn_closed_company_filter.place(x=225, y=85)
