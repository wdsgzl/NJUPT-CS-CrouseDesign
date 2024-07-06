import sqlite3
conn = sqlite3.connect('../db.sqlite3')   #连接数据库
cur = conn.cursor()        #创建关联数据库的游标实例
cur.execute("select * from Tem")  #对T_fish表执行数据查找命令
for row in cur.fetchall():      #以一条记录为元组单位返回结果给row
     # temperature=row[2]
     # print(temperature)
     temperature=row[2]
     print(row)
     print(temperature)

cur.execute("select * from Lig")  #对T_fish表执行数据查找命令
for row in cur.fetchall():      #以一条记录为元组单位返回结果给row
     # lightness=row[2]
     # print(lightness)
     lightness=row[2]
     print(row)
     print(lightness)

cur.execute("select * from Dio")  #对T_fish表执行数据查找命令
for row in cur.fetchall():      #以一条记录为元组单位返回结果给row
     # CCOO=row[2]
     # print(CCOO)
     CCOO=row[2]
     print(row)
     print(CCOO)
conn.close()   #关闭数据库
