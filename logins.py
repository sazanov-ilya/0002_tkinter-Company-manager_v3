import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb
# import tkinter.ttk as ttk
# import sqlite3

# Импортируем свои модули
import __general_procedures as gp
import connections as connections
import logins_db as logins_db  # БД для форм логинов
import connections_db as connections_db  # БД для форм подключения
import users_db as users_db
# import new_login_by_id_connection as new_login_by_id_connection
# import login as login


# Словарь фильтров
logins_filter_dict = {}


class Logins(tk.Frame):
    """ Класс формы списка логинов """
    def __init__(self, root, main, id_connection):
        super().__init__(root)

        self.root = root  # frm_content_all
        self.main = main  # Main
        self.id_connection = id_connection

        self.logins_db = logins_db.LoginsDB()  # БД логинов
        self.connections_db = connections_db.ConnectionsDB()  # БД подключений
        self.users_db = users_db.UsersDB()  # БД пользователей

        self.init_logins()
        self.show_logins_by_id_connection()
        self.show_company_name()

    def init_logins(self):
        # self.title('Список логинов')

        # резиновая ячейка с таблицей
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        # для отображения данных на форме
        self.pack(fill=tk.BOTH, expand=True)

        # # базовая рамка для модуля
        # frm_logins = ttk.Frame(self, relief=tk.RAISED, borderwidth=0)
        # frm_logins.pack(fill=tk.BOTH, expand=True)

        # рамка для toolbar
        # frm_logins_top_toolbar = ttk.Frame(frm_logins, relief=tk.RAISED, borderwidth=0)
        # frm_logins_top_toolbar.pack(fill=tk.X)
        frm_logins_top_toolbar = ttk.Frame(self, relief=tk.RAISED, borderwidth=0)
        frm_logins_top_toolbar.grid(row=0, column=0, columnspan=2, sticky='nwse')

        # Кнопки
        # 1
        btn_open_filter = tk.Button(frm_logins_top_toolbar, text='Фильтр', **self.main.btn_style,
                                    command=self.open_filter_login)
        btn_open_filter.pack(side=tk.LEFT, padx=5, pady=7)
        # 2
        btn_open_new_login = tk.Button(frm_logins_top_toolbar, text='Добавить', **self.main.btn_style,
                                       command=self.open_new_login)
        btn_open_new_login.pack(side=tk.LEFT, **self.main.btn_pack_padding)
        # 3
        btn_open_update_login = tk.Button(frm_logins_top_toolbar, text='Редактировать', **self.main.btn_style,
                                          command=self.open_update_login)
        btn_open_update_login.pack(side=tk.LEFT, **self.main.btn_pack_padding)
        # 4
        btn_open_delete_logins = tk.Button(frm_logins_top_toolbar, text='Удалить', **self.main.btn_style,
                                           command=self.delete_logins)
        btn_open_delete_logins.pack(side=tk.LEFT, **self.main.btn_pack_padding)
        # 5
        if self.users_db.get_user_is_admin_by_login(self.main.user_login):
            btn_open_permission = tk.Button(frm_logins_top_toolbar, text='Управление правами', **self.main.btn_style,
                                            command=self.open_permission)
            btn_open_permission.pack(side=tk.LEFT, **self.main.btn_pack_padding)

        # Рамка вывода названия компании и типа подключения
        frm_logins_title = ttk.Frame(self, relief=tk.RAISED, borderwidth=0)
        frm_logins_title.grid(row=1, column=0, columnspan=2, sticky='nwse')

        self.lbl_company_name = tk.Label(frm_logins_title, bg='#d7d8e0', text='Компания - > Тип подключения')
        self.lbl_company_name.pack(side=tk.LEFT, padx=5, pady=7)

        # список Treeview
        self.logins_table = ttk.Treeview(self, columns=('id_login', 'login_name', 'login_password', 'login_description'),
                                         height=10, show='headings')
        #self.logins_table = ttk.Treeview(frm_logins_content,
        #                                 columns=('id_login', 'login_name', 'login_password', 'login_description'),
        #                                 height=10, show='headings')
        # Параметры столбцов
        self.logins_table.column("id_login", width=40, anchor=tk.CENTER)
        self.logins_table.column("login_name", anchor=tk.CENTER)
        self.logins_table.column("login_password", anchor=tk.CENTER)
        self.logins_table.column("login_description", anchor=tk.CENTER)
        # Названия столбцов
        self.logins_table.heading('id_login', text='ID')
        self.logins_table.heading('login_name', text='Логин')
        self.logins_table.heading('login_password', text='Пароль')
        self.logins_table.heading('login_description', text='Описание')

        # self.logins_table.pack(fill="both", side='left', expand=True)
        self.logins_table.grid(row=2, column=0, sticky='nwse')
        # вешаем контекстное меню на ЛКМ
        self.logins_table.bind('<Button-3>', self.show_context_menu)

        # полоса прокрутки для таблицы
        scroll = tk.Scrollbar(self, command=self.logins_table.yview)
        #scroll.pack(side=tk.RIGHT, fill=tk.Y)
        scroll.grid(row=2, column=1, sticky='nwse')
        self.logins_table.configure(yscrollcommand=scroll.set)

        # рамка для нижнего toolbar
        frm_logins_bottom_toolbar = ttk.Frame(self, relief=tk.RAISED, borderwidth=0)
        frm_logins_bottom_toolbar.grid(row=3, column=0, columnspan=2, sticky='nwse')
        # Кнопки
        # 1
        self.btn_ligins_back = tk.Button(frm_logins_bottom_toolbar, text='Назад на список логинов',
                                         **self.main.btn_style,
                                         command=self.open_connections)
        self.btn_ligins_back.pack(side=tk.RIGHT, **self.main.btn_pack_padding)

        # контекстное меню для копирования
        self.context_menu = tk.Menu(self.logins_table, tearoff=0)
        self.context_menu.add_command(
            label='Копировать логин', command=self.copy_login)
        self.context_menu.add_command(
            label='Копировать пароль', command=self.copy_password)
        self.context_menu.add_command(
            label='Копировать описание', command=self.copy_description)
        # self.context_menu.add_command(
        #     label='Копировать все', command=self.copy_all)

    def show_context_menu(self, event):
        """ Процедура вывода контекстного меню
        :param event:
        :return:
        """
        if self.logins_table.focus() != '':
            self.logins_table.identify_row(event.y)
            self.context_menu.post(event.x_root, event.y_root)

    def copy_login(self):
        """ Процедура копирования в буфер обмена """
        self.root.clipboard_clear()
        self.root.clipboard_append(self.logins_table.set(self.logins_table.selection()[0], '#2'))

    def copy_password(self):
        """ Процедура копирования в буфер обмена """
        self.root.clipboard_clear()
        self.root.clipboard_append(self.logins_table.set(self.logins_table.selection()[0], '#3'))

    def copy_description(self):
        """ Процедура копирования в буфер обмена """
        self.root.clipboard_clear()
        self.root.clipboard_append(self.logins_table.set(self.logins_table.selection()[0], '#4'))

    def copy_all(self):
        """ Процедура копирования в буфер обмена """
        self.root.clipboard_clear()
        self.root.clipboard_append(self.logins_table.set(self.logins_table.selection()[0], '#2') + '\n' +
                                   self.logins_table.set(self.logins_table.selection()[0], '#3') + '\n' +
                                   self.logins_table.set(self.logins_table.selection()[0], '#4'))

    def open_filter_login(self):
        """ Открываем окно для ввода нового логина по выбранному подключению
        Передаем app и id первого выбранного в списке подключения """
        FilterLogin(self.main, self, self.id_connection)
        # self.show_logins_by_id_connection()

    def open_new_login(self):
        """ Открываем окно для ввода нового логина по выбранному подключению
        Передаем app и id первого выбранного в списке подключения """
        NewLogin(self.main, self, self.id_connection)
        self.show_logins_by_id_connection()

    def open_update_login(self):
        """ Открываем окно для обновления выбранного логина """
        if self.logins_table.focus() != '':
            id_login = self.logins_table.set(self.logins_table.selection()[0], '#1')
            UpdateLogin(self.main, self, self.id_connection, id_login)
        else:
            mb.showwarning('Предупреждение', 'Выберите логин')

    def open_permission(self):
        """ Открываем окно разрещений для выбранного логина """
        if self.logins_table.focus() != '':
            id_login = self.logins_table.set(self.logins_table.selection()[0], '#1')
            Permission(self, id_login)
        else:
            mb.showwarning('Предупреждение', 'Выберите логин')

    def open_connections(self):
        """ Возврат на окно со списком подключений """
        self.main.clear_frm_content_all()  # Чистим форму
        self.destroy()  # Убиваем текушую форму
        connections.Connections(self.main.frm_content_all, self.main)  # Вывод таблицы

    def get_filter(self):
        """ Процедура получения текущих значений фильтра """
        return logins_filter_dict

    def set_filter(self, dict):
        """ Процедура применения фильтра
        :param dict:
        :return: No
        """
        logins_filter_dict.clear()  # Чистим словарь
        logins_filter_dict.update(dict)
        self.show_logins_by_id_connection()  # Перезегружаем таблицу

    def show_company_name(self):
        """ Процедура выводв на форму названия компании и типа подклюжчения """
        data = self.connections_db.get_company_connection_type_by_id_connection(self.id_connection)
        label = (data[1]) + '  ->  ' + (data[2])
        self.lbl_company_name.config(text=label)

    def show_logins_by_id_connection(self):
        """ Процедура заполнения тиблицы логинов """
        [self.logins_table.delete(i) for i in self.logins_table.get_children()]  # Очистка таблицы

        if self.users_db.get_user_is_admin_by_login(self.main.user_login):
            data = self.logins_db.get_logins_list_by_id_connection_for_admin(self.id_connection,
                                                                             self.get_filter())
        else:
            data = self.logins_db.get_logins_list_by_id_connection_for_user(self.id_connection,
                                                                            self.main.id_user,
                                                                            self.get_filter())
        [self.logins_table.insert('', 'end', values=row) for row in data]

    def delete_logins(self):
        """ Процедура удаления выбранных типов подключения """
        if self.logins_table.focus() != '':
            answer = mb.askyesno(title='Запрос действия',
                                 message="Хотите удалить выбранные элементы?")
            if answer:  # если Да = True
                ids = []  # кортеж id выделенных элементов
                for selection_item in self.logins_table.selection():
                    ids.append(self.logins_table.set(selection_item, '#1'),)
                self.logins_db.delete_logins(ids)
                self.show_logins_by_id_connection()  # перезагружаем список
        else:
            mb.showwarning('Предупреждение', 'Выберите логин (логины)')


