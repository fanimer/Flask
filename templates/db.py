import pymysql
if __name__ == '__main__':
    conn = pymysql.connect(host='localhost', user='root', password='123456', db='account')
    cursor = conn.cursor()
    cursor.execute('insert into userinfo(username, password) value (%s, %s)', ["123", "456"])
    conn.commit()
    #row = dict((cursor.description[idx][0], value) for idx, value in enumerate(res))
    cursor.close()
    conn.close()
