import sqlite3
from datetime import date
# 连接到SQLite数据库文件，如果不存在则创建它
conn = sqlite3.connect('../db.sqlite3')

# 创建一个游标对象
cursor = conn.cursor()

#cursor.execute("Drop TABLE Lig")
cursor.execute("CREATE TABLE Lig(device varchar,time varchar,Lightness FLOAT,status bool)")


conn.commit()
conn.close()

