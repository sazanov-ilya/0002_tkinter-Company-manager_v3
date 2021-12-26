import sqlite3
import tkinter.messagebox as mb

# Свои модули
import __general_procedures as gp
import main_db_sqlite3 as db  # БД - общий


class CompaniesDB(db.DB):
    """ Класс работы с таблицей компаний """
    def __init__(self):
        super().__init__()  # вызов __init__ базового класса

    ###########################
    # Процедуры для companies #
    ###########################
    def get_company_by_id(self, id_company):
        """ Процедура возврата данных компании по переданному id
        :param id_company:
        :return: No
        """
        try:
            self.c_sqlite3.execute(
                '''SELECT id_company, company_name, company_description FROM companies WHERE id_company=?''',
                [id_company]
            )
        except sqlite3.Error as err:
            mb.showerror("ОШИБКА!", err.__str__())
            # self.root.destroy()
        data = self.c_sqlite3.fetchone()  # возвращает только одну запись
        return data

    def get_company_name_by_name(self, company_name):
        """ Процедура проверки наличия компании по ее имени
        :param company_name: Название компании
        :return: company_name/None
        """
        company_name = company_name.lower()
        try:
            self.c_sqlite3.execute(
                '''SELECT company_name FROM companies WHERE LOWER(company_name) = ?''', [company_name]
            )
        except sqlite3.Error as err:
            mb.showerror("ОШИБКА!", err.__str__())
            # self.root.destroy()
        data = self.c_sqlite3.fetchone()
        if data is not None:
            return data[0]
        else:
            return None

    def get_company_list_by_filter(self, companies_filter_dict):
        """ Процедура возврата результата списка компаний согласно фильтров
        :param companies_filter_dict:
        :return: Набор кортежей
        """
        match companies_filter_dict:
            # company_name/company_description
            case {'company_name': company_name, 'company_description': company_description}:
                f_company_name = ('%' + company_name.lower() + '%')
                f_company_description = ('%' + company_description.lower() + '%')
                try:
                    self.c_sqlite3.execute(
                        '''SELECT id_company, company_name, company_description FROM companies 
                           WHERE LOWER(company_name) LIKE ? AND LOWER(company_description) LIKE ?''',
                        [f_company_name, f_company_description]
                    )
                except sqlite3.Error as err:
                    mb.showerror("ОШИБКА!", err.__str__())
            # company_name
            case {'company_name': company_name}:
                f_company_name = ('%' + company_name.lower() + '%')
                try:
                    self.c_sqlite3.execute(
                        '''SELECT id_company, company_name, company_description FROM companies 
                           WHERE LOWER(company_name) LIKE ?''', [f_company_name]
                    )
                except sqlite3.Error as err:
                    mb.showerror("ОШИБКА!", err.__str__())
            # company_description
            case {'company_description': company_description}:
                f_company_description = ('%' + company_description.lower() + '%')
                try:
                    self.c_sqlite3.execute(
                        '''SELECT id_company, company_name, company_description FROM companies 
                           WHERE LOWER(company_description) LIKE ?''', [f_company_description]
                    )
                except sqlite3.Error as err:
                    mb.showerror("ОШИБКА!", err.__str__())
            # Прочее
            case _:
                try:
                    self.c_sqlite3.execute(
                        '''SELECT id_company, company_name, company_description FROM companies'''
                    )
                except sqlite3.Error as err:
                    mb.showerror("ОШИБКА!", err.__str__())
        data = []  # Запрос возвращает набор кортежей
        [data.append(row) for row in self.c_sqlite3.fetchall()]

        return data

