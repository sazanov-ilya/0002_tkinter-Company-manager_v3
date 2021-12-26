import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb
# import hashlib
# import sqlite3

# Импортируем свои модули
import __general_procedures as gp
# import main_db_sqlite3 as db  # БД - общий
import users as users  # Формы пользователей
import roles as roles  # Формы ролей
import users_db as users_db
import companies as companies
import connection_types as connection_types
import connections as connections
import logins as logins

# словарь данных пользователя
# companies_filter_dict = {'user_login': '', 'user_name': ''}
user_auth = {}

# # закрываем на крестик
# def on_closing():
#    if mb.askokcancel("Выход из приложения", "Хотите выйти из приложения?"):
#        root.destroy()


# def compute_md5_hash(my_string):
#     m = hashlib.md5()
#     m.update(my_string.encode('utf-8'))
#     return m.hexdigest()


def authorization(*w, **kw):
    """ Процедура отображения окна авторизации в бозовом окне """
    root = tk.Tk()
    root.title("Войдите в систему")
    root.geometry('270x120+400+300')
    root.resizable(False, False)

    app = Authorization(root)
    app.pack()

    root.mainloop()


def main(user_login, user_id, role_id, *w, **kw):
    """ Процедура отображения окна приложения в бозовом окне после авторизации"""
    root = tk.Tk()
    root.title("База подключений")
    root.geometry("700x450+300+200")  # "'ширина' x 'высота'+300+200"
    # root.resizable(False, False)

    app = Main(root, user_login, user_id, role_id)
    app.pack()

    root.mainloop()


class Authorization(tk.Frame):
    """ Базовый класс всплывающего окна авторизации """
    def __init__(self, root=None, parent=None):
        super().__init__()
        self["bg"] = '#d7d8e0'  # Цвет фона формы

        # Тема оформления
        self.style = ttk.Style()
        self.style.theme_use("default")

        self.root = root  # Класс Main
        self.parent = parent  # Класс Logins
        self.roles_db = users_db.RolesDB()  # БД ролей
        self.users_db = users_db.UsersDB()  # БД пользователей

        self.init_auth()  # Строим окно

    def init_auth(self):
        # Добавляем функции модального, прехватываем фокус до закрытия
        self.grab_set()
        self.focus_set()

        lbl_padding = {'sticky': 'w', 'padx': 10, 'pady': 10}
        ent_padding = {'sticky': 'we', 'padx': 10}

        # Таблица на 3 колонки
        # 1 - ячейка для метки для подписи, текстовой поле на 2 ячейки
        # 2-3 - ячейки для кнопок в последней строке

        # # резировая ячейка для описания
        # self.columnconfigure(1, weight=1)
        # self.rowconfigure(5, weight=1)

        # 1 Логин
        lbl_login = ttk.Label(self, text="Логин", width=7)
        lbl_login.grid(row=0, column=0, **lbl_padding)
        self.ent_login = ttk.Entry(self)
        self.ent_login.grid(row=0, column=1, columnspan=2, **ent_padding)
        self.ent_login.focus()
        self.ent_login.bind("<Control-KeyPress>", gp.keys)

        # 2 Пароль
        lbl_password = ttk.Label(self, text="Пароль", width=7)
        lbl_password.grid(row=1, column=0, **lbl_padding)
        self.ent_password = ttk.Entry(self, show='*')
        self.ent_password.grid(row=1, column=1, columnspan=2, **ent_padding)
        self.ent_password.bind("<Control-KeyPress>", gp.keys)

        # 3 Кнопки
        btn_auth_login = ttk.Button(self, text='Войти', command=self.auth_user)
        btn_auth_login.grid(row=2, column=1, sticky=tk.W + tk.E, pady=10, padx=10)

        self.btn_cancel = ttk.Button(self, text='Отмена', command=self.root.destroy)
        self.btn_cancel.grid(row=2, column=2, sticky=tk.W + tk.E, pady=10, padx=10)

    def check_empty(self):
        """ Процедура проверки на пустые поля формы
        :return: True/False
        """
        if len(self.ent_login.get()) == 0:
            mb.showwarning('Предупреждение', 'Введите логин')
            return False
        elif len(self.ent_password.get()) == 0:
            mb.showwarning('Предупреждение', 'Введите пароль')
            return False
        return True

    def check_exists(self):
        """ Процедура проверки существования логина
        :return: True/False
        """
        data = self.users_db.get_user_login_for_check_auth(self.ent_login.get())
        if data is None:
            mb.showwarning('Предупреждение', 'Логин не найден')
            return False
        return True

    def check_pass(self):
        """ Процедура проверки пароля
        :return: True/False
        """
        data = self.users_db.get_password_by_login(self.ent_login.get())
        if gp.compute_md5_hash(self.ent_password.get()) != data:
            mb.showwarning('Предупреждение', 'Пароль не верный')
            return False
        return True

    def auth_user(self):
        """ Процедура авторизаци пользователя """
        if self.check_empty() and self.check_exists() and self.check_pass():  # Проверка
            user_login = self.ent_login.get()
            id_user = self.users_db.get_id_user_by_login(self.ent_login.get())
            id_role = self.roles_db.get_role_id_by_name(self.ent_login.get())

            self.btn_cancel.invoke()  # Имитация клика по "Отмена"

            main(user_login, id_user, id_role)  # Открываем главное окно