class Login(tk.Toplevel):
    """ Базовый класс всплывающего окна логина """
    def __init__(self, main, parent, id_connection):
        super().__init__()
        self["bg"] = '#d7d8e0'  # цвет фона формы
        self.title("Логин")

        # тема
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.geometry('415x250+400+300')
        self.resizable(False, False)

        self.main = main  # Main
        self.parent = parent  # Logins
        self.id_connection = id_connection
        self.logins_db = logins_db.LoginsDB()  # Подключаем бд логинов

        self.init_login()

    def init_login(self):
        # добавляем функции модального, прехватываем фокус до закрытия
        self.grab_set()
        self.focus_set()

        # резировая ячейка для описания
        self.columnconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        # 1 логин
        lbl_login_name = ttk.Label(self, text="Логин", width=10)
        lbl_login_name.grid(row=0, column=0, sticky='w', pady=10, padx=10)
        self.ent_login_name = ttk.Entry(self)
        self.ent_login_name.grid(row=0, column=1, columnspan=4, sticky='we', padx=10)
        self.ent_login_name.focus()
        self.ent_login_name.bind("<Control-KeyPress>", gp.keys)

        # 2 пароль
        self.lbl_login_password = ttk.Label(self, text="Пароль", width=10)
        self.lbl_login_password.grid(row=1, column=0, sticky='w', pady=10, padx=10)
        self.ent_login_password = ttk.Entry(self)
        self.ent_login_password.grid(row=1, column=1, columnspan=4, sticky='we', padx=10)
        self.ent_login_password.bind("<Control-KeyPress>", gp.keys)

        # 3 описание
        lbl_login_description = ttk.Label(self, text="Описание", width=10)
        lbl_login_description.grid(row=2, column=0, sticky='n', pady=10, padx=10)
        self.txt_login_description = tk.Text(self)
        self.txt_login_description.grid(row=2, column=1, columnspan=4, sticky='nwse', pady=10, padx=10)
        self.txt_login_description.bind("<Control-KeyPress>", gp.keys)

        # 3 Создатель
        lbl_creator = ttk.Label(self, text="Создана", width=10)
        lbl_creator.grid(row=3, column=0, sticky='n', pady=10, padx=10)
        self.ent_creator = ttk.Entry(self)
        self.ent_creator.grid(row=3, column=1, columnspan=4, sticky='we', padx=10)
        self.ent_creator.bind("<Control-KeyPress>", gp.keys)

        # 4 кнопки
        # self.btn_apply_connection_filter = ttk.Button(self, text='Применить',command=self.apply_connection_filter)
        # self.btn_apply_connection_filter.grid(row=3, column=2, sticky=tk.W + tk.E, pady=10, padx=10)

        # btn_clear_connection_filter = ttk.Button(self, text='Сбросить')
        # btn_clear_connection_filter.grid(row=3, column=3, sticky=tk.W + tk.E, pady=10, padx=10)

        self.btn_login_cancel = ttk.Button(self, text='Отмена', command=self.destroy)
        self.btn_login_cancel.grid(row=4, column=4, sticky=tk.W + tk.E, pady=10, padx=10)

    def check_empty(self):
        """ Процедура проверки на пустые поля формы
        :return: True/False
        """
        if len(self.ent_login_name.get()) == 0:
            mb.showwarning('Предупреждение', 'Введите логин')
            return False
        elif len(self.ent_login_password.get()) == 0:
            mb.showwarning('Предупреждение', 'Введите пароль')
            return False
        return True

    def check_exists(self):
        """ Процедура проверки дублей логина по введенным данным
        :return: True/False
        """
        id_connection = self.id_connection
        login_name = self.ent_login_name.get()
        data = self.logins_db.get_login_name_for_check_exists(id_connection, login_name)
        if data:
            mb.showwarning('Предупреждение', 'Дубль логина <' + data + '> для выбранного подключения')
            return False
        return True


