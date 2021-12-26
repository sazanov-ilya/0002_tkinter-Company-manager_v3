import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb
# import hashlib


# Импортируем свои модули
import __general_procedures as gp
import users_db as users_db  # БД для форм пользователей
import user_roles as user_roles  # Формы для Списка ролей пользователя

# def compute_md5_hash(my_string):
#     m = hashlib.md5()
#     m.update(my_string.encode('utf-8'))
#     return m.hexdigest()


# Словарь фильтров
users_filter_dict = {}


class Users(tk.Frame):
    """ Базовый класс формы логинов """
    def __init__(self, root, main):
        super().__init__(root)

        self.root = root  # frm_content_all
        self.main = main  # Main

        self.users_db = users_db.UsersDB()  # БД пользователей

        self.init_users()
        self.show_users()

    def init_users(self):
        # self.title('Список логинов')

        # резиновая ячейка с таблицей
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # для отображения данных на форме
        self.pack(fill=tk.BOTH, expand=True)

        # рамка для toolbar
        frm_users_top_toolbar = ttk.Frame(self, relief=tk.RAISED, borderwidth=0)
        frm_users_top_toolbar.grid(row=0, column=0, columnspan=2, sticky='nwse')

        # Кнопки
        # 1
        self.btn_open_filter = tk.Button(frm_users_top_toolbar, text='Фильтр', **self.main.btn_style,
                                         command=self.open_filter_user)
        self.btn_open_filter.pack(side=tk.LEFT, **self.main.btn_pack_padding)
        # 2
        btn_open_new = tk.Button(frm_users_top_toolbar, text='Добавить', **self.main.btn_style,
                                 command=self.open_new_user)
        btn_open_new.pack(side=tk.LEFT, **self.main.btn_pack_padding)
        # 3
        btn_open_update = tk.Button(frm_users_top_toolbar, text='Редактировать', **self.main.btn_style,
                                    command=self.open_update_users)
        btn_open_update.pack(side=tk.LEFT, **self.main.btn_pack_padding)
        # 4
        btn_delete = tk.Button(frm_users_top_toolbar, text='Удалить', **self.main.btn_style,
                               command=self.delete_users)
        btn_delete.pack(side=tk.LEFT, **self.main.btn_pack_padding)
        # 5
        btn_open_roles = tk.Button(frm_users_top_toolbar, text='Управление ролями', **self.main.btn_style,
                                   command=self.open_user_roles)
        btn_open_roles.pack(side=tk.LEFT, **self.main.btn_pack_padding)
        # # 6
        # btn_open_auth_users = tk.Button(frm_users_top_toolbar, text='Авторизация',
        #                                   bg='#d7d8e0', bd=0, compound=tk.BOTTOM, relief=tk.GROOVE,
        #                                   borderwidth=5, pady=2, padx=2,
        #                                   command=self.open_auth_user
        #                                   )
        # btn_open_auth_users.pack(side=tk.LEFT, padx=5, pady=7)

        # # рамка вывода названия компании и типа подключения
        # frm_logins_title = ttk.Frame(self, relief=tk.RAISED, borderwidth=0)
        # frm_logins_title.grid(row=1, column=0, columnspan=2, sticky='nwse')
        #
        # self.lbl_company_name = tk.Label(frm_logins_title, bg='#d7d8e0', text='Компания - > Тип подключения')
        # self.lbl_company_name.pack(side=tk.LEFT, padx=5, pady=7)

        # Список Treeview
        self.users_table = ttk.Treeview(self, columns=('id_user',
                                                       'user_login',
                                                       'user_role',
                                                       'user_name',
                                                       'user_description',
                                                       'is_deleted'),
                                        height=10, show='headings')
        # Параметры столбцов
        self.users_table.column("id_user", width=50, anchor=tk.CENTER)
        self.users_table.column("user_login", width=100, anchor=tk.W)
        self.users_table.column("user_role", width=70, anchor=tk.W)
        self.users_table.column("user_name", width=150, anchor=tk.W)
        self.users_table.column("user_description", width=250, anchor=tk.W)
        self.users_table.column("is_deleted", width=40, anchor=tk.CENTER)
        # названия столбцов
        self.users_table.heading('id_user', text='ID')
        self.users_table.heading('user_login', text='Логин')
        self.users_table.heading('user_role', text='Роль')
        self.users_table.heading('user_name', text='ФИО')
        self.users_table.heading('user_description', text='Описание')
        self.users_table.heading('is_deleted', text='del')

        self.users_table.grid(row=1, column=0, sticky='nwse')

        # Вешаем контекстное меню на ЛКМ
        self.users_table.bind('<Button-3>', self.show_context_menu)

        # полоса прокрутки для таблицы
        scroll = tk.Scrollbar(self, command=self.users_table.yview)
        # scroll.pack(side=tk.RIGHT, fill=tk.Y)
        scroll.grid(row=1, column=1, sticky='nwse')
        self.users_table.configure(yscrollcommand=scroll.set)

        # # рамка для нижнего toolbar
        # frm_logins_bottom_toolbar = ttk.Frame(self, relief=tk.RAISED, borderwidth=0)
        # frm_logins_bottom_toolbar.grid(row=3, column=0, columnspan=2, sticky='nwse')
        # # Кнопки
        # # 1
        # self.btn_ligins_back = tk.Button(frm_logins_bottom_toolbar, text='Назад', bg='#d7d8e0', bd=0,
        #                                  compound=tk.BOTTOM, relief=tk.GROOVE, borderwidth=5, pady=2, padx=10,
        #                                  command=self.open_connections)
        # self.btn_ligins_back.pack(side=tk.RIGHT, padx=17, pady=10)

        # контекстное меню для копирования
        self.context_menu = tk.Menu(self.users_table, tearoff=0)
        self.context_menu.add_command(
            label='Копировать логин', command=self.copy_login)
        self.context_menu.add_command(
            label='Копировать роли', command=self.copy_roles)
        self.context_menu.add_command(
            label='Копировать ФИО', command=self.copy_fio)
        self.context_menu.add_command(
            label='Копировать описание', command=self.copy_description)
        # self.context_menu.add_command(
        #     label='Копировать все', command=self.copy_all)

    def show_context_menu(self, event):
        """ Процедура вывода контекстного меню
        :param event:
        :return:
        """
        if self.users_table.focus() != '':
            self.users_table.identify_row(event.y)
            self.context_menu.post(event.x_root, event.y_root)

    def copy_login(self):
        """ Процедура копирования в буфер обмена логина """
        self.root.clipboard_clear()
        self.root.clipboard_append(self.users_table.set(self.users_table.selection()[0], '#2'))

    def copy_roles(self):
        """ Процедура копирования в буфер обмена ролей """
        self.root.clipboard_clear()
        self.root.clipboard_append(self.users_table.set(self.users_table.selection()[0], '#3'))

    def copy_fio(self):
        """ Процедура копирования в буфер обмена ФИО"""
        self.root.clipboard_clear()
        self.root.clipboard_append(self.users_table.set(self.users_table.selection()[0], '#4'))

    def copy_description(self):
        """ Процедура копирования в буфер обмена"""
        self.root.clipboard_clear()
        self.root.clipboard_append(self.users_table.set(self.users_table.selection()[0], '#5'))

    def copy_all(self):
        """ Процедура копирования в буфер обмена логина """
        self.root.clipboard_clear()
        self.root.clipboard_append(self.users_table.set(self.users_table.selection()[0], '#2') + '\n' +
                                   self.users_table.set(self.users_table.selection()[0], '#3') + '\n' +
                                   self.users_table.set(self.users_table.selection()[0], '#4') + '\n' +
                                   self.users_table.set(self.users_table.selection()[0], '#5'))

    def color_btn_filter(self):
        """ Процедура смены цвета кнопки Фильтр """
        if users_filter_dict:  # Если есть фильтры
            self.btn_open_filter.configure(bg='#A9A9A9')
        else:
            self.btn_open_filter.configure(bg='#f0f0f0')

    def open_filter_user(self):
        """ Открываем окно фильтров """
        FilterUser(self.main, self)

    def open_new_user(self):
        """ Открываем окно для ввода нового логина по выбранному подключению
        Передаем app и id первого выбранного в списке подключения """
        NewUser(self.main, self)

    def open_update_users(self):
        """ Открываем окно для обновления выбранного пользователя """
        if self.users_table.focus() != '':
            # Запрет на редактирование базового админа
            if not users_db.get_user_is_base_admin(self.users_table.set(self.users_table.selection()[0], '#2')):
                id_user = self.users_table.set(self.users_table.selection()[0], '#1')
                UpdateUser(self.main, self, id_user)
            else:
                mb.showwarning('Предупреждение', 'Редактирование базового администратора запрещено')
        else:
            mb.showwarning('Предупреждение', 'Выберите пользователя в списке')

    def open_user_roles(self):
        """ Открывааем окно со списком всех логинов выделенного подключения
        Передаем app и id первого выбранного в списке подключения """
        if self.users_table.focus() != '':
            # Запрет на редактирование базового админа
            # if not users_db.get_user_is_base_admin(self.users_db.get_user_login_by_id(
            #         self.users_table.set(self.users_table.selection()[0], '#1'))):
            if not users_db.get_user_is_base_admin(self.users_table.set(self.users_table.selection()[0], '#2')):
                id_user = self.users_table.set(self.users_table.selection()[0], '#1')
                # self.main.clear_frm_content_all()  # Чистим форму
                # user_roles.UserRoles(self.main.frm_content_all, self.main, id_user)  # Открываем роли
                UserRoles(self.main, self, id_user)
            else:
                mb.showwarning('Предупреждение', 'Редактирование базового администратора запрещено')
        else:
            mb.showwarning('Предупреждение', 'Выберите пользователя в списке')

    def get_filter(self):
        """ Процедура получения текущих значений фильтра """
        return users_filter_dict

    def set_filter(self, tmp_users_filter_dict):
        """ Процедура применения фильтра
        :param tmp_users_filter_dict:
        :return: No
        """
        users_filter_dict.clear()  # Чистим словарь
        users_filter_dict.update(tmp_users_filter_dict)
        self.show_users()  # Перезегружаем список

    def show_users(self):
        """ Процедура перезаполнения списка пользователей согласно фильтров """
        self.color_btn_filter()  # Цвет кнопки фильтра

        [self.users_table.delete(i) for i in self.users_table.get_children()]  # Чистим таблицу

        data = self.users_db.get_users_by_filter(users_filter_dict)
        [self.users_table.insert('', 'end', values=row) for row in data]  # Выводим список на форму

    def delete_users(self):
        """ Процедура удаления выбранных пользователей """
        if self.users_table.focus() != '':
            answer = mb.askyesno(title='Запрос действия',
                                 message="Хотите удалить выбранные элементы?")
            if answer:  # если Да = True
                ids = []  # кортеж id выделенных элементов
                for selection_item in self.users_table.selection():
                    ids.append(self.users_table.set(selection_item, '#1'),)
                self.users_db.delete_users(ids)
                self.show_users()  # Перезагружаем список
        else:
            mb.showwarning('Предупреждение', 'Выберите пользователя/пользователей')


