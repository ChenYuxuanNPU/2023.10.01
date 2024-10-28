import openpyxl
import sqlite3


# 确定收集的数据表
wb = openpyxl.load_workbook('source/验证表.xlsx', data_only=True)
sheet = wb["Sheet"]

# 获取表格数据
result = []
for row in sheet.iter_rows(values_only=True):
    result.append(row)

database_name = "202310.db"
table_name = "teacher_info"

# 用来连接数据库
result_database = []
conn = sqlite3.connect(database_name)
c = conn.cursor()

try:
    c.execute("select name,id,current_level,school_name from teacher_info")
    result_database = c.fetchall()

except Exception as e:
    print("执行mysql语句时报错：%s" % e)

finally:
    conn.commit()

print("采集来的人数有：")
print(result_database.__len__())
print("工资系统的人数有：")
print(result.__len__())

name_list = []
id_list = []

for i in result_database:
    name_list.append(i[0])

for i in result_database:
    id_list.append(i[1])

none_list = []
wrong_id_list = []

for i in range(0,len(result)):
    if(not result[i][1] in id_list and "x" not in result[i][1] and "X" not in result[i][1]):
        none_list.append(result[i])

print(none_list.__len__())

flag = 0
del_list = []


for i in range(0,len(none_list)):
    if(none_list[i][0] not in name_list):
        pass
    else:
        wrong_id_list.append(none_list[i])
        del_list.append(i)


for i in range(0,len(del_list)):

    del none_list[del_list[0]]

    del del_list[0]

    for k in range(0,len(del_list)):
        del_list[k] = del_list[k] - 1

print(none_list.__len__())
print(wrong_id_list.__len__())

name_list = []

for i in result:
    name_list.append(i[0])

extra_list = []

for i in range(0,len(result_database)):
    if(result_database[i][0] not in name_list):
        extra_list.append(result_database[i])

print(extra_list)