class FilterLogin(Login):
    """ Класс формы добавления нового логина по id_connection """
    def __init__(self, main, parent, id_connection):
        super().__init__(main, parent, id_connection)
        # self.geometry("500x300+300+200")

        self.main = main  # Main
        self.parent = parent  # Logins
        self.id_connection = id_connection

        self.init_new_login()

    def init_new_login(self):
        self.title("Добавить новый логин")

        self.ent_creator.insert(0, self.main.user_login)
        self.ent_creator.configure(state="disabled")  # normal, readonly и disabled

        self.lbl_login_password.configure(state="disabled")  # normal, readonly и disabled
        self.ent_login_password.configure(state="disabled")  # normal, readonly и disabled

        # 7 Кнопки
        btn_apply_filter = ttk.Button(self, text='Применить', command=self.apply_filter)
        btn_apply_filter.grid(row=4, column=2, sticky=tk.W + tk.E, pady=10, padx=10)

        btn_clear_filter = ttk.Button(self, text='Сбросить', command=self.clear_filter)
        btn_clear_filter.grid(row=4, column=3, sticky=tk.W + tk.E, pady=10, padx=10)

    def get_filter(self):
        """ Процедура получения текущих значений фильтра и вывод на форму """
        tmp_logins_filter_dict = {}
        tmp_logins_filter_dict.update(self.parent.get_filter())

        if tmp_logins_filter_dict:
            if tmp_logins_filter_dict.get('login_name', ''):
                self.ent_login_name.insert(0, tmp_logins_filter_dict.get('login_name', ''))
            if tmp_logins_filter_dict.get('login_description', ''):
                self.txt_login_description.insert(1.0, tmp_logins_filter_dict.get('login_description', ''))

    def apply_filter(self):
        """ Процедура применения фильтров """
        tmp_logins_filter_dict = {}
        if len(self.ent_login_name.get()) > 0:
            tmp_logins_filter_dict['login_name'] = self.ent_login_name.get()
        if len(gp.get_text_in_one_line(self.txt_login_description.get('1.0', tk.END))) > 0:
            tmp_logins_filter_dict['login_description'] = \
                gp.get_text_in_one_line(self.txt_login_description.get('1.0', tk.END))

        self.parent.set_filter(tmp_logins_filter_dict)
        self.btn_login_cancel.invoke()  # Имитация клика по кнопке "Закрыть"

    def clear_filter(self):
        """ Процедура применения фильтров """
        self.parent.set_filter({})
        self.btn_login_cancel.invoke()  # Имитация клика по кнопке "Закрыть"