class User(tk.Toplevel):
    """ Базовый класс формы пользователя """
    def __init__(self, main, parent):
        super().__init__()
        self["bg"] = '#d7d8e0'  # Цвет фона формы

        self.title("Пользователь")
        # тема
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.geometry('415x320+400+300')
        self.resizable(False, False)

        self.main = main  # Main
        self.parent = parent  # Users

        # Классы-переменные - для связки значений виджетов
        self.is_deleted = tk.BooleanVar()
        self.is_admin = tk.BooleanVar()

        self.users_db = users_db.UsersDB()  # БД Пользователей

        # self.roles_db = users_db.RolesDB()  # Роли
        # self.role_list = self.roles_db.get_role_list_all()  # Кортеж (id, name) списка ролей
        # self.show_role_list()  # Заполняем список ролей

        self.init_user()  # Строим форму

    def init_user(self):
        # Добавляем функции модального, прехватываем фокус до закрытия
        self.grab_set()
        self.focus_set()

        lbl_padding = {'sticky': 'w', 'padx': 10, 'pady': 10}
        ent_padding = {'sticky': 'we', 'padx': 10}

        # Резировая ячейка для описания
        self.columnconfigure(1, weight=1)
        self.rowconfigure(5, weight=1)

        # 1 Логин
        lbl_login = ttk.Label(self, text="Логин", width=10)
        lbl_login.grid(row=0, column=0, **lbl_padding)
        self.ent_login = ttk.Entry(self)
        self.ent_login.grid(row=0, column=1, columnspan=4, **ent_padding)
        self.ent_login.focus()
        self.ent_login.bind("<Control-KeyPress>", gp.keys)

        # 2 Пароль
        self.lbl_password = ttk.Label(self, text="Пароль", width=10)
        self.lbl_password.grid(row=1, column=0, **lbl_padding)
        self.ent_password = ttk.Entry(self)
        self.ent_password.grid(row=1, column=1, columnspan=4, **ent_padding)
        self.ent_password.bind("<Control-KeyPress>", gp.keys)

        # 3 Подтверждение пароля
        self.ent_password2 = ttk.Entry(self)

        # # 4 Роль админ
        # self.check_is_admin = ttk.Checkbutton(self, text='Пользователь является администратором',
        #                                       variable=self.is_admin)
        # self.check_is_admin.grid(row=3, column=1, columnspan=4, sticky='nwse', pady=10, padx=10)

        # 5 Имя
        lbl_name = ttk.Label(self, text="Имя", width=10)
        lbl_name.grid(row=4, column=0, **lbl_padding)
        self.ent_name = ttk.Entry(self)
        self.ent_name.grid(row=4, column=1, columnspan=4, **ent_padding)
        self.ent_name.bind("<Control-KeyPress>", gp.keys)

        # 6 Описание
        lbl_description = ttk.Label(self, text="Описание", width=10)
        lbl_description.grid(row=5, column=0, sticky='n', pady=10, padx=10)
        self.txt_description = tk.Text(self)
        self.txt_description.grid(row=5, column=1, columnspan=4, sticky='nwse', pady=10, padx=10)
        self.txt_description.bind("<Control-KeyPress>", gp.keys)

        # # Полоса прокрутки
        # scroll = tk.Scrollbar(self, command=self.txt_login_description.yview)
        # # scroll.pack(side=tk.RIGHT, fill=tk.Y)
        # scroll.grid(row=5, column=5)
        # self.txt_login_description.configure(yscrollcommand=scroll.set)

        # 4 Пользователь является администратором
        self.check_is_admin = ttk.Checkbutton(self, text='Пользователь является администратором',
                                              variable=self.is_admin)
        self.check_is_admin.grid(row=6, column=1, columnspan=4, sticky='nwse', pady=10, padx=10)

        # 7 Признак "Удален"
        # lbl_is_deleted = ttk.Label(self, text="Удален", width=10)
        # lbl_is_deleted.grid(row=6, column=0, sticky='n', pady=10, padx=10)
        self.check_is_deleted = ttk.Checkbutton(self, text='Признак "удален"', variable=self.is_deleted)
        # self.check_is_deleted.invoke()
        self.check_is_deleted.grid(row=7, column=1, columnspan=4, sticky='nwse', pady=10, padx=10)

        # 4 кнопки
        # self.btn_apply_connection_filter = ttk.Button(self, text='Применить',command=self.apply_connection_filter)
        # self.btn_apply_connection_filter.grid(row=3, column=2, sticky=tk.W + tk.E, pady=10, padx=10)

        # btn_clear_connection_filter = ttk.Button(self, text='Сбросить')
        # btn_clear_connection_filter.grid(row=3, column=3, sticky=tk.W + tk.E, pady=10, padx=10)

        # 7 Кнопки
        self.btn_cancel = ttk.Button(self, text='Отмена', command=self.destroy)
        self.btn_cancel.grid(row=8, column=4, sticky=tk.W + tk.E, pady=10, padx=10)

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
        # elif (self.cmb_role.current()) == -1:
        #     mb.showwarning('Предупреждение', 'Выберите роль')
        #     return False
        elif len(self.ent_name.get()) == 0:
            mb.showwarning('Предупреждение', 'Введите имя')
            return False
        return True

    def check_exists(self):
        """ Процедура проверки дублей логина по введенным данным
        :return: True/False
        """
        data = self.users_db.get_user_login_for_check_exists(self.ent_login.get())
        if data:
            mb.showwarning('Предупреждение', 'Логин <' + data + '> уже используется')
            return False
        return True


