import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import sqlite3
import os
import datetime
from openpyxl import *

database_name = "202310.db"
table_name = "teacher_info"

# 用来连接数据库
conn = sqlite3.connect(database_name)
c = conn.cursor()

try:
    c.execute("select school_name,name,gender,id from teacher_info")
    raw_result = c.fetchall()

except Exception as e:
    print("执行mysql语句时报错：%s" % e)

finally:
    conn.commit()

print(raw_result)

result = []

for i in raw_result:
    result.append(list(i))

for i in range(0,len(result)):
    year = int(result[i][3][6:10])
    month = int(result[i][3][10:12])
    day = int(result[i][3][12:14])

    result[i].append(year)
    result[i].append(month)
    result[i].append(day)
    result[i].pop(3)

print(result)

while(True):
    target_date = input("请输入退休计算日期，格式如20230901或20220901-20230901\n")

    #这里是某一个时间节点前的退休统计
    if(target_date.__len__() == 8):

        target_year = int(target_date[0:4])
        target_month = int(target_date[4:6])
        target_day = int(target_date[6:8])

        print("截止年份" + str(target_year))
        print("截止月份" + str(target_month))
        print("截止日期" + str(target_day))

        # 男60女55

        retirement_list = []

        for i in range(0, len(result)):
            if (result[i][2] == "男"):
                if (result[i][3] + 60 < target_year or result[i][3] + 60 == target_year and result[i][
                    4] < target_month or result[i][3] + 60 == target_year and result[i][4] == target_month and
                        result[i][5] < target_day):
                    retirement_list.append(result[i])

            elif (result[i][2] == "女"):
                if (result[i][3] + 55 < target_year or result[i][3] + 55 == target_year and result[i][
                    4] < target_month or result[i][3] + 55 == target_year and result[i][4] == target_month and
                        result[i][5] < target_day):
                    retirement_list.append(result[i])

            else:
                print("有一个奇怪的性别:")
                print(result[i])

        print(retirement_list)
        print(len(retirement_list))

        wb = Workbook()

        # 取得当前活动worksheet对象
        ws = wb.active

        for row in retirement_list:
            ws.append(row)

        wb.save(r".\output\退休统计\公办在编人员退休退休名单（截止至" + str(target_date) + "）.xlsx")

        break


    #这里是时间范围统计
    elif(target_date.__len__() == 17):

        target_year_0 = int(target_date[0:4])
        target_month_0 = int(target_date[4:6])
        target_day_0 = int(target_date[6:8])

        print("开始年份" + str(target_year_0))
        print("开始月份" + str(target_month_0))
        print("开始日期" + str(target_day_0))

        target_year_1 = int(target_date[9:13])
        target_month_1 = int(target_date[13:15])
        target_day_1 = int(target_date[15:17])

        print("结束年份" + str(target_year_1))
        print("结束月份" + str(target_month_1))
        print("结束日期" + str(target_day_1))

        # 男60女55

        retirement_list = []

        for i in range(0, len(result)):
            if (result[i][2] == "男"):
                if ((result[i][3] + 60 < target_year_1 or result[i][3] + 60 == target_year_1 and result[i][
                    4] < target_month_1 or result[i][3] + 60 == target_year_1 and result[i][4] == target_month_1 and
                        result[i][5] < target_day_1) and (result[i][3] + 60 > target_year_0 or result[i][3] + 60 == target_year_0 and result[i][
                    4] > target_month_0 or result[i][3] + 60 == target_year_0 and result[i][4] == target_month_0 and
                        result[i][5] > target_day_0)):
                    retirement_list.append(result[i])

            elif (result[i][2] == "女"):
                if ((result[i][3] + 55 < target_year_1 or result[i][3] + 55 == target_year_1 and result[i][
                    4] < target_month_1 or result[i][3] + 55 == target_year_1 and result[i][4] == target_month_1 and
                        result[i][5] < target_day_1) and (result[i][3] + 55 > target_year_0 or result[i][3] + 55 == target_year_0 and result[i][
                    4] > target_month_0 or result[i][3] + 55 == target_year_0 and result[i][4] == target_month_0 and
                        result[i][5] > target_day_0)):
                    retirement_list.append(result[i])

            else:
                print("有一个奇怪的性别:")
                print(result[i])

        print(retirement_list)
        print(len(retirement_list))

        wb = Workbook()

        # 取得当前活动worksheet对象
        ws = wb.active

        for row in retirement_list:
            ws.append(row)

        wb.save(r".\output\退休统计\公办在编人员退休退休名单（从" + str(target_date[:8]) + "至" + str(target_date[9:]) + "）.xlsx")



        break

    else:
        print("长度为" + str(len(target_date)))
        target_date = ""
        print("请重新输入")



conn.close()