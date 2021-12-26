import os
import errno
import sqlite3
import tkinter.messagebox as mb


path_db = 'db'
# Список ролей для создания
roles = ['admin', 'manager', 'user']


def create_db_dir():
    # path = os.curdir  # Текущая папка
    # path = os.getcwd()  # Абсолютный путь
    try:
        os.makedirs(path_db)
    except OSError as exception:
        # Игнорируем ошибку "папка уже создана", но выводим все остальные
        if exception.errno != errno.EEXIST:
            mb.showerror("ОШИБКА!", exception)
            raise

    # if not os.path.exists('db'):  # Если на существует
    #    os.makedirs('db')
    #    print('Создана папка')

    # print(os.walk(path))
    # for dirs, folder, files in os.walk(path):
    #    print('Выбранный каталог: ', dirs)
    #    print('Вложенные папки: ', folder)
    #    print('Файлы в папке: ', files)
    #    print('\n')
    #    # Отобразит только корневую папку и остановит цикл
    #    break


class DB:
    """ Класс подвлючения к БД sqlite3 """
    def __init__(self):
        create_db_dir()  # Создаем папку для БД
        self.conn_sqlite3 = sqlite3.connect(path_db + '/' + 'company_manager.db')
        self.c_sqlite3 = self.conn_sqlite3.cursor()
        self.c_sqlite3.execute("PRAGMA foreign_keys=ON")  # Для каскадного удаления

        #################
        # Таблица roles #
        #################
        # ,CONSTRAINT role_name UNIQUE (role_name)
        try:
            self.c_sqlite3.execute(
                '''CREATE TABLE IF NOT EXISTS roles 
                (id_role integer primary key autoincrement not null
                ,role_name text not null
                ,role_description text
                ,user integer
                ,CONSTRAINT role_name UNIQUE (role_name)
                )'''
            )
            self.conn_sqlite3.commit()
        except sqlite3.Error as err:
            print('Ошибка: ' + err.__str__())

        #################
        # Таблица users #
        #################
        try:
            self.c_sqlite3.execute(
                '''CREATE TABLE IF NOT EXISTS users 
                (id_user integer primary key autoincrement not null
                ,user_login text not null
                ,user_password text
                ,user_name text
                ,user_description text
                ,is_deleted int default(0)
                ,CONSTRAINT user_login UNIQUE (user_login)
                )'''
            )
            self.conn_sqlite3.commit()
        except sqlite3.Error as err:
            print('Ошибка: ' + err.__str__())

        #######################
        # Таблица users_roles #
        #######################
        try:
            self.c_sqlite3.execute(
                '''CREATE TABLE IF NOT EXISTS users_roles 
                (id_users_roles integer primary key autoincrement not null
                ,id_user integer not null
                ,id_role integer not null
                ,FOREIGN KEY(id_user) REFERENCES users(id_user) ON DELETE CASCADE
                ,FOREIGN KEY(id_role) REFERENCES roles(id_role) ON DELETE CASCADE
                )'''
            )
            self.conn_sqlite3.commit()
        except sqlite3.Error as err:
            print('Ошибка: ' + err.__str__())

        #####################
        # Таблица companies #
        #####################
        """ Таблица компаний """
        try:
            self.c_sqlite3.execute(
                '''CREATE TABLE IF NOT EXISTS companies 
                (id_company integer primary key autoincrement not null
                ,company_name text not null
                ,company_description text
                )'''
            )
            self.conn_sqlite3.commit()
        except sqlite3.Error as err:
            print('Ошибка: ' + err.__str__())
            # self.root.destroy()
            # sys.exit()
            # raise SystemExit
            # exit()
            # ??? self.master.title("Оставить отзыв")
            # self.master.destroy()

        ############################
        # Таблица connection_types #
        ############################
        """ Таблица типов подключения """
        try:
            self.c_sqlite3.execute(
                '''CREATE TABLE IF NOT EXISTS connection_types 
                (id_connection_type integer primary key autoincrement not null
                ,connection_type_name text not null
                ,connection_type_description text
                )'''
            )
            self.conn_sqlite3.commit()
        except sqlite3.Error as err:
            mb.showerror("ОШИБКА!", err.__str__())
            # self.root.destroy()

        #######################
        # Таблица connections #
        #######################
        """ Таблица подключений """
        try:
            self.c_sqlite3.execute(
                '''CREATE TABLE IF NOT EXISTS connections 
                (id_connection integer primary key autoincrement not null
                ,id_company integer not null
                ,id_connection_type integer not null
                ,connection_ip text, connection_description text
                ,FOREIGN KEY(id_company) REFERENCES companies(id_company) ON DELETE CASCADE
                ,FOREIGN KEY(id_connection_type) REFERENCES connection_types(id_connection_type) ON DELETE CASCADE
                )'''
            )
            self.conn_sqlite3.commit()
        except sqlite3.Error as err:
            mb.showerror("ОШИБКА!", err.__str__())
            # self.root.destroy()

        ##################
        # Таблица logins #
        ##################
        """ Таблица логинов для подключения """
        try:
            self.c_sqlite3.execute(
                '''CREATE TABLE IF NOT EXISTS logins
                (id_login integer primary key autoincrement not null
                ,id_connection integer not null
                ,login_name text
                ,login_password text
                ,login_description text
                ,id_creator integer
                ,FOREIGN KEY(id_connection) REFERENCES connections(id_connection) ON DELETE CASCADE
                ,FOREIGN KEY(id_creator) REFERENCES users(id_user) ON DELETE SET NULL
                )'''
            )
            self.conn_sqlite3.commit()
        except sqlite3.Error as err:
            mb.showerror("ОШИБКА!", err.__str__())
            # self.root.destroy()

        # ###############################
        # # Таблица permission_by_users #
        # ###############################
        # """ Таблица прямых прав на пользователей """
        # try:
        #     self.c_sqlite3.execute(
        #         '''CREATE TABLE IF NOT EXISTS permission_by_users
        #         (id_permission_by_user integer primary key autoincrement not null
        #         ,id_login integer not null
        #         ,id_user integer not null
        #         ,FOREIGN KEY(id_login) REFERENCES logins(id_login) ON DELETE CASCADE
        #         ,FOREIGN KEY(id_user) REFERENCES users(id_user) ON DELETE CASCADE
        #         )'''
        #     )
        #     self.conn_sqlite3.commit()
        # except sqlite3.Error as err:
        #     mb.showerror("ОШИБКА!", err.__str__())
        #     # self.root.destroy()

        ###############################
        # Таблица permission_by_roles #
        ###############################
        """ Таблица прав через роли """
        try:
            self.c_sqlite3.execute(
                '''CREATE TABLE IF NOT EXISTS permission_by_roles
                (id_permission integer primary key autoincrement not null
                ,id_login integer not null
                ,id_role integer not null
                ,FOREIGN KEY(id_login) REFERENCES logins(id_login) ON DELETE CASCADE
                ,FOREIGN KEY(id_role) REFERENCES roles(id_role) ON DELETE CASCADE
                )'''
            )
            self.conn_sqlite3.commit()
        except sqlite3.Error as err:
            mb.showerror("ОШИБКА!", err.__str__())
            # self.root.destroy()

    # стиль qmark
    # curs.execute("SELECT weight FROM Equipment WHERE name = ? AND price = ?",
    #             ['lead', 24])

    # названный стиль
    # curs.execute("SELECT weight FROM Equipment WHERE name = :name AND price = :price",
    #         {name: 'lead', price: 24})

    # Именованные параметры
    # sql = "SELECT column FROM table WHERE col1=%s AND col2=%s"
    # params = (col1_value, col2_value)
    # cursor.execute(sql, params)

    # curs.execute("SELECT weight FROM Equipment WHERE name = :name AND price = :price",
    #         {name: 'lead', price: 24})