class FilterUser(User):
    """ Класс формы добавления нового пользователя """
    def __init__(self, main, parent):
        super().__init__(main, parent)
        # self.geometry("500x300+300+200")

        self.main = main  # Main
        self.parent = parent  # Users

        self.init_filter_user()
        self.get_filter()

    def init_filter_user(self):
        self.title("Фильтр списка пользователей")

        # Блокируем
        self.lbl_password.configure(state="disabled")  # normal, readonly и disabled
        self.ent_password.configure(state="disabled")  # normal, readonly и disabled
        self.check_is_admin.configure(state="disabled")  # normal, readonly и disabled
        self.check_is_deleted.configure(state="disabled")  # normal, readonly и disabled

        # 7 Кнопки
        btn_apply_filter = ttk.Button(self, text='Применить', command=self.apply_filter)
        btn_apply_filter.grid(row=8, column=2, sticky=tk.W + tk.E, pady=10, padx=10)

        btn_clear_filter = ttk.Button(self, text='Сбросить', command=self.clear_filter)
        btn_clear_filter.grid(row=8, column=3, sticky=tk.W + tk.E, pady=10, padx=10)

    def get_filter(self):
        """ Процедура получения текущих значений фильтра и вывод на форму """
        tmp_users_filter_dict = {}
        tmp_users_filter_dict.update(self.parent.get_filter())

        if tmp_users_filter_dict:
            if tmp_users_filter_dict.get('user_login', ''):
                self.ent_login.insert(0, tmp_users_filter_dict.get('user_login', ''))
            if tmp_users_filter_dict.get('user_name', ''):
                self.ent_name.insert(0, tmp_users_filter_dict.get('user_name', ''))
            if tmp_users_filter_dict.get('user_description', ''):
                self.txt_description.insert(1.0, tmp_users_filter_dict.get('user_description', ''))

    def apply_filter(self):
        """ Процедура применения фильтров """
        tmp_users_filter_dict = {}
        if len(self.ent_login.get()) > 0:
            tmp_users_filter_dict['user_login'] = self.ent_login.get()
        if len(self.ent_name.get()) > 0:
            tmp_users_filter_dict['user_name'] = self.ent_name.get()
        if len(gp.get_text_in_one_line(self.txt_description.get('1.0', tk.END))) > 0:
            tmp_users_filter_dict['user_description'] = gp.get_text_in_one_line(self.txt_description.get('1.0', tk.END))

        self.parent.set_filter(tmp_users_filter_dict)
        self.btn_cancel.invoke()  # Имитация клика по кнопке "Закрыть"

    def clear_filter(self):
        """ Процедура применения фильтров """
        self.parent.set_filter({})
        self.btn_cancel.invoke()  # Имитация клика по кнопке "Закрыть"


