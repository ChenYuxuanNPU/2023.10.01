import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import sqlite3
import os
import verification_for_school_title


database_name = "202310.db"
table_name = "teacher_info"

# 用来连接数据库
conn = sqlite3.connect(database_name)
c = conn.cursor()

try:
    c.execute("select name,major_discipline from teacher_info where major_discipline like '%无%'")
    result = c.fetchall()

except Exception as e:
    print("执行mysql语句时报错：%s" % e)

finally:
    conn.commit()

print(result)
dic = {}
for i in range(0,len(result)):
    if(result[i][1] in dic):
        dic[result[i][1]] = dic[result[i][1]] + 1
    else:
        dic[result[i][1]] = 0

print(dic)

conn.close()