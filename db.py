import psycopg2
database_url = "postgresql://postgres:postgres@localhost/postgres"

def execute_query(query, select=False):
    conn = None
    try:
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        cursor.execute(query)
        if select:
            rows = cursor.fetchall()
        cursor.close()
        conn.commit()
        if select:
            return rows
    except:
        print('Ошибка при работе с PostgreSQL')
    finally:
        if conn is not None:
            conn.close()

def registration(login, password):
    execute_query(f"insert into users (login, password) values ('{login}','{password}')")

def authorization(login, password):
    user = execute_query(f"select * from users where login = '{login}' and password = '{password}'")
    if user:
        return True
    return False


def getLoginUser(login):
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()
    cursor.execute("select * from users where login = '"+login+"'")
    if cursor.fetchone():
        return True
    return False

def getUser(login):
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()
    cursor.execute("select * from users where login = '" + login + "'")
    return cursor.fetchone()

def updatePassword(password, login):
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()
    cursor.execute("update users set password = '"+password+"' where login = '"+login+"'")
    conn.commit()