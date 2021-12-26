import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb
# import hashlib


# импортируем свои модули
import __general_procedures as gp
import users_db as users_db  # БД для форм пользователей


# Словарь фильтров
roles_filter_dict = {}


class Roles(tk.Frame):
    """ Класс формы списка ролей """
    def __init__(self, root, main):
        super().__init__(root)

        self.root = root  # frm_content_all
        self.main = main  # Main

        # self.users_db = users_db.UsersDB()  # БД пользователей
        self.roles_db = users_db.RolesDB()  # БД ролей

        self.init_roles()
        self.show_roles()

    def init_roles(self):
        # self.title('Список логинов')

        # Резиновая ячейка с таблицей
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Для отображения данных на форме
        self.pack(fill=tk.BOTH, expand=True)

        # Рамка для toolbar
        frm_roles_top_toolbar = ttk.Frame(self, relief=tk.RAISED, borderwidth=0)
        frm_roles_top_toolbar.grid(row=0, column=0, columnspan=2, sticky='nwse')

        # Кнопки
        # 1
        self.btn_open_filter = tk.Button(frm_roles_top_toolbar, text='Фильтр', **self.main.btn_style,
                                         command=self.open_filter_role)
        self.btn_open_filter.pack(side=tk.LEFT, **self.main.btn_pack_padding)
        # 2
        btn_open_new_roles = tk.Button(frm_roles_top_toolbar, text='Добавить', **self.main.btn_style,
                                       command=self.open_new_role)
        btn_open_new_roles.pack(side=tk.LEFT, **self.main.btn_pack_padding)
        # 3
        btn_open_update_roles = tk.Button(frm_roles_top_toolbar, text='Редактировать', **self.main.btn_style,
                                          command=self.open_update_role)
        btn_open_update_roles.pack(side=tk.LEFT, **self.main.btn_pack_padding)
        # 4
        btn_open_delete_roles = tk.Button(frm_roles_top_toolbar, text='Удалить', **self.main.btn_style,
                                          command=self.delete_roles)
        btn_open_delete_roles.pack(side=tk.LEFT, **self.main.btn_pack_padding)

        # Список Treeview
        self.roles_table = ttk.Treeview(self, columns=('id_role', 'role_name', 'role_description'),
                                        height=10, show='headings')
        # Параметры столбцов
        self.roles_table.column("id_role", width=50, anchor=tk.CENTER)
        self.roles_table.column("role_name", width=100, anchor=tk.W)
        self.roles_table.column("role_description", width=250, anchor=tk.W)
        # названия столбцов
        self.roles_table.heading('id_role', text='ID')
        self.roles_table.heading('role_name', text='Наименование')
        self.roles_table.heading('role_description', text='Описание')

        self.roles_table.grid(row=1, column=0, sticky='nwse')

        # Вешаем контекстное меню на ЛКМ
        self.roles_table.bind('<Button-3>', self.show_context_menu)

        # Полоса прокрутки для таблицы
        scroll = tk.Scrollbar(self, command=self.roles_table.yview)
        # scroll.pack(side=tk.RIGHT, fill=tk.Y)
        scroll.grid(row=1, column=1, sticky='nwse')
        self.roles_table.configure(yscrollcommand=scroll.set)

        # # рамка для нижнего toolbar
        # frm_logins_bottom_toolbar = ttk.Frame(self, relief=tk.RAISED, borderwidth=0)
        # frm_logins_bottom_toolbar.grid(row=3, column=0, columnspan=2, sticky='nwse')
        # # Кнопки
        # # 1
        # self.btn_ligins_back = tk.Button(frm_logins_bottom_toolbar, text='Назад', bg='#d7d8e0', bd=0,
        #                                  compound=tk.BOTTOM, relief=tk.GROOVE, borderwidth=5, pady=2, padx=10,
        #                                  command=self.open_connections)
        # self.btn_ligins_back.pack(side=tk.RIGHT, padx=17, pady=10)

        # Контекстное меню для копирования
        self.context_menu = tk.Menu(self.roles_table, tearoff=0)
        self.context_menu.add_command(
            label='Копировать наименование', command=self.copy_name)
        self.context_menu.add_command(
            label='Копировать описание', command=self.copy_description)
        # self.context_menu.add_command(
        #     label='Копировать все', command=self.copy_all)

    def show_context_menu(self, event):
        """ Процедура вывода контекстного меню
        :param event:
        :return:
        """
        if self.roles_table.focus() != '':
            self.roles_table.identify_row(event.y)
            self.context_menu.post(event.x_root, event.y_root)

    def copy_name(self):
        """ Процедура копирования наименования в буфер обмена """
        self.root.clipboard_clear()
        self.root.clipboard_append(self.roles_table.set(self.roles_table.selection()[0], '#2'))

    def copy_description(self):
        """ Процедура копирования описания в буфер обмена """
        self.root.clipboard_clear()
        self.root.clipboard_append(self.roles_table.set(self.roles_table.selection()[0], '#3'))

    def copy_all(self):
        """ Процедура копирования наименования и описания  в буфер обмена """
        self.root.clipboard_clear()
        self.root.clipboard_append(self.roles_table.set(self.roles_table.selection()[0], '#2') + '\n' +
                                   self.roles_table.set(self.roles_table.selection()[0], '#3'))

    def color_btn_filter(self):
        """ Процедкра смены цвета кнопки Фильтра """
        if roles_filter_dict:  # Если есть фильтры
            self.btn_open_filter.configure(bg='#A9A9A9')
        else:
            self.btn_open_filter.configure(bg='#f0f0f0')

    def show_roles(self):
        """ Процедура перезаполнения списка ролей согласно данных БД и фильтров """
        self.color_btn_filter()  # Цвет кнопки фильтра

        [self.roles_table.delete(i) for i in self.roles_table.get_children()]  # чистим таблицу

        data = self.roles_db.get_roles_by_filter(roles_filter_dict.get('role_name', ''),
                                                 roles_filter_dict.get('role_description', ''))

        [self.roles_table.insert('', 'end', values=row) for row in data]  # выводим список на форму

    def open_filter_role(self):
        """ Открываем окно фильтров списка ролей"""
        FilterRole(self.main, self)

    def open_new_role(self):
        """ Открываем окно для ввода новой роли"""
        NewRole(self.main, self)

    def open_update_role(self):
        """ Открываем окно для редактирования выбранной роли"""
        if self.roles_table.focus() != '':
            if self.roles_db.get_role_for_admin() != self.roles_table.set(self.roles_table.selection()[0], '#2'):
                UpdateRole(self.main, self, self.roles_table.set(self.roles_table.selection()[0], '#1'))
            else:
                mb.showwarning('Предупреждение', 'Редактирование базовой роли для администратора запрещено')
        else:
            mb.showwarning('Предупреждение', 'Выберите роль')

    def set_filter(self, role_name, role_description):
        """ Процедура применения фильтра
        :param role_name:
        :param role_description:
        :return: No
        """
        roles_filter_dict.clear()  # Чистим словарь
        # Пересоздаем словарь
        if role_name:
            roles_filter_dict['role_name'] = role_name
        if role_description:
            roles_filter_dict['role_description'] = role_description

        self.show_roles()  # перезегружаем список

    def delete_roles(self):
        """ Процедура удаления выбранных ролей """
        if self.roles_table.focus() != '':
            answer = mb.askyesno(title='Запрос действия',
                                 message="Хотите удалить выбранные элементы?")
            if answer:  # если Да = True
                ids = []  # кортеж id выделенных элементов
                for selection_item in self.roles_table.selection():
                    ids.append(self.roles_table.set(selection_item, '#1'),)
                self.roles_db.delete_roles(ids)
                self.show_roles()  # Перевыводим список
                # self.users_db.check_count_admins()  # Проверяем админов (для расблокировки базового)
        else:
            mb.showwarning('Предупреждение', 'Выберите роль/роли')


