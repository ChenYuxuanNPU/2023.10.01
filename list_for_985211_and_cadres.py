import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import sqlite3
import os
import datetime
import shutil
import gc
import verification_for_school_title
from openpyxl import *
from openpyxl.styles import Font


conn = sqlite3.connect("202310.db")
c = conn.cursor()

if __name__ == '__main__':
    try:
        c.execute(
            "select school_name,name,graduate_school,graduate_school_id,degree,current_administrative_position from teacher_info where current_administrative_position != '无' and degree != '无' order by case current_administrative_position when '党组织书记' then 1 when '党组织书记兼校长' then 2 when '正校级' then 3 when '副校级' then 4 when '中层正职' then 5 when '中层副职' then 6 else 7 end")
        result = c.fetchall()

    except Exception as e:
        print("执行mysql语句时报错：%s" % e)

    finally:
        conn.commit()

    #print(result)

    #print(len(result))


    result_done = []
    list_985 = []
    list_211 = []
    list_affiliate = []
    list_else = []

    for i in result:
        result_done.append(list(i))
        #print(i)

    #print(len(result_done))

    list_all = []

    for i in range(0,len(result_done)):
        if(result_done[i][3] in verification_for_school_title.code_of_985):
            list_985.append(result_done[i])
            result_done[i].append("985")

        if (result_done[i][3] in verification_for_school_title.code_of_affiliate):
            list_affiliate.append(result_done[i])
            result_done[i].append("部属师范")

        if (result_done[i][3] in verification_for_school_title.code_of_211):
            list_211.append(result_done[i])
            result_done[i].append("211")

        if(result_done[i][3] not in verification_for_school_title.code_of_985 and result_done[i][3] not in verification_for_school_title.code_of_211 and result_done[i][3] not in verification_for_school_title.code_of_affiliate):
            list_else.append(result_done[i])

    for i in result_done:
        if(int(len(i)) > 6):
            #print(i)
            pass

    list_done = []
    for single_data in result_done:
        if (int(len(single_data)) > 6):
            single_data.pop(3)
            list_done.append(single_data)

    for i in list_done:
        # print(i,file=file)
        pass

    wb = Workbook()

    # 取得当前活动worksheet对象
    ws = wb.active

    for row in list_done:
        ws.append(row)

    wb.save("1.xlsx")