class NewLogin(Login):
    """ Класс формы добавления нового логина по id_connection """
    def __init__(self, main, parent, id_connection):
        super().__init__(main, parent, id_connection)
        # self.geometry("500x300+300+200")

        self.main = main  # Main
        self.parent = parent  # Logins
        self.id_connection = id_connection

        self.init_new_login()

    def init_new_login(self):
        self.title("Добавить новый логин")

        self.ent_creator.insert(0, self.main.user_login)
        self.ent_creator.configure(state="disabled")  # normal, readonly и disabled

        btn_save_login = ttk.Button(self, text='Сохранить', command=self.save_new_login)
        btn_save_login.grid(row=4, column=3, sticky=tk.W + tk.E, pady=10, padx=10)

    def save_new_login(self):
        """ Процедура сохранения нового логина
        :return: No
        """
        if self.check_empty() and self.check_exists():  # Проверка на пустые поля и дубль
            self.logins_db.save_new_login(self.id_connection,
                                          self.ent_login_name.get(),
                                          self.ent_login_password.get(),
                                          gp.get_text_in_one_line(self.txt_login_description.get('1.0', tk.END)),
                                          self.main.id_user,
                                          self.main.id_role)
            self.parent.show_logins_by_id_connection()  # Выводим списко логинов
            self.btn_login_cancel.invoke()  # Имитация клика по "Отмена"