#     def get_company_list_by_filter(self, company_name, company_description):
#         """ Процедура возврата результата списка компаний согласно фильтров
#         :param company_name: Фильтр по названию компании
#         :param company_description: Фильтр по описанию для компании
#         :return: набор кортежей со списком компаний согласно фильтров
#         """
#         if company_name and company_description:  # проверяем фильтр
#             company_filter_name = ('%' + company_name.lower() + '%')
#             company_filter_description = ('%' + company_description.lower() + '%')
#             try:
#                 self.c_sqlite3.execute(
#                     '''SELECT id_company, company_name, company_description FROM companies WHERE company_name LIKE ?
#                     AND company_description LIKE ?''',
#                     [company_filter_name, company_filter_description]
#                 )
#             except sqlite3.Error as err:
#                 mb.showerror("ОШИБКА!", err.__str__())
#                 # self.root.destroy()
#         elif company_name:  # Проверяем фильтр
#             company_filter_name = ('%' + company_name.lower() + '%')
#             # company_filter_description = ('%' + company_filter_description.lower() + '%',)
#
#             # рабочий
#             # company_filter_name = ('%' + company_filter_name.lower() + '%',)
#             # self.db.c_sqlite3.execute(
#             #    '''SELECT id_company, company_name, company_description FROM companies WHERE company_name LIKE ?''',
#             #    (company_filter_name)
#             # )
#
#             try:
#                 self.c_sqlite3.execute(
#                     '''SELECT id_company, company_name, company_description FROM companies WHERE company_name LIKE ?''',
#                     [company_filter_name]
#                 )
#             except sqlite3.Error as err:
#                 mb.showerror("ОШИБКА!", err.__str__())
#                 # self.root.destroy()
#         elif company_description:  # Проверяем фильтр
#             # company_filter_name = ('%' + company_filter_name.lower() + '%',)
#             company_filter_description = ('%' + company_description.lower() + '%')
#             try:
#                 self.c_sqlite3.execute(
#                     '''SELECT id_company, company_name, company_description FROM companies
#                     WHERE company_description LIKE ?''', [company_filter_description]
#                 )
#             except sqlite3.Error as err:
#                 mb.showerror("ОШИБКА!", err.__str__())
#                 # self.root.destroy()
#         else:
#             try:
#                 self.c_sqlite3.execute(
#                     '''SELECT id_company, company_name, company_description FROM companies'''
#                 )
#             except sqlite3.Error as err:
#                 mb.showerror("ОШИБКА!", err.__str__())
#                 # self.root.destroy()
#         data = []  # запрос возвращает набор кортежей
#         [data.append(row) for row in self.c_sqlite3.fetchall()]
# #        [self.companies_list.insert('', 'end', values=row) for row in self.db.c_sqlite3.fetchall()]
#         return data

    def get_company_for_list(self):
        """ Процедура возвращает список компаний для выпадающего списка
        :return: набор кортежей id и company_name
        """
        try:
            self.c_sqlite3.execute(
                '''SELECT id_company, company_name FROM companies'''
            )
        except sqlite3.Error as err:
            mb.showerror("ОШИБКА!", err.__str__())
            # self.root.destroy()

        data = []  # запрос возвращает набор кортежей
        [data.append(row) for row in self.c_sqlite3.fetchall()]
        return data

    def insert_new_company(self, company_name, company_description):
        """ Процедура сохранения данных новой компании
        :param company_name: Название компании
        :param company_description: Описание для компании
        :return: No
        """
        try:
            self.c_sqlite3.execute(
                '''INSERT INTO companies(company_name, company_description) VALUES(?, ?)''',
                (company_name, gp.get_text_in_one_line(company_description))
            )
            self.conn_sqlite3.commit()
        except sqlite3.Error as err:
            mb.showerror("ОШИБКА!", err.__str__())
            # self.root.destroy()

    def update_company_by_name(self, company_name, company_description):
        """ Процедура обновления данных компании по ее имени
        :param company_name: Название компании
        :param company_description: Комментарий для компании
        :return: No
        """
        try:
            self.c_sqlite3.execute(
                '''UPDATE companies SET company_name=?, company_description=? WHERE LOWER(company_name) = ?''',
                (company_name.lower(), company_description, company_name.lower())
            )
            self.conn_sqlite3.commit()
        except sqlite3.Error as err:
            mb.showerror("ОШИБКА!", err.__str__())
            # self.root.destroy()

    def update_company_by_id(self, id_company, company_name, company_description):
        """ Процедура обновления данных компании по ее id
        :param id_company: Id компании
        :param company_name: Название компании
        :param company_description: Комментарий для компании
        :return No
        """
        try:
            self.c_sqlite3.execute(
                '''UPDATE companies SET company_name=?, company_description=? WHERE id_company=?''',
                (company_name, gp.get_text_in_one_line(company_description), id_company)
            )
            self.conn_sqlite3.commit()
        except sqlite3.Error as err:
            mb.showerror("ОШИБКА!", err.__str__())
            # self.root.destroy()

    def delete_companies(self, ids):
        """ Процедура удаления выбранных в списке компаний
        :param ids: Список id компаний
        :return: No
        """
        try:
            for id in ids:
                self.c_sqlite3.execute(
                    '''DELETE FROM companies WHERE id_company=?''', [id]
                    )
                self.conn_sqlite3.commit()
        except sqlite3.Error as err:
            mb.showerror("ОШИБКА!", err.__str__())
            # self.root.destroy()
