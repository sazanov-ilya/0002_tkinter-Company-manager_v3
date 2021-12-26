import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb
# import sqlite3

# Импортируем свои модули
import __general_procedures as gp
import connection_types_db as connection_types_db  # БД для форм типов подключения

# Словарь фильтров
# connection_types_filter_dict = {'connection_type_name': '', 'connection_type_description': ''}
connection_types_filter_dict = {}


class ConnectionTypes(tk.Frame):
    """ Базовый класс для типов подключения, меню и список типов подключения """
    def __init__(self, root, main):
        super().__init__(root)

        self.root = root  # frm_content_all
        self.main = main  # Main
        self.connection_types_db = connection_types_db.ConnectionTypesDB()  # Подключаем бд Типов подключений

        self.init_connection_types()
        self.show_connection_types()  # Загружаем данные на форму

    def init_connection_types(self):
        # для отображения на полное окно
        self.pack(fill=tk.BOTH, expand=True)

        # Общая рамка для модуля
        # frm_connection_types = ttk.Frame(app.frm_content_all, relief=tk.RAISED, borderwidth=3)
        frm_connection_types = ttk.Frame(self, relief=tk.RAISED, borderwidth=0)
        frm_connection_types.pack(fill=tk.BOTH, expand=True)

        # Рамка верхнего toolbar
        frm_top_toolbar = ttk.Frame(frm_connection_types, relief=tk.RAISED, borderwidth=0)
        frm_top_toolbar.pack(fill=tk.X)

        # кнопки
        # 1
        self.btn_open_filter = tk.Button(frm_top_toolbar, text='Фильтр', **self.main.btn_style,
                                         command=self.open_connection_type_filter)
        self.btn_open_filter.pack(side=tk.LEFT, **self.main.btn_pack_padding)
        # 2
        btn_open_new = tk.Button(frm_top_toolbar, text='Добавить', **self.main.btn_style,
                                 command=self.open_new_connection_type)
        btn_open_new.pack(side=tk.LEFT, **self.main.btn_pack_padding)
        # 3
        btn_open_update = tk.Button(frm_top_toolbar, text='Редактировать', **self.main.btn_style,
                                    command=self.open_update_connection_type)
        btn_open_update.pack(side=tk.LEFT, **self.main.btn_pack_padding)
        # 4
        btn_delete = tk.Button(frm_top_toolbar, text='Удалить', **self.main.btn_style,
                               command=self.delete_connection_types)
        btn_delete.pack(side=tk.LEFT, **self.main.btn_pack_padding)

        # контент модуля
        frm_connection_types_content = ttk.Frame(frm_connection_types, relief=tk.RAISED, borderwidth=0)
        frm_connection_types_content.pack(fill=tk.BOTH, expand=True)

        # список Treeview
        self.connection_types_list = ttk.Treeview(frm_connection_types_content,
                                                  columns=('id_connection', 'connection_name',
                                                           'connection_description'), height=10, show='headings')
        # параметры столбцов
        self.connection_types_list.column("id_connection", width=40, anchor=tk.CENTER)
        self.connection_types_list.column("connection_name", width=150, anchor=tk.CENTER)
        self.connection_types_list.column("connection_description", width=355, anchor=tk.CENTER)
        # названия столбцов
        self.connection_types_list.heading('id_connection', text='ID')
        self.connection_types_list.heading('connection_name', text='Наименование')
        self.connection_types_list.heading('connection_description', text='Описание')
        # вывод с выравниванием по левой стороне
        self.connection_types_list.pack(fill="both", side='left', expand=True)
        # вешаем контекстное меню на ЛКМ
        self.connection_types_list.bind('<Button-3>', self.show_context_menu)

        # полоса прокрутки для списка
        scroll = tk.Scrollbar(frm_connection_types_content, command=self.connection_types_list.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.connection_types_list.configure(yscrollcommand=scroll.set)

        # контекстное меню для копирования
        self.context_menu = tk.Menu(self.connection_types_list, tearoff=0)
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
        if self.connection_types_list.focus() != '':
            self.connection_types_list.identify_row(event.y)
            self.context_menu.post(event.x_root, event.y_root)

    def copy_name(self):
        """ Процедура копирования в буфер обмена """
        self.root.clipboard_clear()
        self.root.clipboard_append(self.connection_types_list.set(self.connection_types_list.selection()[0], '#2'))

    def copy_description(self):
        """ Процедура копирования в буфер обмена """
        self.root.clipboard_clear()
        self.root.clipboard_append(self.connection_types_list.set(self.connection_types_list.selection()[0], '#3'))

    def copy_all(self):
        """ Процедура копирования в буфер обмена """
        self.root.clipboard_clear()
        self.root.clipboard_append(self.connection_types_list.set(self.connection_types_list.selection()[0], '#2') + '\n' +
                                   self.connection_types_list.set(self.connection_types_list.selection()[0], '#3'))

    def show_connection_types(self):
        """ Процедура заполнения списка тиов подключения согласно данных БД и фильтров """
        self.color_btn_filter()  # Цвет кнопки фильтра
        [self.connection_types_list.delete(i) for i in self.connection_types_list.get_children()]  # Очистка таблицы
        data = self.connection_types_db.get_connection_type_list_by_filter(connection_types_filter_dict)
        # [self.connection_types_list.insert('', 'end', values=row) for row in self.db.c_sqlite3.fetchall()]
        [self.connection_types_list.insert('', 'end', values=row) for row in data]

    def delete_connection_types(self):
        """ Процедура удаления выбранных типов подключения """
        if self.connection_types_list.focus() != '':
            answer = mb.askyesno(title='Запрос действия',
                                 message="Хотите удалить выбранные элементы?")
            if answer:  # если Да = True
                # Цикл удаление нескольких записей
                # [ids.append(row) for row in self.[ids.append(row) for row in self._list.selection()]_list.selection()]
                ids = []  # кортеж id выделенных элементов
                for selection_item in self.connection_types_list.selection():
                    ids.append(self.connection_types_list.set(selection_item, '#1'),)
                self.connection_types_db.delete_connection_types(ids)
                self.show_connection_types()  # перезагружаем список

                ## Запятая (self.tree.set(select, '#1'),)) - для удаление при более 10 записей
                #for selection_item in self.connection_types_list.selection():
                #    self.db.c_sqlite3.execute(
                #        '''DELETE FROM connection_types WHERE id_connection=?''', (self.connection_types_list.set(selection_item, '#1'),)
                #    )
                #self.db.conn_sqlite3.commit()
        else:
            mb.showwarning('Предупреждение', 'Выберите тип подключения')

    def open_new_connection_type(self):
        """ Открываем форму ввода нового типа подключения """
        NewConnectionType(self)

    def open_update_connection_type(self):
        """ Открываем окно для обновления выбранного типа подключения """
        if self.connection_types_list.focus() != '':
            UpdateConnectionType(self, self.connection_types_list.set(self.connection_types_list.selection()[0], '#1'))
        else:
            mb.showwarning('Предупреждение', 'Выберите тип подключения')

    def open_connection_type_filter(self):
        """ Открываем форму ввода фильтров для списка типов подключения """
        FilterConnectionTypes(self)

    def color_btn_filter(self):
        """ Процедкра смены цвета кнопки Фильтр """
        if connection_types_filter_dict:  # Если есть фильтры
            self.btn_open_filter.configure(bg='#A9A9A9')
        else:
            self.btn_open_filter.configure(bg='#f0f0f0')

    def apply_connection_type_filter(self, connection_type_name, connection_type_description):
        """ Процедура применения фильтра
        :param connection_type_name: Название типа подключения
        :param connection_type_description: Описание типа подключения
        :return No
        """
        connection_types_filter_dict.clear()  # чистим словарь
        # пересоздаем словарь
        if connection_type_name:  # сохраняем фильтр в словарь
            connection_types_filter_dict['connection_type_name'] = connection_type_name
        if connection_type_description:
            connection_types_filter_dict['connection_type_description'] = connection_type_description
        self.show_connection_types()  # перезегружаем список

    def clear_connection_type_filter(self):
        """ Процедура очистки фильтров типов подключения """
        # for key in connection_types_filter_dict:
        #    connection_types_filter_dict[key] = ''  # обнуляем ключи
        #    self.show_connection_types()     # перезегружаем список компаний
        connection_types_filter_dict.clear()  # чистим словарь
        self.show_connection_types()  # перезегружаем список


class ConnectionType(tk.Toplevel):
    """ Базовый класс формы типа подключения """
    def __init__(self, parent=None):
        super().__init__()

        self.parent = parent  # Main
        self.connection_types_db = connection_types_db.ConnectionTypesDB()  # Подключаем бд Типов подключений

        self.init_connection_type()
        self.clear_connection_type()  # Чистим форму

    def init_connection_type(self):
        self.geometry('415x200+400+300')
        self.resizable(False, False)

        # Добавляем функции модального, т.е прехватываем фокус не нем до закрытия
        self.grab_set()
        self.focus_set()

        # Создаем поля формы
        lbl_connection_type_name = tk.Label(self, text='Тип подключения')
        lbl_connection_type_name.place(x=50, y=20)
        self.ent_connection_type_name = ttk.Entry(self)
        self.ent_connection_type_name.place(x=200, y=20, width=180)
        self.ent_connection_type_name.bind("<Control-KeyPress>", gp.keys)
        self.ent_connection_type_name.focus()

        lbl_connection_type_description = tk.Label(self, text='Описание')
        lbl_connection_type_description.place(x=50, y=50)
        self.txt_connection_type_description = tk.Text(self)
        self.txt_connection_type_description.place(x=200, y=50, width=180, height=100)
        self.txt_connection_type_description.bind("<Control-KeyPress>", gp.keys)

        # Полоса прокрутки
        scroll = tk.Scrollbar(self, command=self.txt_connection_type_description.yview)
        # scroll.pack(side=tk.RIGHT, fill=tk.Y)
        scroll.place(x=380, y=50, height=100)
        self.txt_connection_type_description.configure(yscrollcommand=scroll.set)

        self.btn_cancel = ttk.Button(self, text='Отмена', command=self.destroy)
        self.btn_cancel.place(x=305, y=160)

    def clear_connection_type(self):
        """ Процедура очистки полей формы """
        self.ent_connection_type_name.delete(0, tk.END)
        self.txt_connection_type_description.delete(1.0, tk.END)

    def check_empty(self):
        """ Процедура проверки на пустые поля формы
        :return: True/False
        """
        if len(self.ent_connection_type_name.get()) == 0:
            mb.showwarning('Предупреждение', 'Введите тип подключения')
            return False
        return True

    def check_exists(self):
        """ Процедура проверки дубли по введенным данным
        :return: True/False
        """
        connection_type_name = self.ent_connection_type_name.get()
        data = self.connection_types_db.get_connection_type_name_by_name(connection_type_name)
        if data:
            mb.showwarning('Предупреждение', 'Дубль логина <' + data + '>')
            return False
        return True


class NewConnectionType(ConnectionType):
    """ Класс формы добавления подключения """
    def __init__(self, parent):  # Конструктор
        super().__init__()

        self.parent = parent  # Main

        self.init_new_connection_type()

    def init_new_connection_type(self):
        self.title('Добавить подключение')

        btn_save = ttk.Button(self, text='Сохранить', command=self.save_new_connection_type)
        btn_save.place(x=220, y=160)
        # btn_save.bind('<Button-1>', lambda event: self.main.save_new_connection_type(
        #    self.ent_connection_type_name.get(), self.txt_connection_types_description.get('1.0', tk.END)
        # ))

    def save_new_connection_type(self):
        """ Процедура сохранения нового логина """
        if self.check_empty() and self.check_exists():  # проверка на пустые поля и дубль
            # Получаем поля с формы
            connection_type_name = self.ent_connection_type_name.get()
            connection_type_description = gp.get_text_in_one_line(
                self.txt_connection_type_description.get('1.0', tk.END))
            # Сохраняем
            self.connection_types_db.insert_new_connection_type(connection_type_name, connection_type_description)
            self.parent.show_connection_types()  # Выводим на форму
            self.btn_cancel.invoke()  # Имитация клика по "Отмена"


class UpdateConnectionType(ConnectionType):
    """ Класс формы обновления типов подключений """
    def __init__(self, parent, id_connection_type):  # Конструктор
        super().__init__()

        self.parent = parent  # класс ConnectionTypes
        self.id_connection_type = id_connection_type

        self.init_update_connection_type()
        self.get_connection_type_for_update()

    def init_update_connection_type(self):
        self.title('Обновить тип подключение')
        btn_update = ttk.Button(self, text='Обновить', command=self.update_connection_type)
        btn_update.place(x=220, y=160)

    def get_connection_type_for_update(self):
        """ Процедура получения и вывода на форму данных выделенной строки """
        # print(self.id_connection_type)
        data = self.connection_types_db.get_connection_type_by_id(self.id_connection_type)
        # Выводим значения в поля формы
        self.ent_connection_type_name.insert(0, data[1])
        self.txt_connection_type_description.insert(1.0, data[2])

    def update_connection_type(self):
        """ Процедура сохранения нового типа подключения """
        if self.check_empty():  # проверка на пустые поля
            # получаем поля с формы
            connection_type_name = self.ent_connection_type_name.get()
            connection_type_description = gp.get_text_in_one_line(
                self.txt_connection_type_description.get('1.0', tk.END))
            self.connection_types_db.update_connection_type_by_id(self.id_connection_type, connection_type_name,
                                                                  connection_type_description)  # обновляем
            self.parent.show_connection_types()  # выводим на форму
            self.btn_cancel.invoke()  # имитация клика по "Отмена"


class FilterConnectionTypes(tk.Toplevel):
    """ Класс формы фильльтра для отображения списка подключений """
    def __init__(self, parent):
        super().__init__()

        self.parent = parent  # Передаем класс Main

        self.init_filter_connection_type()


    def init_filter_connection_type(self):
        self.title('Фильтр типов доступа')
        self.geometry('415x125+400+300')
        self.resizable(False, False)

        # Добавляем функции модального, прехватываем фокус на нем до закрытия
        self.grab_set()
        self.focus_set()

        lbl_connection_type_name = tk.Label(self, text='Тип подключения')
        lbl_connection_type_name.place(x=50, y=20)
        self.ent_connection_type_name = ttk.Entry(self)
        self.ent_connection_type_name.place(x=200, y=20, width=180)
        self.ent_connection_type_name.insert(0, connection_types_filter_dict.get('connection_type_name', ''))  # имя
        self.ent_connection_type_name.bind("<Control-KeyPress>", gp.keys)
        self.ent_connection_type_name.focus()

        lbl_connection_type_description = tk.Label(self, text='Описание')
        lbl_connection_type_description.place(x=50, y=50)
        self.ent_connection_type_description = ttk.Entry(self)
        self.ent_connection_type_description.place(x=200, y=50, width=180)
        self.ent_connection_type_description.insert(0, connection_types_filter_dict.get('connection_type_description',
                                                                                        ''))  # описание
        self.ent_connection_type_description.bind("<Control-KeyPress>", gp.keys)

        btn_clear_connection_type_filter = ttk.Button(self, text='Сбросить')
        btn_clear_connection_type_filter.place(x=65, y=85)
        btn_clear_connection_type_filter.bind('<Button-1>', lambda event: self.parent.clear_connection_type_filter())
        btn_clear_connection_type_filter.bind('<Button-1>', lambda event: self.destroy(), add='+')  # Доп событие

        btn_apply_connection_type_filter = ttk.Button(self, text='Применить')
        btn_apply_connection_type_filter.place(x=145, y=85)
        btn_apply_connection_type_filter.bind('<Button-1>', lambda event: self.parent.apply_connection_type_filter(
            self.ent_connection_type_name.get(), self.ent_connection_type_description.get()))
        btn_apply_connection_type_filter.bind('<Button-1>', lambda event: self.destroy(), add='+')  # Доп событие

        btn_closed_connection_type_filter = ttk.Button(self, text='Отмена', command=self.destroy)
        btn_closed_connection_type_filter.place(x=225, y=85)
