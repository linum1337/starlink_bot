import sqlite3

def user_add(id, cookie):
    con = sqlite3.connect('/Users/vladislavcehov/PycharmProjects/starlink_bot/user_cookie.db')
    cursor = con.cursor()
    sqlite_insertion = """INSERT INTO user_data (user_id, cookie) VALUES (?, ?)"""
    insertion_data = (str(id), str(cookie))
    cursor.execute(sqlite_insertion, insertion_data)
    con.commit()
    cursor.close()

def user_search(id, cookie):
    con = sqlite3.connect('/Users/vladislavcehov/PycharmProjects/starlink_bot/user_cookie.db')
    cursor = con.cursor()
    bd_parse =cursor.execute(""" SELECT * FROM * """)
    print(bd_parse)
    con.commit()
    cursor.close()