class UpdateLogin(Login):
    """ Класс формы обновления логина по id_connection и id_login"""
    def __init__(self, main, parent, id_connection, id_login):
        super().__init__(main, parent, id_connection)

        self.main = main  # Main
        self.parent = parent  # Logins
        self.id_connection = id_connection
        self.id_login = id_login

        self.init_update_login()
        self.get_login_for_update()  # выводим данные логина

    def init_update_login(self):
        self.title("Редактировать логин")

        btn_login_update = ttk.Button(self, text='Обновить', command=self.update_login)
        btn_login_update.grid(row=4, column=3, sticky=tk.W + tk.E, pady=10, padx=10)

    def get_login_for_update(self):
        """ Процедура получения и вывода на форму данных логина по id_login """
        data = self.logins_db.get_login_by_id(self.id_login)
        # выводим значения в поля формы
        self.ent_login_name.insert(0, data[1])
        self.ent_login_password.insert(0, data[2])
        self.txt_login_description.insert(1.0, data[3])
        self.ent_creator.insert(0, data[4])
        self.ent_creator.configure(state="disabled")  # normal, readonly и disabled

    def update_login(self):
        """ Процедура сохранения нового типа подключения """
        if self.check_empty():  # проверка на пустые поля
            # данные с формы
            login_name = self.ent_login_name.get()
            login_password = self.ent_login_password.get()
            login_description = gp.get_text_in_one_line(self.txt_login_description.get('1.0', tk.END))
            self.logins_db.update_login_by_id(self.id_login, login_name, login_password, login_description)  # обновляем
            self.parent.show_logins_by_id_connection()  # выводим список на форму
            # mb.showinfo("Информация", 'Данные сохранены')
            self.btn_login_cancel.invoke()  # имитация клика по кнопке закрыть