class Role(tk.Toplevel):
    """ Базовый класс всплывающего окна роли """
    def __init__(self, main, parent):
        super().__init__()
        self["bg"] = '#d7d8e0'  # Цвет фона формы

        self.title("Роль")
        # Тема
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.geometry('415x200+400+300')
        self.resizable(False, False)

        self.main = main  # Main
        self.parent = parent  # Roles

        self.roles_db = users_db.RolesDB()  # Подключаем роли

        self.init_role()  # Строим форму

    def init_role(self):
        # Добавляем функции модального, прехватываем фокус до закрытия
        self.grab_set()
        self.focus_set()

        lbl_padding = {'sticky': 'w', 'padx': 10, 'pady': 10}
        ent_padding = {'sticky': 'we', 'padx': 10}

        # Резировая ячейка для описания
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

        # 1 Наименование
        lbl_name = ttk.Label(self, text="Роль", width=10)
        lbl_name.grid(row=0, column=0, **lbl_padding)
        self.ent_name = ttk.Entry(self)
        self.ent_name.grid(row=0, column=1, columnspan=4, **ent_padding)
        self.ent_name.focus()
        self.ent_name.bind("<Control-KeyPress>", gp.keys)

        # 2 Описание
        lbl_description = ttk.Label(self, text="Описание", width=10)
        lbl_description.grid(row=1, column=0, sticky='n', pady=10, padx=10)
        self.txt_description = tk.Text(self)
        self.txt_description.grid(row=1, column=1, columnspan=4, sticky='nwse', pady=10, padx=10)
        self.txt_description.bind("<Control-KeyPress>", gp.keys)

        # # Полоса прокрутки
        # scroll = tk.Scrollbar(self, command=self.txt_description.yview)
        # # scroll.pack(side=tk.RIGHT, fill=tk.Y)
        # scroll.grid(row=1, column=5, sticky='nwse', pady=10)
        # self.txt_description.configure(yscrollcommand=scroll.set)


        # 7 Кнопки
        self.btn_cancel = ttk.Button(self, text='Отмена', command=self.destroy)
        self.btn_cancel.grid(row=2, column=4, sticky=tk.W + tk.E, pady=10, padx=10)

    def check_empty(self):
        """ Процедура проверки на пустые поля формы
        :return: True/False
        """
        if len(self.ent_name.get()) == 0:
            mb.showwarning('Предупреждение', 'Введите роль')
            return False
        return True

    def check_exists(self):
        """ Процедура проверки дублей роли по введенным данным
        :return: True/False
        """
        data = self.roles_db.get_role_for_check_exists(self.ent_name.get())
        if data:
            mb.showwarning('Предупреждение', 'Роль <' + data + '> уже существует')
            return False
        return True