# # Множественная вствыка
# weekdays = ["Воскресенье", "Понедельник", "Вторник", "Среда",
#  "Четверг", "Пятница", "Суббота",
# "Воскресенье"]
#  import sqlite as db
#  c = db.connect(database="tvprogram")
#  cu = c.cursor()
#  cu.execute("""DELETE FROM wd;""")
#  cu.executemany("""INSERT INTO wd VALUES (%s, %s);""",
#  enumerate(weekdays))
#  c.commit()
#  c.close()


#    # пример 1
#    try:
#        cursor.execute("INSERT INTO ...", params)
#    except sqlite3.Error as err:
#        logger.error(err.message)

#    # пример 2
#    import sqlite3 as lite
#
#    con = lite.connect('test.db')
#
#    with con:
#        cur = con.cursor()
#        cur.execute("CREATE TABLE Persons(Id INT, Name TEXT)")
#        cur.execute("INSERT INTO Persons VALUES(1,'Joe')")
#        cur.execute("INSERT INTO Persons VALUES(1,'Jenny')")
#
#        try:
#            cur.execute("INSERT INTO Persons VALUES(1,'Jenny', 'Error')")
#            self.con.commit()
#
#        except lite.Error as er:
#            print
#            'er:', er.message
#
#        # Retrieve data
#        cur.execute("SELECT * FROM Persons")
#        rows = cur.fetchall()
#        for row in rows:
#            print
#            row