class NewUser(User):
    """ Класс формы добавления нового пользователя """
    def __init__(self, main, parent):
        super().__init__(main, parent)
        # self.geometry("500x300+300+200")

        self.main = main  # Main
        self.parent = parent  # Users

        self.init_new_user()
        # self.show_role_list()  # Заполняем список ролей

    def init_new_user(self):
        self.title("Добавить нового пользователя")

        # Блокируем список ролей и галочку
        # self.cmb_role.configure(state="disabled")  # normal, readonly и disabled
        self.check_is_deleted.configure(state="disabled")  # normal, readonly и disabled

        # 7 Кнопки
        btn_save = ttk.Button(self, text='Сохранить', command=self.save_new_user)
        btn_save.grid(row=8, column=3, sticky=tk.W + tk.E, pady=10, padx=10)

    def save_new_user(self):
        """ Процедура сохранения нового логина """
        if self.check_empty() and self.check_exists():  # Проверка на пустые поля и дубль
            self.users_db.save_new_user(self.ent_login.get(),
                                        self.ent_password.get(),
                                        self.ent_name.get(),
                                        self.txt_description.get('1.0', tk.END),
                                        self.is_admin.get())
            self.parent.show_users()  # Выводим список пользователей
            self.btn_cancel.invoke()  # Имитация клика по "Отмена"


