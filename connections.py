import ctypes
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb
import re

# импортируем свои модули
import __general_procedures as gp
import logins as logins
import connections_db as connections_db  # БД для форм подключения
import companies_db as companies_db  # БД для форм компаний
import connection_types_db as connection_types_db  # БД для форм типов подключения

# import new_login_by_id_connection as new_login_by_id_connection
# import connection_types as connection_types


# словать фильтров
# connections_filter_dict = {'id_company': '', 'id_connection_type': '', 'connection_ip': '', 'connection_description': ''}
connections_filter_dict = {}


class Connections(tk.Frame):
    """ Базовый класс формы списка подключений """
    def __init__(self, root, main):
        super().__init__(root)

        self.root = root  # frm_content_all
        self.main = main  # Main
        self.connections_db = connections_db.ConnectionsDB()  # Подключаем бд подключений

        self.init_connections()
        self.show_connections()  # Загружаем данные на форму

    def init_connections(self):
        # Для отображения на полное окно
        self.pack(fill=tk.BOTH, expand=True)

        # Базовая рамка формы
        # frm_conns = ttk.Frame(app.frm_content_all, relief=tk.RAISED, borderwidth=3)
        frm_conns = ttk.Frame(self, relief=tk.RAISED, borderwidth=0)
        frm_conns.pack(fill=tk.BOTH, expand=True)

        # Рамка верхнего toolbar для кнопок
        frm_conns_toolbar = ttk.Frame(frm_conns, relief=tk.RAISED, borderwidth=0)
        frm_conns_toolbar.pack(fill=tk.X)

        # Кнопки
        # 1
        self.btn_open_filter = tk.Button(frm_conns_toolbar, text='Фильтр', **self.main.btn_style,
                                         command=self.open_filter_connection)
        self.btn_open_filter.pack(side=tk.LEFT, **self.main.btn_pack_padding)
        # 2
        btn_open_new = tk.Button(frm_conns_toolbar, text='Добавить', **self.main.btn_style,
                                 command=self.open_new_connection)
        btn_open_new.pack(side=tk.LEFT, **self.main.btn_pack_padding)
        # 3
        btn_open_update = tk.Button(frm_conns_toolbar, text='Редактировать', **self.main.btn_style,
                                    command=self.open_update_connection)
        btn_open_update.pack(side=tk.LEFT, **self.main.btn_pack_padding)
        # 4
        btn_delete = tk.Button(frm_conns_toolbar, text='Удалить', **self.main.btn_style,
                               command=self.delete_connections)
        btn_delete.pack(side=tk.LEFT, **self.main.btn_pack_padding)
        # 7
        btn_open_login_list = tk.Button(frm_conns_toolbar, text='Открыть логины', **self.main.btn_style,
                                        command=self.open_logins)
        btn_open_login_list.pack(side=tk.LEFT, **self.main.btn_pack_padding)

        # Рамка контента
        frm_conns_content = ttk.Frame(frm_conns, relief=tk.RAISED, borderwidth=0)
        frm_conns_content.pack(fill=tk.BOTH, expand=True)

        # Таблица Treeview
        self.treeview_list = ttk.Treeview(frm_conns_content,
                                          columns=('id_connection', 'company_name', 'connection_type_name',
                                                   'connection_ip', 'connection_description'),
                                          height=10, show='headings')
        # Параметры столбцов
        self.treeview_list.column("id_connection", width=40, anchor=tk.CENTER)
        self.treeview_list.column("company_name", width=110, anchor=tk.CENTER)
        self.treeview_list.column("connection_type_name", width=110, anchor=tk.CENTER)
        self.treeview_list.column("connection_ip", width=100, anchor=tk.CENTER)
        self.treeview_list.column("connection_description", width=300, anchor=tk.CENTER)

        # Названия столбцов
        self.treeview_list.heading('id_connection', text='ID')
        self.treeview_list.heading('company_name', text='Компания')
        self.treeview_list.heading('connection_type_name', text='Тип подключения')
        self.treeview_list.heading('connection_ip', text='Ip-адрес (домен)')
        self.treeview_list.heading('connection_description', text='Описание для подключения')
        # Вывод с выравниванием по левой стороне
        self.treeview_list.pack(fill="both", side='left', expand=True)
        # Вешаем контекстное меню на ЛКМ
        self.treeview_list.bind('<Button-3>', self.show_context_menu)

        # Полоса прокрутки для списка
        scroll = tk.Scrollbar(frm_conns_content, command=self.treeview_list.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.treeview_list.configure(yscrollcommand=scroll.set)

        # Контекстное меню для копирования
        self.context_menu = tk.Menu(self.treeview_list, tearoff=0)
        self.context_menu.add_command(
            label='Копировать компанию', command=self.copy_company)
        self.context_menu.add_command(
            label='Копировать тип подкл.', command=self.copy_conn_type)
        self.context_menu.add_command(
            label='Копировать домен', command=self.copy_domain)
        self.context_menu.add_command(
            label='Копировать описание', command=self.copy_description)
        # self.context_menu.add_command(
        #     label='Копировать все', command=self.copy_all)

    def show_context_menu(self, event):
        """ Процедура вывода контекстного меню
        :param event:
        :return:
        """
        if self.treeview_list.focus() != '':
            self.treeview_list.identify_row(event.y)
            self.context_menu.post(event.x_root, event.y_root)

    def copy_company(self):
        """ Процедура копирования в буфер обмена """
        self.root.clipboard_clear()
        self.root.clipboard_append(self.treeview_list.set(self.treeview_list.selection()[0], '#2'))

    def copy_conn_type(self):
        """ Процедура копирования в буфер обмена """
        self.root.clipboard_clear()
        self.root.clipboard_append(self.treeview_list.set(self.treeview_list.selection()[0], '#3'))

    def copy_domain(self):
        """ Процедура копирования в буфер обмена """
        self.root.clipboard_clear()
        self.root.clipboard_append(self.treeview_list.set(self.treeview_list.selection()[0], '#4'))

    def copy_description(self):
        """ Процедура копирования в буфер обмена """
        self.root.clipboard_clear()
        self.root.clipboard_append(self.treeview_list.set(self.treeview_list.selection()[0], '#5'))

    def copy_all(self):
        """ Процедура копирования в буфер обмена """
        self.root.clipboard_clear()
        self.root.clipboard_append(self.treeview_list.set(self.treeview_list.selection()[0], '#2') + '\n' +
                                   self.treeview_list.set(self.treeview_list.selection()[0], '#3') + '\n' +
                                   self.treeview_list.set(self.treeview_list.selection()[0], '#4') + '\n' +
                                   self.treeview_list.set(self.treeview_list.selection()[0], '#5'))

    def show_connections(self):
        """ Процедура заполнения списка тиов подключения согласно данных БД и фильтров """
        self.color_btn_filter()  # Цвет кнопки фильтра
        [self.treeview_list.delete(i) for i in self.treeview_list.get_children()]  # Чистим таблицу
        data = self.connections_db.get_connections_by_filter(connections_filter_dict)
        [self.treeview_list.insert('', 'end', values=row) for row in data]  # Выводим список на форму

    def delete_connections(self):
        """ Процедура удаления выбранных типов подключения """
        if self.treeview_list.focus() != '':
            answer = mb.askyesno(title='Запрос действия',
                                 message="Хотите удалить выбранные элементы?")
            if answer:  # если Да = True
                ids = []  # кортеж id выделенных элементов
                for selection_item in self.treeview_list.selection():
                    ids.append(self.treeview_list.set(selection_item, '#1'), )
                self.connections_db.delete_connections(ids)
                self.show_connections()  # перезагружаем список
        else:
            mb.showwarning('Предупреждение', 'Выберите подключение')

    def open_update_connection(self):
        """ Открываем окно для обновления выбранного подключения """
        if self.treeview_list.focus() != '':
            id_connection = self.treeview_list.set(self.treeview_list.selection()[0], '#1')
            UpdateConnection(self, id_connection)
        else:
            mb.showwarning('Предупреждение', 'Выберите подключение')

    def open_new_connection(self):
        """ Открываем окно ввода данных нового подключения """
        NewConnection(self)

    def open_filter_connection(self):
        """ Открываем окно фильтров списка подключений """
        FilterConnections(self)

    def open_logins(self):
        """ Открывааем окно со списком всех логинов выделенного подключения
        Передаем app и id первого выбранного в списке подключения """
        if self.treeview_list.focus() != '':
            id_connection = self.treeview_list.set(self.treeview_list.selection()[0], '#1')
            # чистим форму
            self.main.clear_frm_content_all()
            # открываем логины
            self.logins = logins.Logins(self.main.frm_content_all, self.main, id_connection)

            # Companies()
            # self.connection_types = connection_types.ConnectionTypes(self.parent.frm_content_all, self.parent)
        else:
            mb.showwarning('Предупреждение', 'Выберите подключение в списке')

    def color_btn_filter(self):
        """ Процедкра смены цвета кнопки Фильтр """
        if connections_filter_dict:  # если есть фильтры
            self.btn_open_filter.configure(bg='#A9A9A9')
        else:
            self.btn_open_filter.configure(bg='#f0f0f0')

    def set_connection_filter(self, id_company, id_connection_type, connection_ip, connection_description):
        """ Процедура применения фильтра
        :param id_company:
        :param id_connection_type:
        :param connection_ip:
        :param connection_description:
        :return: No
        """
        connections_filter_dict.clear()  # Чистим словарь
        # Пересоздаем словарь
        if id_company:
            connections_filter_dict['id_company'] = id_company
        if id_connection_type:
            connections_filter_dict['id_connection_type'] = id_connection_type
        if connection_ip:
            connections_filter_dict['connection_ip'] = connection_ip
        if connection_description:
            connections_filter_dict['connection_description'] = connection_description

        # self.color_btn_filter()  # цвет кнопки фильтра
        self.show_connections()  # перезегружаем список

    def clear_connection_filter(self):
        """ Процедура очистки фильтров подключений """
        connections_filter_dict.clear()  # чистим словарь
        # self.color_btn_filter()  # цвет кнопки фильтра
        self.show_connections()  # перезегружаем список


class Connection(tk.Toplevel):
    """ Базовый класс всплывающего окна подключений """
    def __init__(self, parent=None):
        super().__init__()
        self["bg"] = '#d7d8e0'

        self.parent = parent  # Main
        self.connections_db = connections_db.ConnectionsDB()  # БД подключений
        self.companies_db = companies_db.CompaniesDB()  # БД компаний
        self.connection_types_db = connection_types_db.ConnectionTypesDB()  # БД  типов подключений

        self.init_connections()

    def init_connections(self):
        # для отображения на полное окно
        # self.pack(fill=tk.BOTH, expand=True)
        # color = self.bg

        # Тема
        self.style = ttk.Style()
        self.style.theme_use("default")

        self.geometry('415x250+400+300')
        self.resizable(False, False)

        # Добавляем функции модального, прехватываем фокус до закрытия
        self.grab_set()
        self.focus_set()

        # Резировая ячейка для описания
        self.columnconfigure(1, weight=1)
        self.rowconfigure(3, weight=1)

        # 1 строка
        lbl_comps_list = ttk.Label(self, text="Компания", width=17)
        lbl_comps_list.grid(row=0, column=0, sticky='e', pady=10, padx=10)
        self.cmb_comps_list = ttk.Combobox(self, width=50, height=20)
        self.cmb_comps_list.grid(row=0, column=1, columnspan=4, sticky='we', padx=10)

        # 2 строка
        lbl_conn_types_list = ttk.Label(self, text="Тип подключения", width=17)
        lbl_conn_types_list.grid(row=1, column=0, sticky=tk.W, pady=10, padx=10)
        self.cmb_conn_types_list = ttk.Combobox(self, width=50, height=20)
        self.cmb_conn_types_list.grid(row=1, column=1, columnspan=4, sticky='we', padx=10)

        # 3 строка
        lbl_conn_name = ttk.Label(self, text="Ip-адрес/домен", width=17)
        lbl_conn_name.grid(row=2, column=0, sticky=tk.W, pady=10, padx=10)
        self.ent_conn_name = ttk.Entry(self)
        self.ent_conn_name.grid(row=2, column=1, columnspan=4, sticky='we', padx=10)
        self.ent_conn_name.bind("<Control-KeyPress>", gp.keys)

        # 4 строка
        self.lbl_conn_description = ttk.Label(self, text="Описание", width=17)
        self.lbl_conn_description.grid(row=3, column=0, sticky=tk.N, pady=10, padx=10)
        self.txt_conn_description = tk.Text(self)
        self.txt_conn_description.grid(row=3, column=1, columnspan=4, sticky='nwse', pady=10, padx=10)
        self.txt_conn_description.bind("<Control-KeyPress>", gp.keys)

        # 5 строка КНОПКИ

        # 1
        # self.btn_apply_connection_filter = ttk.Button(self, text='Применить',
        #                                              # command=self.apply_connection_filter
        #                                              )
        # self.btn_apply_connection_filter.grid(row=4, column=2, sticky=tk.W + tk.E, pady=10, padx=10)

        # 2
        # btn_clear_connection_filter = ttk.Button(self, text='Сбросить')
        # btn_clear_connection_filter.grid(row=4, column=3, sticky=tk.W + tk.E, pady=10, padx=10)

        # 3
        self.btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.grid(row=4, column=4, sticky=tk.W + tk.E, pady=10, padx=10)

    def get_comps_list(self):
        """ Процедура заполнения списка компаний """
        self.comps_list = self.companies_db.get_company_for_list()
        # first, second- первые 2 элемента, *other - все остальные элементы
        # self.cmb_comps_list['values'] = [second for first, second, *other in data]
        self.cmb_comps_list['values'] = [elem[1] for elem in self.comps_list]
        # self.cmb_comps_list.current(0)

    def get_conn_types_list(self):
        """ Процедура заполнения списка типов подключения """
        self.conn_types_list = self.connection_types_db.get_connection_type_for_list()
        # first, second- первые 2 элемента, *other - все остальные элементы
        # self.cmb_comps_list['values'] = [second for first, second, *other in data]
        self.cmb_conn_types_list['values'] = [elem[1] for elem in self.conn_types_list]
        # self.cmb_conn_types_list.current(0)

    def check_empty(self):
        """ Процедкра проверки на пустые поля
        :return: True/False
        """
        if (self.cmb_comps_list.current()) == -1:
            mb.showwarning('Предупреждение', 'Выберите компанию')
            return False
        elif (self.cmb_conn_types_list.current()) == -1:
            mb.showwarning('Предупреждение', 'Выберите тип доступа')
            return False
        elif len(self.ent_conn_name.get()) == 0:
            mb.showwarning('Предупреждение', 'Введите Ip-адрес/домен')
            return False
        return True

    def check_exists(self):
        """ Процедура проверки дублей по введенным данным
        :return: True/False
        """
        id_company = self.comps_list[self.cmb_comps_list.current()][0]
        id_connection_type = self.conn_types_list[self.cmb_conn_types_list.current()][0]
        conn_name = self.ent_conn_name.get()
        data = self.connections_db.get_connection_ip_for_check_exists(id_company, id_connection_type, conn_name)
        if data:
            mb.showwarning('Предупреждение', 'Данное подключение уже существует')
            return False
        return True


class FilterConnections(Connection):
    """ Класс формы ввода фильтров для списка подключений """
    def __init__(self, parent):  # Конструктор
        super().__init__()

        self.parent = parent  # Main

        self.init_filter_connection()
        self.get_comps_list()  # Список компаний
        self.get_conn_types_list()  # Список типов подключения
        self.get_connection_filter()

    def init_filter_connection(self):
        self.title('Фильтр подключений')

        # Блокируем "Описание"
        self.lbl_conn_description.configure(state="disabled")  # normal, readonly и disabled
        self.txt_conn_description.configure(state="disabled")  # normal, readonly и disabled

        # Кнопки
        self.btn_apply_connection_filter = ttk.Button(self, text='Применить', command=self.apply_connection_filter)
        self.btn_apply_connection_filter.grid(row=4, column=2, sticky=tk.W + tk.E, pady=10, padx=10)

        btn_clear_connection_filter = ttk.Button(self, text='Сбросить')
        btn_clear_connection_filter.grid(row=4, column=3, sticky=tk.W + tk.E, pady=10, padx=10)

        btn_clear_connection_filter.bind('<Button-1>', lambda event: self.parent.clear_connection_filter())
        btn_clear_connection_filter.bind('<Button-1>', lambda event: self.destroy(), add='+')  # Доп событие

    def get_connection_filter(self):
        """ Процедура получения текущих значений фильтра и вывод на форму """
        if connections_filter_dict:
            # Получаем текущие фильтры
            id_company = connections_filter_dict.get('id_company', '')
            id_connection_type = connections_filter_dict.get('id_connection_type', '')
            connection_ip = connections_filter_dict.get('connection_ip', '')
            connection_description = connections_filter_dict.get('connection_description', '')

            # Компания по фильтру
            if id_company:
                index_company = 0
                for items in self.comps_list:
                    if items[0] == id_company:
                        break
                    index_company += 1
                self.cmb_comps_list.current(index_company)

            # Тип подключения по фильтру
            if id_connection_type:
                index_connection_type = 0
                for items in self.conn_types_list:
                    if items[0] == id_connection_type:
                        break
                    index_connection_type += 1
                self.cmb_conn_types_list.current(index_connection_type)

            if connection_ip:
                self.ent_conn_name.insert(0, connection_ip)
            if connection_description:
                self.txt_conn_description.insert(1.0, connection_description)

        # в идеале описание преопределить на однострочное поле

    def apply_connection_filter(self):
        """ Процедура применения фильтров """
        # получаем компанию с формы
        if (self.cmb_comps_list.current()) == -1:
            id_company = ''
        else:
            id_company = self.comps_list[self.cmb_comps_list.current()][0]
        # получаем тип подключения с формы
        if (self.cmb_conn_types_list.current()) == -1:
            id_connection_type = ''
        else:
            id_connection_type = self.conn_types_list[self.cmb_conn_types_list.current()][0]
        conn_name = self.ent_conn_name.get()
        conn_description = gp.get_text_in_one_line(self.txt_conn_description.get('1.0', tk.END))
        # сохраняем фильтр
        self.parent.set_connection_filter(id_company, id_connection_type, conn_name, conn_description)
        # имитация клика по кнопке закрыть
        self.btn_cancel.invoke()


class NewConnection(Connection):
    """ Класс формы ввода нового подключения """
    def __init__(self, parent):  # Конструктор
        super().__init__()

        self.parent = parent  # Main

        self.init_new_connection()
        self.get_comps_list()  # Список компаний
        self.get_conn_types_list()  # Список типов подключения

    def init_new_connection(self):
        self.title('Добавить подключение')

        # кнопка "Сохранить"
        self.btn_save = ttk.Button(self, text='Сохранить', command=self.save_new_connection)
        self.btn_save.grid(row=4, column=3, sticky=tk.W + tk.E, pady=10, padx=10)

    def save_new_connection(self):
        """ Процедура сохраненеия нового подключения """
        if self.check_empty() and self.check_exists():  # проверка на пустые поля и дубль
            # Данные с формы
            id_company = self.comps_list[self.cmb_comps_list.current()][0]
            id_connection_type = self.conn_types_list[self.cmb_conn_types_list.current()][0]
            conn_name = self.ent_conn_name.get()
            conn_description = gp.get_text_in_one_line(self.txt_conn_description.get('1.0', tk.END))
            # Сохраняем
            self.connections_db.insert_new_connection(id_company, id_connection_type, conn_name, conn_description)
            self.parent.show_connections()  # выводим список на форму
            # mb.showinfo("Информация", 'Данные сохранены')
            self.btn_cancel.invoke()  # имитация клика по кнопке закрыть


class UpdateConnection(Connection):
    """ Класс формы обновления подключений """
    def __init__(self, parent, id_connection):  # конструктор
        super().__init__()

        self.parent = parent  # передаем класс Main
        self.id_connection = id_connection

        self.init_update_connection()
        self.get_connection_for_update()

    def init_update_connection(self):
        self.title('Обновить подключение')
        # добавляем кнопку "Обновить"
        btn_update = ttk.Button(self, text='Обновить', command=self.update_connection)
        btn_update.grid(row=4, column=3, sticky=tk.W + tk.E, pady=10, padx=10)

    def get_connection_for_update(self):
        """ Процедура получения и вывода на форму данных выделенной строки """
        data = self.connections_db.get_connection_for_update_by_id(self.id_connection)
        # Выводим значения в поля формы
        self.cmb_comps_list['values'] = [data[1]]
        self.cmb_comps_list.current(0)
        self.cmb_comps_list.configure(state="disabled")  # normal, readonly и disabled
        self.cmb_conn_types_list['values'] = [data[2]]
        self.cmb_conn_types_list.current(0)
        self.cmb_conn_types_list.configure(state="disabled")  # normal, readonly и disabled
        self.ent_conn_name.insert(0, data[3])
        self.txt_conn_description.insert(1.0, data[4])

    def update_connection(self):
        """ Процедура обновления типа подключения """
        if self.check_empty():  # проверка на пустые поля
            # данные с формы
            # id_company = self.comps_list[self.cmb_comps_list.current()][0]  # Отключено
            # id_connection_type = self.conn_types_list[self.cmb_conn_types_list.current()][0]  # Отключено
            conn_name = self.ent_conn_name.get()
            conn_description = gp.get_text_in_one_line(self.txt_conn_description.get('1.0', tk.END))
            self.connections_db.update_connection_by_id(self.id_connection, conn_name, conn_description)  # Обновляем
            self.parent.show_connections()  # выводим список на форму
            # mb.showinfo("Информация", 'Данные сохранены')
            self.btn_cancel.invoke()  # имитация клика по кнопке закрыть
