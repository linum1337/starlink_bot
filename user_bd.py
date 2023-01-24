import sqlite3
#bd_location = '/Users/vladislavcehov/PycharmProjects/starlink_bot/user_cookie.db'
bd_location = 'home/guest/starlink_bot/user_cookie.db'
def user_add(id, cookie, login, pwd):
    con = sqlite3.connect(bd_location)
    cursor = con.cursor()
    sqlite_insertion = """INSERT INTO user_data (user_id, cookie, login, pwd) VALUES (?, ?, ?, ?)"""
    insertion_data = (str(id), str(cookie), str(login), str(pwd))
    cursor.execute(sqlite_insertion, insertion_data)
    con.commit()
    cursor.close()

def user_search(id):
    con = sqlite3.connect(bd_location)
    cursor = con.cursor()
    get_all = """SELECT * FROM user_data"""
    cursor.execute(get_all)
    us_dat = cursor.fetchall()
    con.commit()
    cursor.close()
    if len(us_dat) != 0:
        for i in us_dat:
            print(i)
            if id in i:
                return (True, i[0], i[1], i[2], i[3])
    return (False, 'fuck it', 1, 1)

def delete_user(id):
    con = sqlite3.connect(bd_location)
    cursor = con.cursor()
    get_all = """DELETE FROM user_data WHERE user_id=(?)"""
    insertion = str(id)
    print(insertion)
    cursor.execute(get_all, (insertion, ))
    us_dat = cursor.fetchall()
    con.commit()
    cursor.close()