class UpdateUser(User):
    """ Класс формы обновления пользователя """
    def __init__(self, main, parent, id_user):
        super().__init__(main, parent)
        # self.geometry("500x300+300+200")

        self.main = main  # Main
        self.parent = parent  # Users
        self.id_user = id_user

        self.init_update_user()  # Строим форму
        self.get_user_for_update()  # Выводим на форму данные
        # self.show_role_list_for_update(self.id_user)  # Заполняем список ролей

    def init_update_user(self):
        self.title("Обновить пользователя")

        # 7 Кнопки
        btn_save = ttk.Button(self, text='Обновить', command=self.update_user)
        btn_save.grid(row=8, column=3, sticky=tk.W + tk.E, pady=10, padx=10)

    def get_user_for_update(self):
        """ Процедура получения и вывода на форму данных логина по id_login """
        user_data = self.users_db.get_user_by_id(self.id_user)  # Получает данные пользователя
        # Выводим значения в поля формы
        self.ent_login.insert(0, user_data[1])
        self.ent_password.insert(0, '*')
        self.ent_name.insert(0, user_data[3])
        self.txt_description.insert(1.0, user_data[4])
        self.is_admin.set(self.users_db.get_user_is_admin_by_login(user_data[1]))  # Галочка is_admin
        self.is_deleted.set(user_data[5])  # Галочка is_deleted

    def update_user(self):
        """ Процедура сохранения нового типа подключения """
        if self.check_empty():  # Проверка на пустые поля
            self.users_db.update_user_by_id(self.id_user,
                                            self.ent_login.get(),
                                            self.ent_password.get(),
                                            self.ent_name.get(),
                                            self.txt_description.get('1.0', tk.END),
                                            self.is_admin.get(),   # Галочка is_admin
                                            self.is_deleted.get()  # Галочка is_deleted
                                            )
            self.parent.show_users()  # Выводим список пользователей
            self.btn_cancel.invoke()  # Имитация клика по "Отмена"