class Permission(tk.Toplevel):
    """ Класс формы управления правами для логинов"""
    def __init__(self, parent, id_login):
        super().__init__()

        self.title("Управление правами")

        # Добавляем функции модального, прехватываем фокус до закрытия
        self.grab_set()
        self.focus_set()

        self.width = 415
        self.height = 350
        self.posx = 400
        self.posy = 300

        self["bg"] = '#d7d8e0'  # Цвет фона формы
        self.style = ttk.Style()  # Тема
        self.style.theme_use("default")
        # self.geometry('415x350+400+300')  # Высота по высоте canvas
        self.geometry("%dx%d+%d+%d" % (self.width, self.height, self.posx, self.posy))
        self.resizable(False, False)

        self.parent = parent  # Logins
        self.id_login = id_login

        self.logins_db = logins_db.LoginsDB()  # БД логинов
        self.permission_list = self.logins_db.get_permission_by_id_login(self.id_login)  # Кортеж прав логина

        self.checks = []  # Список объектов "Галочка" с ролями пользователей

        self._init_permission()
        self.show_permission()  # Вывод данных на форму

    def _init_permission(self):
        # Резировая ячейка
        # self.columnconfigure(0, weight=1)
        # self.rowconfigure(0, weight=1)

        # Общая рамка
        frm_all = ttk.Frame(self)
        frm_all.pack(fill=tk.BOTH, expand=tk.YES)
        # Резировая ячейка
        frm_all.columnconfigure(0, weight=1)
        frm_all.rowconfigure(1, weight=1)

        # ############### #
        # Верхний toolbar #
        # ############### #
        frm_top_toolbar = tk.Frame(frm_all, relief=tk.RAISED, borderwidth=1)
        frm_top_toolbar.grid(row=0, column=0, sticky="nesw")
        # Резировая ячейка для ent_filter на весь экран
        frm_top_toolbar.columnconfigure(1, weight=1)
        # Кнопка
        frm_top_toolbar.rowconfigure(0, weight=1)
        self.btn_filter = tk.Button(frm_top_toolbar, text="Применить фильтр", command=self.apply_filter)
        self.btn_filter.grid(row=0, column=0, pady=10, padx=10)
        # Текстовое поле
        self.ent_filter = ttk.Entry(frm_top_toolbar)
        self.ent_filter.grid(row=0, column=1, sticky='we', pady=10, padx=10)

        # ################ #
        # Рамка для canvas #
        # ################ #
        frm_canvas = tk.LabelFrame(frm_all)
        frm_canvas.grid(row=1, column=0, sticky="nesw")

        # Резировая ячейка
        frm_canvas.columnconfigure(0, weight=1)
        frm_canvas.rowconfigure(0, weight=1)

        self.canvas = tk.Canvas(frm_canvas)
        self.canvas.grid(row=0, column=0, sticky="nesw")
        # self.canvas.pack(fill=tk.BOTH, expand=tk.YES)

        canvas_y_scroll = ttk.Scrollbar(frm_canvas, orient="vertical", command=self.canvas.yview)
        canvas_y_scroll.grid(row=0, column=1, sticky="ns")
        self.canvas.configure(yscrollcommand=canvas_y_scroll.set)

        # Рамка для списка Checkbutton
        self.frm_permission = tk.Frame(self.canvas, relief=tk.RAISED, borderwidth=2)

        self.canvas_frame = self.canvas.create_window((0, 0), window=self.frm_permission, anchor="nw")

        self.frm_permission.bind("<Enter>", self._bound_to_mousewheel)
        self.frm_permission.bind("<Leave>", self._unbound_to_mousewheel)
        # Подключение полосы прокрутки
        self.frm_permission.bind('<Configure>', self._on_configure)
        # Изменения размеров вложенного frame
        self.canvas.bind("<Configure>", self._on_resize_canvas)

        # ############## #
        # Нижний toolbar #
        # ############## #
        frm_bottom_toolbar = tk.Frame(frm_all, relief=tk.RAISED, borderwidth=1)
        frm_bottom_toolbar.grid(row=2, column=0, sticky="nesw")
        self.btn_cancel = ttk.Button(frm_bottom_toolbar, text='Отмена', command=self.destroy)
        self.btn_cancel.pack(side=tk.RIGHT, pady=10, padx=10)
        btn_save = ttk.Button(frm_bottom_toolbar, text='Сохранить', command=self.save_permission)
        btn_save.pack(side=tk.RIGHT, pady=10, padx=10)

    def _on_resize_canvas(self, event):
        canvas_width, canvas_height = event.width - 5, event.height - 5
        # Ширина внутренней рамки по ширине canvas
        self.canvas.itemconfig(self.canvas_frame, width=canvas_width)
        # Выстора внутренней рамки по высоте canvas, если ролей недостаточно для полной высоты
        if self.frm_permission.winfo_height() < canvas_height:
            self.canvas.itemconfig(self.canvas_frame, height=canvas_height)

    def _bound_to_mousewheel(self, event):
        """ Процедура обработки события входа курсора мыши в область canvas
        :param event:
        :return: No
        """
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        """ Процедура обработки события выхода курсора мыши из области canvas
        :param event:
        :return: No
        """
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        """ Процедура прокрутки области canvas колесиком мышки
        :param event:
        :return: No
        """
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_configure(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    # def show_permission(self):
    #     """ Процедура вывода массива галочек со списком ролей
    #     :return: No
    #     """
    #     self.checks = []
    #     for check in range(10):
    #         self.checks.append(PermissionCheckButton(self.frm_permission, check))

    def show_permission(self):
        """ Процедура вывода массива галочек со списком ролей
        :return: No
        """
        self.checks = []
        for iter in range(len(self.permission_list)):
            self.checks.append(PermissionCheckButton(self.frm_permission,
                                                     iter,
                                                     self.permission_list[iter][0],
                                                     self.permission_list[iter][1],
                                                     self.permission_list[iter][2],
                                                     self.permission_list[iter][3]))

    def clear_frm_permission(self):
        """ Процедура очистки формы со вписком ролей """
        for widget in self.frm_permission.winfo_children():
            # widget.pack_forget()
            widget.destroy()

    def apply_filter(self):
        """ Процедура применения фильтрации по введенной строке
        :return: No
        """
        self.clear_frm_permission()  # Чистим форму с павами
        self.permission_list = []  # Перезаполняем словарь прав
        if len(self.ent_filter.get()) == 0:
            self.permission_list = self.logins_db.get_permission_by_id_login(self.id_login)
        else:
            self.permission_list = self.logins_db.get_permission_by_like_role_name(self.id_login,
                                                                                   self.ent_filter.get())
        self.show_permission()  # Перевыводим список ролей

    def save_permission(self):
        """ Процедура сохранения назначенных прав
        :return: No
        """
        for check in self.checks:
            if self.permission_list[check.iter][2] != check.permission.get():  # Значение изменилось
                if check.permission.get():  # На True
                    # print('Изменен элемент № ' + str(check.iter) + ' Добавдена роль ' + check.role_name)
                    self.add_permission(check.id_role)
                else:
                    # print('Изменен элемент № ' + str(check.iter) + ' Удалена роль ' + check.role_name)
                    self.delete_permission(check.id_permission)
        self.btn_cancel.invoke()  # Имитация клика по "Отмена"

    def add_permission(self, id_role):
        """ Процедура добавления прав на новую роль """
        self.logins_db.insert_permission_by_roles(self.id_login, id_role)

    def delete_permission(self, id_permission):
        """ Процедура добавления прав на новую роль """
        self.logins_db.delete_permission_by_id(id_permission)


class PermissionCheckButton:
    """ Класс объекта галочка для списка ролей """
    def __init__(self, parent, iter, id_role, role_name, permission, id_permission):
        self.permission = tk.BooleanVar()
        self.iter = iter
        self.id_role = id_role
        self.role_name = role_name
        self.id_permission = id_permission
        self.permission.set(permission)  # Устанавливаем значение
        self.cb = tk.Checkbutton(parent, text=self.role_name, variable=self.permission, onvalue=1, offvalue=0)
        self.cb.grid(row=self.iter, column=0, sticky='w', pady=3, padx=10)
        # self.cb.pack(side=tk.BOTTOM)