class FilterRole(Role):
    """ Класс формы фильтров для списка ролей """
    def __init__(self, main, parent):
        super().__init__(main, parent)

        self.main = main  # Main
        self.parent = parent  # Logins

        self.init_filter_role()  # Строим форму
        self.get_filter()  # Выводим фильтры

    def init_filter_role(self):
        self.title("Фильтр списка ролей")

        # Добавляем кнопки
        btn_apply_filter = ttk.Button(self, text='Применить', command=self.apply_filter)
        btn_apply_filter.grid(row=2, column=2, sticky=tk.W + tk.E, pady=10, padx=10)

        btn_clear_filter = ttk.Button(self, text='Сбросить', command=self.clear_filter)
        btn_clear_filter.grid(row=2, column=3, sticky=tk.W + tk.E, pady=10, padx=10)

        # btn_clear_connection_filter.bind('<Button-1>', lambda event: self.parent.clear_connection_filter())
        # btn_clear_connection_filter.bind('<Button-1>', lambda event: self.destroy(), add='+')  # Доп событие

    def get_filter(self):
        """ Процедура получения текущих значений фильтра и вывод на форму """
        if roles_filter_dict:
            if roles_filter_dict.get('role_name', ''):
                self.ent_name.insert(0, roles_filter_dict.get('role_name', ''))
            if roles_filter_dict.get('role_description', ''):
                self.txt_description.insert(1.0, roles_filter_dict.get('role_description', ''))

    def apply_filter(self):
        """ Процедура применения фильтров """
        self.parent.set_filter(self.ent_name.get(),
                               gp.get_text_in_one_line(self.txt_description.get('1.0', tk.END)))
        self.btn_cancel.invoke()  # Имитация клика по кнопке закрыть

    def clear_filter(self):
        """ Процедура применения фильтров """
        self.parent.set_filter(None, None)
        self.btn_cancel.invoke()  # Имитация клика по кнопке закрыть


class NewRole(Role):
    """ Класс формы добавления новой роли """
    def __init__(self, main, parent):
        super().__init__(main, parent)

        self.main = main  # Main
        self.parent = parent  # Logins

        self.init_new_role()

    def init_new_role(self):
        self.title("Добавить новую роль")

        # 7 Кнопки
        btn_save = ttk.Button(self, text='Сохранить', command=self.save_new_role)
        btn_save.grid(row=2, column=3, sticky=tk.W + tk.E, pady=10, padx=10)

    def save_new_role(self):
        """ Процедура сохранения новой роли """
        if self.check_empty() and self.check_exists():  # Проверка на пустые поля и дубль
            self.roles_db.insert_new_role(self.ent_name.get(),
                                          self.txt_description.get('1.0', tk.END))
            self.parent.show_roles()  # Выводим список ролей
            self.btn_cancel.invoke()  # Имитация клика по "Отмена"


class UpdateRole(Role):
    """ Класс формы обновления роли """
    def __init__(self, main, parent, id_role):
        super().__init__(main, parent)

        self.main = main  # Main
        self.parent = parent  # Logins
        self.id_role = id_role

        self.init_update_role()
        self.get_role_for_update()

    def init_update_role(self):
        self.title("Редактировать роль")

        # Кнопки
        btn_save = ttk.Button(self, text='Обновить', command=self.update_role)
        btn_save.grid(row=2, column=3, sticky=tk.W + tk.E, pady=10, padx=10)

    def get_role_for_update(self):
        """ Процедура получения и вывода на форму данных выделенной строки """
        data = self.roles_db.get_role_by_id(self.id_role)
        self.ent_name.insert(0, data[1])
        self.txt_description.insert(1.0, data[2])

    def update_role(self):
        """ Процедура обновления типа подключения """
        if self.check_empty():  # проверка на пустые поля
            self.roles_db.update_role_by_id(self.id_role,
                                            self.ent_name.get(),
                                            gp.get_text_in_one_line(self.txt_description.get('1.0', tk.END)))
            self.parent.show_roles()  # Выводим список на форму
            self.btn_cancel.invoke()  # Имитация клика по кнопке закрыть