# ###
# Класс для формы динамически расширяющегося Canvas c Вертикальной полосой прокрутки
# ###
class UserRoles(tk.Toplevel):
    """ Класс формы управления зазначением ролей пользователю """
    def __init__(self, main, parent, id_user):
        super().__init__()

        self.title("Управление ролями")

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

        self.main = main  # Main
        self.parent = parent  # Users
        self.id_user = id_user

        self.users_roles = users_db.UsersRolesDB()  # БД роли-пользователей
        self.roles_db = users_db.RolesDB()  # БД ролей
        self.roles_list = self.roles_db.get_role_list_for_user_roles(self.id_user)  # Кортеж ролей пользорателя

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

    def show_permission(self):
        """ Процедура вывода массива галочек со списком ролей
        :return: No
        """
        self.checks = []
        for iter in range(len(self.roles_list)):
            self.checks.append(PermissionCheckButton(self.frm_permission,
                                                     iter,
                                                     self.roles_list[iter][0],
                                                     self.roles_list[iter][1],
                                                     self.roles_list[iter][2],
                                                     self.roles_list[iter][3]))

    def clear_frm_permission(self):
        """ Процедура очистки формы со вписком ролей """
        for widget in self.frm_permission.winfo_children():
            # widget.pack_forget()
            widget.destroy()

    def apply_filter(self):
        """ Процедура применения фильтрации по введенной строке
        :return: No
        """
        self.clear_frm_permission()  # Чистим форму с ролями
        self.roles_list = []  # Перезаполняем словарь полей
        if len(self.ent_filter.get()) == 0:
            self.roles_list = self.roles_db.get_role_list_for_user_roles(self.id_user)  # Кортеж ролей пользорателя
        else:
            self.roles_list = self.roles_db.get_role_list_for_user_roles_by_like_role_name(self.id_user,
                                                                                           self.ent_filter.get())
        self.show_permission()  # Перевыводим список ролей

    def save_permission(self):
        """ Процедура сохранения назначенных прав
        :return: No
        """
        for check in self.checks:
            if self.roles_list[check.iter][2] != check.exists_role.get():  # Значение изменилось
                if check.exists_role.get():  # На True
                    # print('Изменен элемент № ' + str(check.iter) + ' Добавдена роль ' + check.role_name)
                    self.add_role_for_user(check.id_role)
                else:
                    # print('Изменен элемент № ' + str(check.iter) + ' Удалена роль ' + check.role_name)
                    self.delete_role_for_user([check.id_users_roles])
        self.parent.show_users()  # Выводим список пользователей
        self.btn_cancel.invoke()  # Имитация клика по "Отмена"

    def add_role_for_user(self, id_role):
        """ Процедура добавления прав на новую роль """
        self.users_roles.save_new_user_role(self.id_user, id_role)

    def delete_role_for_user(self, id_users_roles):
        """ Процедура добавления прав на новую роль """
        self.users_roles.delete_user_roles(id_users_roles)


