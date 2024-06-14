import sqlite3

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn

def create_tables(conn):
    try:
        sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                            id integer PRIMARY KEY,
                                            name text NOT NULL,
                                            age integer,
                                            gender text,
                                            bio text
                                        ); """
        sql_create_interests_table = """ CREATE TABLE IF NOT EXISTS interests (
                                            id integer PRIMARY KEY,
                                            name text NOT NULL
                                        ); """
        sql_create_user_interests_table = """ CREATE TABLE IF NOT EXISTS user_interests (
                                                user_id integer NOT NULL,
                                                interest_id integer NOT NULL,
                                                PRIMARY KEY (user_id, interest_id),
                                                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
                                                FOREIGN KEY (interest_id) REFERENCES interests (id) ON DELETE CASCADE
                                            ); """
        conn.execute(sql_create_users_table)
        conn.execute(sql_create_interests_table)
        conn.execute(sql_create_user_interests_table)
    except sqlite3.Error as e:
        print(e)

def create_user(conn, user):
    sql = ''' INSERT INTO users(name, age, gender, bio)
              VALUES(?, ?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, user)
    conn.commit()
    return cur.lastrowid

def select_all_users(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    return rows

def update_user(conn, user):
    sql = ''' UPDATE users
              SET name = ? ,
                  age = ? ,
                  gender = ? ,
                  bio = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, user)
    conn.commit()

def delete_user(conn, id):
    sql = 'DELETE FROM users WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()

def create_interest(conn, interest):
    sql = ''' INSERT INTO interests(name)
              VALUES(?) '''
    cur = conn.cursor()
    cur.execute(sql, interest)
    conn.commit()
    return cur.lastrowid

def select_all_interests(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM interests")
    rows = cur.fetchall()
    return rows

def add_user_interest(conn, user_id, interest_id):
    sql = ''' INSERT INTO user_interests(user_id, interest_id)
              VALUES(?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, (user_id, interest_id))
    conn.commit()

def remove_user_interest(conn, user_id, interest_id):
    sql = 'DELETE FROM user_interests WHERE user_id=? AND interest_id=?'
    cur = conn.cursor()
    cur.execute(sql, (user_id, interest_id))
    conn.commit()

def get_user_interests(conn, user_id):
    cur = conn.cursor()
    cur.execute('''SELECT interests.name FROM interests
                   JOIN user_interests ON interests.id = user_interests.interest_id
                   WHERE user_interests.user_id = ?''', (user_id,))
    rows = cur.fetchall()
    return rows