class Main(tk.Frame):
    """ Класс основной формы """
    def __init__(self, root, user_login=None, id_user=None, id_role=None):
        super().__init__(root)
        # Стили
        self.style = ttk.Style()
        self.style.theme_use("default")

        # Общие настройки
        # bg = '#d7d8e0', bd = 0, compound = tk.BOTTOM, relief = tk.GROOVE, borderwidth = 5, pady = 2, padx = 2,
        # self.btn_style = {'bg': '#d7d8e0', 'compound': tk.BOTTOM, 'relief': tk.GROOVE}
        self.btn_style = {'borderwidth': 3, 'pady': 2, 'padx': 2}
        self.btn_pack_padding = {'pady': 7, 'padx': 5}

        # Данные пользователя
        self.user_login = user_login
        self.id_user = id_user
        self.id_role = id_role  # id связанной роли

        self.root = root  # Main
        # self.db = db  # Передаем класс DB
        self.users_db = users_db.UsersDB()  # Подключаем пользователей

        self.init_main()  # Создаем форму
        self.clear_frm_content_all()  # Чистим блок с контентом

    def init_main(self):
        # главная рамка
        # поле для ввода данных растянуто горизонтально с параметрами fill и expand
        self.pack(fill=tk.BOTH, expand=True)

        # рамка для toolbar главного окна
        frm_main_toolbar = ttk.Frame(self, relief=tk.RAISED, borderwidth=3)  # GROOVE
        frm_main_toolbar.pack(fill=tk.X)

        # Кнопки меню с картинками
        if self.users_db.get_user_is_admin_by_login(self.user_login):
            # 1
            self.users_img = tk.PhotoImage(file='img/users.gif')
            self.btn_open_users = tk.Button(frm_main_toolbar, text='Пользователи', width=120, bg='#d7d8e0',
                                        bd=1, pady=1, padx=6, compound=tk.BOTTOM, image=self.users_img,
                                        command=self.open_users
                                        )
            self.btn_open_users.pack(side=tk.LEFT)
            # 2
            self.roles_img = tk.PhotoImage(file='img/users.gif')
            self.btn_open_roles = tk.Button(frm_main_toolbar, text='Роли', width=120, bg='#d7d8e0',
                                            bd=1, pady=1, padx=6, compound=tk.BOTTOM, image=self.roles_img,
                                            command=self.open_roles
                                            )
            self.btn_open_roles.pack(side=tk.LEFT)

        # 3
        self.companies_img = tk.PhotoImage(file='img/companies.gif')
        self.btn_open_companies = tk.Button(frm_main_toolbar, text='Компании', width=120, bg='#d7d8e0',
                                            bd=1, pady=1, padx=6, compound=tk.BOTTOM, image=self.companies_img,
                                            command=self.open_companies)
        self.btn_open_companies.pack(side=tk.LEFT)
        # 4
        self.connection_types_img = tk.PhotoImage(file='img/connection_types.gif')
        self.btn_open_connection_types = tk.Button(frm_main_toolbar, text='Типы доступов', width=120, bg='#d7d8e0',
                                                   bd=1, pady=1, padx=6, compound=tk.BOTTOM,
                                                   image=self.connection_types_img,
                                                   command=self.open_connection_types)
        self.btn_open_connection_types.pack(side=tk.LEFT)
        # 5
        self.connections_img = tk.PhotoImage(file='img/connections.gif')
        self.btn_open_connections = tk.Button(frm_main_toolbar, text='Доступы', width=120, bg='#d7d8e0',
                                              bd=1, pady=1, padx=6, compound=tk.BOTTOM, image=self.connections_img,
                                              command=self.open_connections)
        self.btn_open_connections.pack(side=tk.LEFT)

        # рамка контента главного окна
        self.frm_content_all = ttk.Frame(self, relief=tk.RAISED, borderwidth=3)
        self.frm_content_all.pack(fill=tk.BOTH, anchor=tk.N, expand=True)

    # # работает 1
    # def content_all_clear(self):
    #    self.frm_content_all.pack_forget()

    # работает 2
    def clear_frm_content_all(self):
        for widget in self.frm_content_all.winfo_children():
            # widget.pack_forget()
            widget.destroy()

    # def open_logins(self):
    #     # self.pack(fill=tk.BOTH, expand=True)
    #     self.clear_frm_content_all()
    #     id_connection = 4
    #     self.logins = logins.Logins(self.frm_content_all, app, id_connection)

    def open_users(self):
        # self.pack(fill=tk.BOTH, expand=True)
        # меняем цвета кнопок
        if self.users_db.get_user_is_admin_by_login(self.user_login):
            self.btn_open_users.configure(bg='#A9A9A9')
            self.btn_open_roles.configure(bg='#d7d8e0')
        self.btn_open_companies.configure(bg='#d7d8e0')
        self.btn_open_connection_types.configure(bg='#d7d8e0')
        self.btn_open_connections.configure(bg='#d7d8e0')

        self.clear_frm_content_all()
        # self.users = users.Users(self.frm_content_all, self.root)
        users.Users(self.frm_content_all, self)

    def open_roles(self):
        # self.pack(fill=tk.BOTH, expand=True)
        # меняем цвета кнопок
        if self.users_db.get_user_is_admin_by_login(self.user_login):
            self.btn_open_roles.configure(bg='#A9A9A9')
            self.btn_open_users.configure(bg='#d7d8e0')
        self.btn_open_companies.configure(bg='#d7d8e0')
        self.btn_open_connection_types.configure(bg='#d7d8e0')
        self.btn_open_connections.configure(bg='#d7d8e0')

        self.clear_frm_content_all()
        # self.roles = users.Roles(self.frm_content_all, self.root)
        roles.Roles(self.frm_content_all, self)

    def open_companies(self):
        # self.pack(fill=tk.BOTH, expand=True)
        # меняем цвета кнопок
        self.btn_open_companies.configure(bg='#A9A9A9')
        if self.users_db.get_user_is_admin_by_login(self.user_login):
            self.btn_open_users.configure(bg='#d7d8e0')
            self.btn_open_roles.configure(bg='#d7d8e0')
        self.btn_open_connection_types.configure(bg='#d7d8e0')
        self.btn_open_connections.configure(bg='#d7d8e0')

        self.clear_frm_content_all()
        self.companies = companies.Companies(self.frm_content_all, self)

    def open_connection_types(self):
        # self.pack(fill=tk.BOTH, expand=True)
        # меняем цвета кнопок
        self.btn_open_connection_types.configure(bg='#A9A9A9')
        if self.users_db.get_user_is_admin_by_login(self.user_login):
            self.btn_open_users.configure(bg='#d7d8e0')
            self.btn_open_roles.configure(bg='#d7d8e0')
        self.btn_open_companies.configure(bg='#d7d8e0')
        self.btn_open_connections.configure(bg='#d7d8e0')

        self.clear_frm_content_all()
        self.connection_types = connection_types.ConnectionTypes(self.frm_content_all, self)

    def open_connections(self):
        # self.pack(fill=tk.BOTH, expand=True)
        # меняем цвета кнопок
        self.btn_open_connections.configure(bg='#A9A9A9')
        if self.users_db.get_user_is_admin_by_login(self.user_login):
            self.btn_open_users.configure(bg='#d7d8e0')
            self.btn_open_roles.configure(bg='#d7d8e0')
        self.btn_open_connection_types.configure(bg='#d7d8e0')
        self.btn_open_companies.configure(bg='#d7d8e0')

        self.clear_frm_content_all()
        # self.connections = connections.Connections(self.frm_content_all, self)
        connections.Connections(self.frm_content_all, self)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    authorization()

    # root = tk.Tk()
    #
    # # # закрываем на крестик
    # # root.protocol("WM_DELETE_WINDOW", on_closing)  # клик по крестику
    #
    # db = db.DB()  # Добавляем класс DB
    # app = Main(root)  # добавляем класс Main
    # # app = users.Authorization(root)
    #
    # app.pack()
    # root.title("База подключений")
    # root.geometry("700x450+300+200")
    # # root.resizable(False, False)
    #
    # # отключил 20210807 (не помню для чего)
    # #root.event_add('<<Paste>>', '<Control-igrave>')
    # #root.event_add("<<Copy>>", "<Control-ntilde>")
    #
    # root.mainloop()