class PermissionCheckButton:
    """ Класс объекта галочка для списка ролей """
    def __init__(self, parent, iter, id_role, role_name, exists_role, id_users_roles):
        self.exists_role = tk.BooleanVar()
        self.iter = iter
        self.id_role = id_role
        self.role_name = role_name
        self.id_users_roles = id_users_roles
        self.exists_role.set(exists_role)  # Устанавливаем значение
        self.cb = tk.Checkbutton(parent, text=self.role_name, variable=self.exists_role, onvalue=1, offvalue=0)
        self.cb.grid(row=self.iter, column=0, sticky='w', pady=3, padx=10)
        # self.cb.pack(side=tk.BOTTOM)


# class Authorization(tk.Toplevel):
#     """ Базовый класс всплывающего окна авторизации """
#     def __init__(self, root=None, parent=None):
#         super().__init__()
#         self["bg"] = '#d7d8e0'  # цвет фона формы
#
#         self.title("Войдите в систему")
#         # тема
#         self.style = ttk.Style()
#         self.style.theme_use("default")
#         self.geometry('250x120+400+300')
#         self.resizable(False, False)
#
#         self.init_auth()  # Строим окно
#
#         self.users_db = users_db.UsersDB()  # Подключаем пользователей
#         self.root = root  # класс Main
#         self.parent = parent  # класс Logins
#
#     def init_auth(self):
#         # Добавляем функции модального, прехватываем фокус до закрытия
#         self.grab_set()
#         self.focus_set()
#
#         lbl_padding = {'sticky': 'w', 'padx': 10, 'pady': 10}
#         ent_padding = {'sticky': 'we', 'padx': 10}
#
#         # Таблица на 3 колонки
#         # 1 - ячейка для метки для подписи, текстовой поле на 2 ячейки
#         # 2-3 - ячейки для кнопок в последней строке
#
#         # # резировая ячейка для описания
#         # self.columnconfigure(1, weight=1)
#         # self.rowconfigure(5, weight=1)
#
#         # 1 Логин
#         lbl_login = ttk.Label(self, text="Логин", width=7)
#         lbl_login.grid(row=0, column=0, **lbl_padding)
#         self.ent_login = ttk.Entry(self)
#         self.ent_login.grid(row=0, column=1, columnspan=2, **ent_padding)
#         self.ent_login.bind("<Control-KeyPress>", gp.keys)
#
#         # 2 Пароль
#         lbl_password = ttk.Label(self, text="Пароль", width=7)
#         lbl_password.grid(row=1, column=0, **lbl_padding)
#         self.ent_password = ttk.Entry(self, show='*')
#         self.ent_password.grid(row=1, column=1, columnspan=2, **ent_padding)
#         self.ent_password.bind("<Control-KeyPress>", gp.keys)
#
#         # 3 Кнопки
#         btn_auth_login = ttk.Button(self, text='Войти', command=self.auth_user)
#         btn_auth_login.grid(row=2, column=1, sticky=tk.W + tk.E, pady=10, padx=10)
#
#         self.btn_cancel = ttk.Button(self, text='Отмена', command=self.destroy)
#         self.btn_cancel.grid(row=2, column=2, sticky=tk.W + tk.E, pady=10, padx=10)
#
#     def check_empty(self):
#         """ Процедура проверки на пустые поля формы
#         :return: True/False
#         """
#         if len(self.ent_login.get()) == 0:
#             mb.showwarning('Предупреждение', 'Введите логин')
#             return False
#         elif len(self.ent_password.get()) == 0:
#             mb.showwarning('Предупреждение', 'Введите пароль')
#             return False
#         return True
#
#     def check_exists(self):
#         """ Процедура проверки существования логина
#         :return: True/False
#         """
#         data = self.users_db.get_user_login_for_check_exists(self.ent_login.get())
#         if data is None:
#             mb.showwarning('Предупреждение', 'Логин не найден')
#             return False
#         return True
#
#     def check_pass(self):
#         """ Процедура проверки пароля
#         :return: True/False
#         """
#         data = self.users_db.get_password_by_login(self.ent_login.get())
#         if compute_md5_hash(self.ent_password.get()) != data:
#             mb.showwarning('Предупреждение', 'Пароль не верный')
#             return False
#         return True
#
#     def auth_user(self):
#         """ Процедура авторизаци пользователя """
#         if self.check_empty() and self.check_exists() and self.check_pass():  # проверка
#             print('Вход разрешен')
#             # имитация клика по "Отмена"
#             self.btn_cancel.invoke()

