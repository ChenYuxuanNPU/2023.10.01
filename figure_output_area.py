import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import sqlite3
import os
import datetime
import shutil
import update_database
import generation_of_input_data
import verification_for_school_title
import gc
import pyecharts.options as opts
from pyecharts.charts import Line
from pyecharts.faker import Faker
from pyecharts.charts import Bar
from pyecharts.charts import Pie
from pyecharts.commons.utils import JsCode
from pyecharts.charts import Page
from bs4 import BeautifulSoup
from pyecharts.globals import ThemeType

# 设置字体为楷体
matplotlib.rcParams['font.sans-serif'] = ['KaiTi']

# 设定数据库与表名
database_name = update_database.database_name
table_name = update_database.table_name

# 设置指导中心
area_list = ["江高", "永平", "钟落潭", "新市", "太和", "人和", "石井"]
area_name = "江高"

# area_list = ['石井']
# area_name = '石井'


# 用全局变量保存查数据库的结果，避免多次查询
result_for_educational_background = []
label_for_educational_background = []
data_for_educational_background = []

result_for_highest_title = []
label_for_highest_title = []
data_for_highest_title = []

result_for_current_age = []
label_for_current_age = []
data_for_current_age = []

result_for_major_discipline = []
label_for_major_discipline = []
data_for_major_discipline = []

result_for_school_title = []
label_for_school_title = []
data_for_school_title = []

result_for_cadre_teacher = []
label_for_cadre_teacher = []
data_for_cadre_teacher = []

result_for_title_01 = []
label_for_title_01 = []
data_for_title_01 = []

result_for_area_of_supporting_education = []
label_for_area_of_supporting_education = []
data_for_area_of_supporting_education = []

result_for_current_administrative_position = []
label_for_current_administrative_position = []
data_for_current_administrative_position = []

result_for_different_period = []

# 用来设置文件名
current_time = datetime.datetime.now().strftime('%Y-%m-%d')
save_path = r".\output\search_by_area" + '\\' + current_time + '\\' + area_name

# 用来设置排序
educational_background_order = {'高中及以下': 1, '高中': 2, '中专': 3, "大学专科": 4, "大学本科": 5, "硕士研究生": 6,
                                "博士研究生": 7, None: 8}
highest_title_order = {'未取得职称': 1, '三级教师': 2, '二级教师': 3, '一级教师': 4, '高级教师': 5, '正高级教师': 6,
                       '初级职称（非中小学系列）': 7, '中级职称（非中小学系列）': 8, '高级职称（非中小学系列）': 9, None: 10}


# 用来设置合适的柱状图竖轴高度
def set_axis_height(max_input):
    if (len(str(max_input)) == 1):
        axis_height = 10

    elif (len(str(max_input)) == 2):
        for i in range(0, 100000, 5):
            if (i > max_input):
                axis_height = i + 1
                break

    elif (len(str(max_input)) == 3):
        for i in range(0, 100000, 50):
            if (i > max_input):
                axis_height = i + 10
                break

    elif (len(str(max_input)) == 4):
        for i in range(0, 100000, 500):
            if (i > max_input):
                axis_height = i + 100
                break

    elif (len(str(max_input)) == 5):
        for i in range(0, 100000, 5000):
            if (i > max_input):
                axis_height = i + 1000
                break

    else:
        axis_height = max_input

    return axis_height


###
###下面做的是学历统计相关的图表
###

def log_for_educational_background(label, data):
    print("学历统计数据：", file=file)

    for i in range(0, len(data)):
        print(str(label[i]) + ":" + str(data[i]) + "人，占比" + str(round(100 * data[i] / sum(data), 1)) + "%",
              file=file)

    print("", file=file)


def figure_for_educational_background_00():
    global result_for_educational_background
    global label_for_educational_background
    global data_for_educational_background

    try:
        c.execute(
            "select count(*),educational_background_highest from " + table_name + " where area = '" + area_name + "' group by educational_background_highest order by count(*) desc")
        result_for_educational_background = c.fetchall()

    except Exception as e:
        print("执行mysql语句时报错：%s" % e)

    finally:
        conn.commit()

    result_for_educational_background = sorted(result_for_educational_background,
                                               key=lambda x: educational_background_order[x[1]])

    print(result_for_educational_background)

    data_for_educational_background = []
    label_for_educational_background = []
    for single_data in result_for_educational_background:
        if (single_data[1] != None and single_data[1] != "无"):
            label_for_educational_background.append(single_data[1])
            data_for_educational_background.append(single_data[0])

    axis_height = set_axis_height(max(data_for_educational_background))

    fig, ax = plt.subplots(figsize=(16, 8), tight_layout=True)
    bar_container = ax.bar(label_for_educational_background, data_for_educational_background)
    ax.set(ylabel='人数', title='全区教师学历统计', ylim=(0, axis_height))
    ax.bar_label(bar_container)

    plt.savefig(save_path + "\\学历分布图\学历分布图_00.svg", format="svg")
    plt.savefig(save_path + "\\学历分布图\学历分布图_00.jpg", dpi=500)
    # plt.show()
    plt.close()

    log_for_educational_background(label=label_for_educational_background, data=data_for_educational_background)


def figure_for_educational_background_01():
    data = []
    label = []
    for single_data in result_for_educational_background:
        if (single_data[1] != None and single_data[1] != "无"):
            label.append(single_data[1])
            data.append(single_data[0])

    fig, ax = plt.subplots(figsize=(9, 6), subplot_kw=dict(aspect="equal"))

    def func(pct, allvals):
        absolute = int(np.round(pct / 100. * np.sum(allvals)))
        return f"{pct:.1f}%\n({absolute:d})"

    wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data),
                                      textprops=dict(color="w"))

    ax.legend(wedges, label,
              title="学历类别",
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1))

    plt.setp(autotexts, size=8, weight="bold")

    ax.set_title("全区教师学历分布_01")
    plt.savefig(save_path + "\\学历分布图\学历分布图_01.svg", format="svg")
    plt.savefig(save_path + "\\学历分布图\学历分布图_01.jpg", dpi=500)
    # plt.show()
    plt.close()


def figure_for_educational_background_02():
    data = []
    label = []
    for single_data in result_for_educational_background:
        if (single_data[1] != None and single_data[1] != "无"):
            label.append(single_data[1])
            data.append(single_data[0])

    fig, ax = plt.subplots()
    ax.pie(data, labels=label, autopct='%1.1f%%')
    plt.title("全区教师学历分布_02")
    plt.savefig(save_path + "\\学历分布图\学历分布图_02.svg", format="svg")
    plt.savefig(save_path + "\\学历分布图\学历分布图_02.jpg", dpi=500)
    # plt.show()
    plt.close()


###
###下面做的是职称统计相关的图表
###

def log_for_highest_title(label, data):
    print("职称统计数据：", file=file)

    for i in range(0, len(data)):
        print(str(label[i]) + ":" + str(data[i]) + "人，占比" + str(round(100 * data[i] / sum(data), 1)) + "%",
              file=file)

    print("", file=file)


def figure_for_highest_title_00():
    global result_for_highest_title
    global label_for_highest_title
    global data_for_highest_title

    try:
        c.execute(
            "select count(*),highest_title from " + table_name + " where area = '" + area_name + "' group by highest_title order by count(*) desc")
        result_for_highest_title = c.fetchall()

    except Exception as e:
        print("执行mysql语句时报错：%s" % e)

    finally:
        conn.commit()

    result_for_highest_title.sort(key=lambda x: highest_title_order[x[1]])

    print(result_for_highest_title)

    data_for_highest_title = []
    label_for_highest_title = []
    for single_data in result_for_highest_title:
        if (single_data[1] != None and single_data[1] != "无"):
            label_for_highest_title.append(single_data[1])
            data_for_highest_title.append(single_data[0])

    axis_height = set_axis_height(max(data_for_highest_title))

    # 这里有可能出现标签为空的，注意检查
    # print("data:")
    # print(data)
    # print("label:")
    # print(label)

    fig, ax = plt.subplots(figsize=(16, 8), tight_layout=True)
    bar_container = ax.bar(label_for_highest_title, data_for_highest_title)
    ax.set(ylabel='人数', title='全区教师职称统计', ylim=(0, axis_height))
    ax.bar_label(bar_container)

    plt.savefig(save_path + "\\职称分布图\职称分布图_00.svg", format="svg")
    plt.savefig(save_path + "\\职称分布图\职称分布图_00.jpg", dpi=500)
    # plt.show()
    plt.close()

    log_for_highest_title(label=label_for_highest_title, data=data_for_highest_title)


def figure_for_highest_title_01():
    data = []
    label = []
    for single_data in result_for_highest_title:
        if (single_data[1] != None and single_data[1] != "无"):
            label.append(single_data[1])
            data.append(single_data[0])

    fig, ax = plt.subplots(figsize=(10, 6), subplot_kw=dict(aspect="equal"))

    def func(pct, allvals):
        absolute = int(np.round(pct / 100. * np.sum(allvals)))
        return f"{pct:.1f}%\n({absolute:d})"

    wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data),
                                      textprops=dict(color="w"))

    ax.legend(wedges, label,
              title="职称类别",
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1))

    plt.setp(autotexts, size=8, weight="bold")

    ax.set_title("全区教师职称分布_01")
    plt.savefig(save_path + "\\职称分布图\职称分布图_01.svg", format="svg")
    plt.savefig(save_path + "\\职称分布图\职称分布图_01.jpg", dpi=500)
    # plt.show()
    plt.close()


def figure_for_highest_title_02():
    label = []
    data = []
    for single_data in result_for_highest_title:
        if (single_data[1] != None and single_data[1] != "无"):
            label.append(single_data[1])
            data.append(single_data[0])

    fig, ax = plt.subplots()
    ax.pie(data, labels=label, autopct='%1.1f%%')
    plt.title("全区教师职称分布_02")
    plt.savefig(save_path + "\\职称分布图\职称分布图_02.svg", format="svg")
    plt.savefig(save_path + "\\职称分布图\职称分布图_02.jpg", dpi=500)
    # plt.show()
    plt.close()


###
###下面做的是年龄统计相关的图表
###

def log_for_current_age(label, data, avg_age):
    print("年龄统计数据：", file=file)

    for i in range(0, len(data)):
        print(str(label[i]) + ":" + str(data[i]) + "人，占比" + str(round(100 * data[i] / sum(data), 1)) + "%",
              file=file)

    print(area_name + "公办在编教师平均年龄为" + str(avg_age) + "岁", file=file)

    print("", file=file)


def figure_for_current_age_00():
    global result_for_current_age
    global label_for_current_age
    global data_for_current_age

    try:
        c.execute(
            "select count(*),current_age from " + table_name + " where area = '" + area_name + "' group by current_age order by current_age asc")
        result_for_current_age = c.fetchall()

    except Exception as e:
        print("执行mysql语句时报错：%s" % e)

    finally:
        conn.commit()

    print(result_for_current_age)

    ###
    # 这部分代码用来统计平均年龄
    avg_age = 0
    teacher_number = 0
    for data1 in result_for_current_age:
        if (data1[1] != '#VALUE!' and data1[1] != '#NUM!' and data1[1] != None and data1[1] != "无"):
            avg_age = avg_age + int(data1[0]) * int(data1[1])
            teacher_number = teacher_number + data1[0]

    avg_age = round(avg_age / teacher_number, 1)
    print(area_name + "公办在编教师平均年龄为" + str(avg_age) + "岁")
    ###

    label_for_current_age = ["25岁以下", "25-29岁", "30-34岁", "35-39岁", "40-44岁", "45-49岁", "50-54岁", "55岁及以上"]
    data_for_current_age = [0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(0, len(result_for_current_age)):

        if (result_for_current_age[i][1] == '#VALUE!'):
            print("数据库中有非法年龄值")
            continue

        elif (result_for_current_age[i][1] == '#NUM!'):
            print("数据库中有非法年龄值")
            continue

        elif (result_for_current_age[i][1] == None):
            print("数据库中有空值")
            continue

        elif (int(result_for_current_age[i][1]) < 25):
            data_for_current_age[0] = data_for_current_age[0] + result_for_current_age[i][0]

        elif (int(result_for_current_age[i][1]) >= 25 and int(result_for_current_age[i][1]) < 30):
            data_for_current_age[1] = data_for_current_age[1] + result_for_current_age[i][0]

        elif (int(result_for_current_age[i][1]) >= 30 and int(result_for_current_age[i][1]) < 35):
            data_for_current_age[2] = data_for_current_age[2] + result_for_current_age[i][0]

        elif (int(result_for_current_age[i][1]) >= 35 and int(result_for_current_age[i][1]) < 40):
            data_for_current_age[3] = data_for_current_age[3] + result_for_current_age[i][0]

        elif (int(result_for_current_age[i][1]) >= 40 and int(result_for_current_age[i][1]) < 45):
            data_for_current_age[4] = data_for_current_age[4] + result_for_current_age[i][0]

        elif (int(result_for_current_age[i][1]) >= 45 and int(result_for_current_age[i][1]) < 50):
            data_for_current_age[5] = data_for_current_age[5] + result_for_current_age[i][0]

        elif (int(result_for_current_age[i][1]) >= 50 and int(result_for_current_age[i][1]) < 55):
            data_for_current_age[6] = data_for_current_age[6] + result_for_current_age[i][0]

        elif (int(result_for_current_age[i][1]) >= 55):
            data_for_current_age[7] = data_for_current_age[7] + result_for_current_age[i][0]

    log_for_current_age(label=label_for_current_age, data=data_for_current_age, avg_age=avg_age)

    # 用来删除数值为0的信息，不用于作图
    temp = []
    for i in range(0, len(data_for_current_age)):
        if (data_for_current_age[i] == 0):
            temp.append(i)

    for change_index, delete_index in enumerate(temp):
        delete_index -= change_index
        del data_for_current_age[delete_index]
        del label_for_current_age[delete_index]

    axis_height = set_axis_height(max(data_for_current_age))

    fig, ax = plt.subplots(figsize=(16, 8), tight_layout=True)
    bar_container = ax.bar(label_for_current_age, data_for_current_age)
    ax.set(ylabel='人数', title='全区教师年龄统计', ylim=(0, axis_height))
    ax.bar_label(bar_container)

    plt.savefig(save_path + "\\年龄分布图\年龄分布图_00.svg", format="svg")
    plt.savefig(save_path + "\\年龄分布图\年龄分布图_00.jpg", dpi=500)
    # plt.show()
    plt.close()


def figure_for_current_age_01():
    label = ["25岁以下", "25-29岁", "30-34岁", "35-39岁", "40-44岁", "45-49岁", "50-54岁", "55岁及以上"]
    data = [0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(0, len(result_for_current_age)):

        if (result_for_current_age[i][1] == '#VALUE!'):
            print("数据库中有非法年龄值")
            continue

        elif (result_for_current_age[i][1] == '#NUM!'):
            print("数据库中有非法年龄值")
            continue

        elif (result_for_current_age[i][1] == None):
            print("数据库中有空值")
            continue

        elif (int(result_for_current_age[i][1]) < 25):
            data[0] = data[0] + result_for_current_age[i][0]

        elif (int(result_for_current_age[i][1]) >= 25 and int(result_for_current_age[i][1]) < 30):
            data[1] = data[1] + result_for_current_age[i][0]

        elif (int(result_for_current_age[i][1]) >= 30 and int(result_for_current_age[i][1]) < 35):
            data[2] = data[2] + result_for_current_age[i][0]

        elif (int(result_for_current_age[i][1]) >= 35 and int(result_for_current_age[i][1]) < 40):
            data[3] = data[3] + result_for_current_age[i][0]

        elif (int(result_for_current_age[i][1]) >= 40 and int(result_for_current_age[i][1]) < 45):
            data[4] = data[4] + result_for_current_age[i][0]

        elif (int(result_for_current_age[i][1]) >= 45 and int(result_for_current_age[i][1]) < 50):
            data[5] = data[5] + result_for_current_age[i][0]

        elif (int(result_for_current_age[i][1]) >= 50 and int(result_for_current_age[i][1]) < 55):
            data[6] = data[6] + result_for_current_age[i][0]

        elif (int(result_for_current_age[i][1]) >= 55):
            data[7] = data[7] + result_for_current_age[i][0]

    # 用来删除数值为0的信息，不用于作图
    temp = []
    for i in range(0, len(data)):
        if (data[i] == 0):
            temp.append(i)

    for change_index, delete_index in enumerate(temp):
        delete_index -= change_index
        del data[delete_index]
        del label[delete_index]

    fig, ax = plt.subplots(figsize=(9, 6), subplot_kw=dict(aspect="equal"))

    def func(pct, allvals):
        absolute = int(np.round(pct / 100. * np.sum(allvals)))
        return f"{pct:.1f}%\n({absolute:d})"

    wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data),
                                      textprops=dict(color="w"))

    ax.legend(wedges, label,
              title="年龄范围",
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1))

    plt.setp(autotexts, size=8, weight="bold")

    ax.set_title("全区教师年龄分布_01")
    plt.savefig(save_path + "\\年龄分布图\年龄分布图_01.svg", format="svg")
    plt.savefig(save_path + "\\年龄分布图\年龄分布图_01.jpg", dpi=500)
    # plt.show()
    plt.close()


def figure_for_current_age_02():
    label = ["25岁以下", "25-29岁", "30-34岁", "35-39岁", "40-44岁", "45-49岁", "50-54岁", "55岁及以上"]
    data = [0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(0, len(result_for_current_age)):

        if (result_for_current_age[i][1] == '#VALUE!'):
            print("数据库中有非法年龄值")
            continue

        elif (result_for_current_age[i][1] == '#NUM!'):
            print("数据库中有非法年龄值")
            continue

        elif (result_for_current_age[i][1] == None):
            print("数据库中有空值")
            continue

        elif (int(result_for_current_age[i][1]) < 25):
            data[0] = data[0] + result_for_current_age[i][0]

        elif (int(result_for_current_age[i][1]) >= 25 and int(result_for_current_age[i][1]) < 30):
            data[1] = data[1] + result_for_current_age[i][0]

        elif (int(result_for_current_age[i][1]) >= 30 and int(result_for_current_age[i][1]) < 35):
            data[2] = data[2] + result_for_current_age[i][0]

        elif (int(result_for_current_age[i][1]) >= 35 and int(result_for_current_age[i][1]) < 40):
            data[3] = data[3] + result_for_current_age[i][0]

        elif (int(result_for_current_age[i][1]) >= 40 and int(result_for_current_age[i][1]) < 45):
            data[4] = data[4] + result_for_current_age[i][0]

        elif (int(result_for_current_age[i][1]) >= 45 and int(result_for_current_age[i][1]) < 50):
            data[5] = data[5] + result_for_current_age[i][0]

        elif (int(result_for_current_age[i][1]) >= 50 and int(result_for_current_age[i][1]) < 55):
            data[6] = data[6] + result_for_current_age[i][0]

        elif (int(result_for_current_age[i][1]) >= 55):
            data[7] = data[7] + result_for_current_age[i][0]

    # 用来删除数值为0的信息，不用于作图
    temp = []
    for i in range(0, len(data)):
        if (data[i] == 0):
            temp.append(i)

    for change_index, delete_index in enumerate(temp):
        delete_index -= change_index
        del data[delete_index]
        del label[delete_index]

    fig, ax = plt.subplots()
    ax.pie(data, labels=label, autopct='%1.1f%%')
    plt.title("全区教师年龄分布_02")
    plt.savefig(save_path + "\\年龄分布图\年龄分布图_02.svg", format="svg")
    plt.savefig(save_path + "\\年龄分布图\年龄分布图_02.jpg", dpi=500)
    # plt.show()
    plt.close()


###
###下面做的是主教学科相关的统计图表
###

def log_for_major_discipline(label, data):
    print("学科统计数据：", file=file)

    for i in range(0, len(data)):
        print("主教" + str(label[i]) + "的教师:" + str(data[i]) + "人，占比" + str(
            round(100 * data[i] / sum(data_for_major_discipline), 1)) + "%", file=file)

    print("", file=file)


def figure_for_major_discipline_00():
    global result_for_major_discipline
    global label_for_major_discipline
    global data_for_major_discipline

    try:
        c.execute(
            "select count(*),major_discipline from " + table_name + " where area = '" + area_name + "' and major_discipline is not null and major_discipline not like '%无%' group by major_discipline order by count(*) desc limit 20")
        result_for_major_discipline = c.fetchall()

    except Exception as e:
        print("执行mysql语句时报错：%s" % e)

    finally:
        conn.commit()

    print(result_for_major_discipline)

    data_for_major_discipline = []
    label_for_major_discipline = []
    for single_data in result_for_major_discipline:
        if (single_data[1] != None and single_data[1] != "无"):
            label_for_major_discipline.append(single_data[1])
            data_for_major_discipline.append(single_data[0])

    axis_height = set_axis_height(max(data_for_major_discipline))

    fig, ax = plt.subplots(figsize=(16, 8), tight_layout=True)
    bar_container = ax.bar(label_for_major_discipline, data_for_major_discipline)
    ax.set(ylabel='人数', title='全区教师主教学科统计', ylim=(0, axis_height))
    ax.bar_label(bar_container)

    plt.savefig(save_path + "\\学科分布图\学科分布图_00.svg", format="svg")
    plt.savefig(save_path + "\\学科分布图\学科分布图_00.jpg", dpi=500)
    # plt.show()
    plt.close()

    log_for_major_discipline(label=label_for_major_discipline, data=data_for_major_discipline)


def figure_for_major_discipline_01():
    data = []
    label = []
    for single_data in result_for_major_discipline:
        if (single_data[1] != None and single_data[1] != "无"):
            label.append(single_data[1])
            data.append(single_data[0])

    fig, ax = plt.subplots(figsize=(9, 6), subplot_kw=dict(aspect="equal"))

    def func(pct, allvals):
        absolute = int(np.round(pct / 100. * np.sum(allvals)))
        return f"{pct:.1f}%\n({absolute:d})"

    wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data),
                                      textprops=dict(color="w"))

    ax.legend(wedges, label,
              title="学科类别",
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1))

    plt.setp(autotexts, size=8, weight="bold")

    ax.set_title("全区教师学科分布_01")
    plt.savefig(save_path + "\\学科分布图\学科分布图_01.svg", format="svg")
    plt.savefig(save_path + "\\学科分布图\学科分布图_01.jpg", dpi=500)
    # plt.show()
    plt.close()


def figure_for_major_discipline_02():
    label = []
    data = []

    for single_data in result_for_major_discipline:
        if (single_data[1] != None and single_data[1] != "无"):
            label.append(single_data[1])
            data.append(single_data[0])

    fig, ax = plt.subplots()
    ax.pie(data, labels=label, autopct='%1.1f%%')
    plt.title("全区教师学科分布_02")
    plt.savefig(save_path + "\\学科分布图\学科分布图_02.svg", format="svg")
    plt.savefig(save_path + "\\学科分布图\学科分布图_02.jpg", dpi=500)
    # plt.show()
    plt.close()


###
###下面做的是985、211、部属师范高校统计的相关图表
###

def log_for_school_title(label, data):
    print("毕业院校统计数据：", file=file)

    for i in range(0, len(data)):
        print("毕业于" + str(label[i]) + "的教师:" + str(data[i]) + "人，占比" + str(
            round(100 * data[i] / sum(data), 1)) + "%", file=file)

    print("", file=file)


def figure_for_school_title_00():
    global result_for_school_title
    global label_for_school_title
    global data_for_school_title

    try:
        c.execute(
            "select graduate_school_id from " + table_name + " where (educational_background = '大学本科' or educational_background = '硕士研究生' or educational_background = '博士研究生') and area = '" + area_name + "'")
        # "select graduate_school_id from " + table_name + " where area = '" + area_name + "'"
        result_for_school_title = c.fetchall()

    except Exception as e:
        print("执行mysql语句时报错：%s" % e)

    finally:
        conn.commit()

    counts_for_others = 0
    counts_for_985 = 0
    counts_for_211 = 0
    counts_for_affiliate = 0

    for word in result_for_school_title:
        if str(word[0]) in verification_for_school_title.code_of_985:
            counts_for_985 = counts_for_985 + 1

        if str(word[0]) in verification_for_school_title.code_of_211:
            counts_for_211 = counts_for_211 + 1

        if str(word[0]) in verification_for_school_title.code_of_affiliate:
            counts_for_affiliate = counts_for_affiliate + 1

        if (str(word[0]) not in verification_for_school_title.code_of_985 + verification_for_school_title.code_of_211 + verification_for_school_title.code_of_affiliate):
            counts_for_others = counts_for_others + 1

    label_for_school_title = ['其他院校', '211院校', '985院校', '部属师范院校']
    data_for_school_title = [counts_for_others, counts_for_211, counts_for_985, counts_for_affiliate]

    print([(counts_for_others, "其他院校"), (counts_for_211, "211院校"), (counts_for_985, "985院校"),
           (counts_for_affiliate, "部属师范院校")])

    log_for_school_title(label=label_for_school_title, data=data_for_school_title)

    # 用来删除数值为0的信息，不用于作图
    temp = []
    for i in range(0, len(data_for_school_title)):
        if (data_for_school_title[i] == 0):
            print(area_name + "不存在毕业院校为" + str(label_for_school_title[i]) + "的教师")
            temp.append(i)

    for change_index, delete_index in enumerate(temp):
        delete_index -= change_index
        del data_for_school_title[delete_index]
        del label_for_school_title[delete_index]

    axis_height = set_axis_height(max(data_for_school_title))

    fig, ax = plt.subplots()
    bar_container = ax.bar(label_for_school_title, data_for_school_title)
    ax.set(ylabel='人数', title='全区教师毕业院校统计', ylim=(0, axis_height))
    ax.bar_label(bar_container)

    plt.savefig(save_path + "\\毕业院校分布图\毕业院校分布图.svg", format="svg")
    plt.savefig(save_path + "\\毕业院校分布图\毕业院校分布图.jpg", dpi=500)
    # plt.show()
    plt.close()


###
###这里统计骨干教师数量
###

def log_for_cadre_teacher(label, data):
    print("骨干教师统计数据：", file=file)

    for i in range(0, len(data)):
        print(str(label[i]) + ":" + str(data[i]) + "人，占比" + str(round(100 * data[i] / sum(data), 1)) + "%",
              file=file)

    print("", file=file)


def figure_for_cadre_teacher_00():
    global result_for_cadre_teacher
    global label_for_cadre_teacher
    global data_for_cadre_teacher

    try:
        c.execute(
            "select count(*),cadre_teacher from " + table_name + " where area = '" + area_name + "' group by cadre_teacher order by case cadre_teacher when '无' then 1 when '其他' then 2 when '白云区骨干教师' then 3 when '广州市骨干教师' then 4 when '广东省骨干教师' then 5 else 6 end")
        result_for_cadre_teacher = c.fetchall()

    except Exception as e:
        print("执行mysql语句时报错：%s" % e)

    finally:
        conn.commit()

    print(result_for_cadre_teacher)

    data_for_cadre_teacher = []
    label_for_cadre_teacher = []
    for single_data in result_for_cadre_teacher:
        if (single_data[1] != None):
            label_for_cadre_teacher.append(single_data[1])
            data_for_cadre_teacher.append(single_data[0])

    axis_height = set_axis_height(max(data_for_cadre_teacher))

    fig, ax = plt.subplots(figsize=(10, 6), tight_layout=True)
    bar_container = ax.bar(label_for_cadre_teacher, data_for_cadre_teacher)
    ax.set(ylabel='人数', title='全区骨干教师统计', ylim=(0, axis_height))
    ax.bar_label(bar_container)

    plt.savefig(save_path + "\\骨干教师统计图\骨干教师统计图_00.svg", format="svg")
    plt.savefig(save_path + "\\骨干教师统计图\骨干教师统计图_00.jpg", dpi=500)
    # plt.show()
    plt.close()

    log_for_cadre_teacher(label=label_for_cadre_teacher, data=data_for_cadre_teacher)


def figure_for_cadre_teacher_01():
    data = []
    label = []
    for single_data in result_for_cadre_teacher:
        if (single_data[1] != None):
            label.append(single_data[1])
            data.append(single_data[0])

    fig, ax = plt.subplots(figsize=(9, 6), subplot_kw=dict(aspect="equal"))

    def func(pct, allvals):
        absolute = int(np.round(pct / 100. * np.sum(allvals)))
        return f"{pct:.1f}%\n({absolute:d})"

    wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data),
                                      textprops=dict(color="w"))

    ax.legend(wedges, label,
              title="骨干教师级别",
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1))

    plt.setp(autotexts, size=8, weight="bold")

    ax.set_title("全区骨干教师统计_01")
    plt.savefig(save_path + "\\骨干教师统计图\骨干教师统计图_01.svg", format="svg")
    plt.savefig(save_path + "\\骨干教师统计图\骨干教师统计图_01.jpg", dpi=500)
    # plt.show()
    plt.close()


def figure_for_cadre_teacher_02():
    label = []
    data = []

    for single_data in result_for_cadre_teacher:
        if (single_data[1] != None):
            label.append(single_data[1])
            data.append(single_data[0])

    fig, ax = plt.subplots()
    ax.pie(data, labels=label, autopct='%1.1f%%')
    plt.title("全区骨干教师统计_02")
    plt.savefig(save_path + "\\骨干教师统计图\骨干教师统计图_02.svg", format="svg")
    plt.savefig(save_path + "\\骨干教师统计图\骨干教师统计图_02.jpg", dpi=500)
    # plt.show()
    plt.close()


###
###这里做三名工作室统计
###

def figure_for_title_01_00():
    global result_for_title_01
    global label_for_title_01
    global data_for_title_01

    try:
        c.execute(
            "select(select count(*) from " + table_name + " where area = '" + area_name + "'), (select count(*) from " + table_name + " where area = '" + area_name + "' and title_01 != '无')")
        result_for_title_01 = c.fetchall()

    except Exception as e:
        print("执行mysql语句时报错：%s" % e)

    finally:
        conn.commit()

    print("三名工作室主持人数：" + str(result_for_title_01[0][1]))
    # 输出三名文档
    print("三名工作室主持人数：" + str(result_for_title_01[0][1]) + "，占比" + str(
        round(100 * result_for_title_01[0][1] / result_for_title_01[0][0], 1)) + "%", file=file)
    print("", file=file)

    label_for_title_01 = ["三名工作室主持人", "无"]
    data_for_title_01 = [result_for_title_01[0][1], result_for_title_01[0][0] - result_for_title_01[0][1]]

    fig, ax = plt.subplots(figsize=(9, 6), subplot_kw=dict(aspect="equal"))

    def func(pct, allvals):
        absolute = int(np.round(pct / 100. * np.sum(allvals)))
        return f"{pct:.1f}%\n({absolute:d})"

    wedges, texts, autotexts = ax.pie(data_for_title_01, autopct=lambda pct: func(pct, data_for_title_01),
                                      textprops=dict(color="w"))

    ax.legend(wedges, label_for_title_01,
              title="三名工作室主持人统计",
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1))

    plt.setp(autotexts, size=8, weight="bold")

    ax.set_title("三名工作室主持人统计")
    plt.savefig(save_path + "\\三名统计图\三名统计图_01.svg", format="svg")
    plt.savefig(save_path + "\\三名统计图\三名统计图_01.jpg", dpi=500)
    # plt.show()
    plt.close()


###
###这里做支教统计数据
###

def log_for_area_of_supporting_education(label, data):
    print("支教统计数据：", file=file)

    for i in range(0, len(data)):

        if (label[i] != "无"):
            print("在" + str(label[i]) + "支教的教师:" + str(data[i]) + "人，占比" + str(
                round(100 * data[i] / sum(data), 1)) + "%", file=file)

        else:
            print("无支教经历的教师：" + str(data[i]) + "人，占比" + str(round(100 * data[i] / sum(data), 1)) + "%",
                  file=file)

    print("", file=file)


def figure_for_area_of_supporting_education_00():
    global result_for_area_of_supporting_education
    global label_for_area_of_supporting_education
    global data_for_area_of_supporting_education

    try:
        c.execute(
            "select count(*),area_of_supporting_education from " + table_name + " where area = '" + area_name + "' group by area_of_supporting_education order by case area_of_supporting_education when '片内' then 1 when '区内' then 2 when '外市' then 3 when '外省' then 4 when '无' then 5 else 6 end")
        result_for_area_of_supporting_education = c.fetchall()

    except Exception as e:
        print("执行mysql语句时报错：%s" % e)

    finally:
        conn.commit()

    print(result_for_area_of_supporting_education)

    data_for_area_of_supporting_education = []
    label_for_area_of_supporting_education = []
    for single_data in result_for_area_of_supporting_education:
        if (single_data[1] != None):
            label_for_area_of_supporting_education.append(single_data[1])
            data_for_area_of_supporting_education.append(single_data[0])

    axis_height = set_axis_height(max(data_for_area_of_supporting_education))

    fig, ax = plt.subplots(figsize=(10, 6), tight_layout=True)
    bar_container = ax.bar(label_for_area_of_supporting_education, data_for_area_of_supporting_education)
    ax.set(ylabel='人数', title='全区支教教师统计', ylim=(0, axis_height))
    ax.bar_label(bar_container)

    plt.savefig(save_path + "\\支教统计图\支教统计图_00.svg", format="svg")
    plt.savefig(save_path + "\\支教统计图\支教统计图_00.jpg", dpi=500)
    # plt.show()
    plt.close()

    log_for_area_of_supporting_education(label=label_for_area_of_supporting_education,
                                         data=data_for_area_of_supporting_education)


###
###这里统计现任行政职务的数量
###

def log_for_current_administrative_position(label, data):
    print("行政职务统计数据：", file=file)

    for i in range(0, len(data)):
        print(str(label[i]) + ":" + str(data[i]) + "人，占比" + str(round(100 * data[i] / sum(data), 1)) + "%",
              file=file)

    print("", file=file)


def figure_for_current_administrative_position_00():
    global result_for_current_administrative_position
    global label_for_current_administrative_position
    global data_for_current_administrative_position

    try:
        c.execute(
            "select count(*),current_administrative_position from " + table_name + " where area = '" + area_name + "' group by current_administrative_position order by case current_administrative_position when '无' then 1 when '中层副职' then 2 when '中层正职' then 3 when '副校级' then 4 when '正校级' then 5 when '党组织书记兼校长' then 6 when '党组织书记' then 7 else 8 end")
        result_for_current_administrative_position = c.fetchall()

    except Exception as e:
        print("执行mysql语句时报错：%s" % e)

    finally:
        conn.commit()

    print(result_for_current_administrative_position)

    data_for_current_administrative_position = []
    label_for_current_administrative_position = []
    for single_data in result_for_current_administrative_position:
        if (single_data[1] != None):
            label_for_current_administrative_position.append(single_data[1])
            data_for_current_administrative_position.append(single_data[0])

    axis_height = set_axis_height(max(data_for_current_administrative_position))

    fig, ax = plt.subplots(figsize=(10, 6), tight_layout=True)
    bar_container = ax.bar(label_for_current_administrative_position, data_for_current_administrative_position)
    ax.set(ylabel='人数', title='现任行政职务统计', ylim=(0, axis_height))
    ax.bar_label(bar_container)

    plt.savefig(save_path + "\\现任行政职务统计图\现任行政职务统计图_00.svg", format="svg")
    plt.savefig(save_path + "\\现任行政职务统计图\现任行政职务统计图_00.jpg", dpi=500)
    # plt.show()
    plt.close()

    log_for_current_administrative_position(label=label_for_current_administrative_position,
                                            data=data_for_current_administrative_position)


###
###这里做的是不同学段的学科、年龄、学历统计
###
def log_for_different_period(label, data):
    print("不同学段教师统计数据：", file=file)

    for i in range(0, len(label) - 1):
        print(str(label[i]) + "教师人数：" + str(data[i]) + "，占比" + str(round(100 * data[i] / sum(data), 1)) + "%",
              file=file)

    print("", file=file)


def figure_for_different_period_00():
    global result_for_different_period
    result_for_different_period = []

    try:
        c.execute(
            "select period,major_discipline,current_age,educational_background from " + table_name + " where area = '" + area_name + "'")
        result_tem = c.fetchall()
        print(result_tem)

    except Exception as e:
        print("执行mysql语句时报错：%s" % e)

    finally:
        conn.commit()

    # 从数据库读出来的是元组，不能修改，所以用全局列表存可以修改的数据
    for i in range(0, len(result_tem)):
        result_for_different_period.append([result_tem[i][0], result_tem[i][1], result_tem[i][2], result_tem[i][3]])

    data = [0, 0, 0, 0, 0, 0]
    label = ["高中", "初中", "中职", "小学", "幼儿园", "其他"]

    # print(result_for_different_period)

    for i in range(0, len(result_for_different_period)):
        # print(result[i][0])
        if (result_for_different_period[i][0] == "高中"):
            data[0] = data[0] + 1
        elif (result_for_different_period[i][0] == "初中"):
            data[1] = data[1] + 1
        elif (result_for_different_period[i][0] == "中职"):
            data[2] = data[2] + 1
        elif (result_for_different_period[i][0] == "小学"):
            data[3] = data[3] + 1
        elif (result_for_different_period[i][0] == "幼儿园"):
            data[4] = data[4] + 1
        elif (result_for_different_period[i][0] == "其他"):
            data[5] = data[5] + 1
        else:
            data[5] = data[5] + 1
            # print("还有这些归到其他类的奇怪数据：" + result_for_different_period[i][0])
            result_for_different_period[i][0] = label[5]

    log_for_different_period(label=label, data=data)

    print("修理好的数据示例：" + str(result_for_different_period[0]))
    print(area_name)
    # print(result_for_different_period)

    axis_height = set_axis_height(max(data))

    for i in range(0, len(data)):
        print((label[i], data[i]))

    fig, ax = plt.subplots(figsize=(10, 6), tight_layout=True)
    bar_container = ax.bar(label, data)
    ax.set(ylabel='人数', title='全区学段教师统计', ylim=(0, axis_height))
    ax.bar_label(bar_container)

    plt.savefig(save_path + "\\学段统计图\学段统计图_00.svg", format="svg")
    plt.savefig(save_path + "\\学段统计图\学段统计图_00.jpg", dpi=500)
    # plt.show()
    plt.close()


def draw_figure_for_major_discipline_AND_high_school(stat_for_high_school):
    print("高中学科教师统计原始数据：")
    print(stat_for_high_school)

    list_temp = []

    for major_discipline, number in stat_for_high_school.items():
        list_temp.append([number, major_discipline])

    print(list_temp)
    list_temp.sort(key=lambda x1: x1[0], reverse=True)

    data = []
    label = []

    for single_data in list_temp:
        label.append(single_data[1])
        data.append(single_data[0])
        if (len(label) > 20):
            break

    axis_height = set_axis_height(max(data))

    fig, ax = plt.subplots(figsize=(16, 8), tight_layout=True)
    bar_container = ax.bar(label, data)
    ax.set(ylabel='人数', title='全区高中教师学科统计', ylim=(0, axis_height))
    ax.bar_label(bar_container)

    plt.savefig(save_path + "\\学段统计图\高中\学科统计_00.svg", format="svg")
    plt.savefig(save_path + "\\学段统计图\高中\学科统计_00.jpg", dpi=500)
    # plt.show()
    plt.close()


def draw_figure_for_major_discipline_AND_middle_school(stat_for_middle_school):
    print("初中学科教师统计原始数据：")
    print(stat_for_middle_school)
    list_temp = []

    for major_discipline, number in stat_for_middle_school.items():
        list_temp.append([number, major_discipline])

    print(list_temp)
    list_temp.sort(key=lambda x1: x1[0], reverse=True)

    data = []
    label = []

    for single_data in list_temp:
        label.append(single_data[1])
        data.append(single_data[0])
        if (len(label) > 20):
            break

    axis_height = set_axis_height(max(data))

    fig, ax = plt.subplots(figsize=(16, 8), tight_layout=True)
    bar_container = ax.bar(label, data)
    ax.set(ylabel='人数', title='全区初中教师学科统计', ylim=(0, axis_height))
    ax.bar_label(bar_container)
    plt.savefig(save_path + "\\学段统计图\初中\学科统计_00.svg", format="svg")
    plt.savefig(save_path + "\\学段统计图\初中\学科统计_00.jpg", dpi=500)
    # plt.show()
    plt.close()


def draw_figure_for_major_discipline_AND_vocational_school(stat_for_vocational_school):
    print("中职学科教师统计原始数据：")
    print(stat_for_vocational_school)

    list_temp = []

    for major_discipline, number in stat_for_vocational_school.items():
        list_temp.append([number, major_discipline])

    print(list_temp)
    list_temp.sort(key=lambda x1: x1[0], reverse=True)

    data = []
    label = []

    for single_data in list_temp:
        label.append(single_data[1])
        data.append(single_data[0])
        if (len(label) > 20):
            break

    axis_height = set_axis_height(max(data))

    fig, ax = plt.subplots(figsize=(16, 8), tight_layout=True)
    bar_container = ax.bar(label, data)
    ax.set(ylabel='人数', title='全区中职教师学科统计', ylim=(0, axis_height))
    ax.bar_label(bar_container)

    plt.savefig(save_path + "\\学段统计图\中职\学科统计_00.svg", format="svg")
    plt.savefig(save_path + "\\学段统计图\中职\学科统计_00.jpg", dpi=500)
    # plt.show()
    plt.close()


def draw_figure_for_major_discipline_AND_primary_school(stat_for_primary_school):
    print("小学学科教师统计原始数据：")
    print(stat_for_primary_school)

    list_temp = []

    for major_discipline, number in stat_for_primary_school.items():
        list_temp.append([number, major_discipline])

    print(list_temp)
    list_temp.sort(key=lambda x1: x1[0], reverse=True)

    data = []
    label = []

    for single_data in list_temp:
        label.append(single_data[1])
        data.append(single_data[0])
        if (len(label) > 20):
            break

    axis_height = set_axis_height(max(data))

    fig, ax = plt.subplots(figsize=(16, 8), tight_layout=True)
    bar_container = ax.bar(label, data)
    ax.set(ylabel='人数', title='全区小学教师学科统计', ylim=(0, axis_height))
    ax.bar_label(bar_container)
    plt.savefig(save_path + "\\学段统计图\小学\学科统计_00.svg", format="svg")
    plt.savefig(save_path + "\\学段统计图\小学\学科统计_00.jpg", dpi=500)
    # plt.show()
    plt.close()


def figure_for_different_period_AND_major_discipline_00():
    print(result_for_different_period)

    stat_for_high_school = {}
    stat_for_middle_school = {}
    stat_for_vocational_school = {}
    stat_for_primary_school = {}
    stat_for_kindergarten = {}

    for single_data in result_for_different_period:
        if (single_data[0] != "其他"):

            if (single_data[0] == "高中"):
                if (single_data[1] in stat_for_high_school):
                    stat_for_high_school[single_data[1]] = stat_for_high_school[single_data[1]] + 1
                else:
                    stat_for_high_school[single_data[1]] = 1

            elif (single_data[0] == "初中"):
                if (single_data[1] in stat_for_middle_school):
                    stat_for_middle_school[single_data[1]] = stat_for_middle_school[single_data[1]] + 1
                else:
                    stat_for_middle_school[single_data[1]] = 1

            elif (single_data[0] == "中职"):
                if (single_data[1] in stat_for_vocational_school):
                    stat_for_vocational_school[single_data[1]] = stat_for_vocational_school[single_data[1]] + 1
                else:
                    stat_for_vocational_school[single_data[1]] = 1

            elif (single_data[0] == "小学"):
                if (single_data[1] in stat_for_primary_school):
                    stat_for_primary_school[single_data[1]] = stat_for_primary_school[single_data[1]] + 1
                else:
                    stat_for_primary_school[single_data[1]] = 1

            elif (single_data[0] == "幼儿园"):
                pass

            else:
                print("出现了奇怪的学段")

    # draw_figure_for_major_discipline_AND_high_school(stat_for_high_school)
    gc.collect()

    draw_figure_for_major_discipline_AND_middle_school(stat_for_middle_school)
    gc.collect()

    # draw_figure_for_major_discipline_AND_vocational_school(stat_for_vocational_school)
    gc.collect()

    draw_figure_for_major_discipline_AND_primary_school(stat_for_primary_school)
    gc.collect()


def draw_figure_for_current_age_AND_high_school(stat_for_high_school):
    print("高中年龄分布：")
    print(stat_for_high_school)

    data = [0, 0, 0, 0, 0, 0, 0, 0]
    label = ["25岁以下", "25-29岁", "30-34岁", "35-39岁", "40-44岁", "45-49岁", "50-54岁", "55岁及以上"]

    list_temp = []

    for current_age, number in stat_for_high_school.items():
        list_temp.append([number, current_age])

    print(list_temp)

    for single_data in list_temp:

        if (int(single_data[1]) < 25):
            data[0] = data[0] + int(single_data[0])

        elif (int(single_data[1]) >= 25 and int(single_data[1]) < 30):
            data[1] = data[1] + int(single_data[0])

        elif (int(single_data[1]) >= 30 and int(single_data[1]) < 35):
            data[2] = data[2] + int(single_data[0])

        elif (int(single_data[1]) >= 35 and int(single_data[1]) < 40):
            data[3] = data[3] + int(single_data[0])

        elif (int(single_data[1]) >= 40 and int(single_data[1]) < 45):
            data[4] = data[4] + int(single_data[0])

        elif (int(single_data[1]) >= 45 and int(single_data[1]) < 50):
            data[5] = data[5] + int(single_data[0])

        elif (int(single_data[1]) >= 50 and int(single_data[1]) < 55):
            data[6] = data[6] + int(single_data[0])

        elif (int(single_data[1]) >= 55):
            data[7] = data[7] + int(single_data[0])

        else:
            print("有一个奇怪的年龄：")
            print(single_data)

    for i in range(0, len(label)):
        print([label[i], data[i]])

    axis_height = set_axis_height(max(data))

    fig, ax = plt.subplots(figsize=(16, 8), tight_layout=True)
    bar_container = ax.bar(label, data)
    ax.set(ylabel='人数', title='全区高中教师年龄统计', ylim=(0, axis_height))
    ax.bar_label(bar_container)
    plt.savefig(save_path + "\\学段统计图\高中\年龄统计_00.svg", format="svg")
    plt.savefig(save_path + "\\学段统计图\高中\年龄统计_00.jpg", dpi=500)
    # plt.show()
    plt.close()


def draw_figure_for_current_age_AND_middle_school(stat_for_middle_school):
    print("初中年龄分布：")
    print(stat_for_middle_school)

    data = [0, 0, 0, 0, 0, 0, 0, 0]
    label = ["25岁以下", "25-29岁", "30-34岁", "35-39岁", "40-44岁", "45-49岁", "50-54岁", "55岁及以上"]

    list_temp = []

    for current_age, number in stat_for_middle_school.items():
        list_temp.append([number, current_age])

    print(list_temp)

    for single_data in list_temp:

        if (int(single_data[1]) < 25):
            data[0] = data[0] + int(single_data[0])

        elif (int(single_data[1]) >= 25 and int(single_data[1]) < 30):
            data[1] = data[1] + int(single_data[0])

        elif (int(single_data[1]) >= 30 and int(single_data[1]) < 35):
            data[2] = data[2] + int(single_data[0])

        elif (int(single_data[1]) >= 35 and int(single_data[1]) < 40):
            data[3] = data[3] + int(single_data[0])

        elif (int(single_data[1]) >= 40 and int(single_data[1]) < 45):
            data[4] = data[4] + int(single_data[0])

        elif (int(single_data[1]) >= 45 and int(single_data[1]) < 50):
            data[5] = data[5] + int(single_data[0])

        elif (int(single_data[1]) >= 50 and int(single_data[1]) < 55):
            data[6] = data[6] + int(single_data[0])

        elif (int(single_data[1]) >= 55):
            data[7] = data[7] + int(single_data[0])

        else:
            print("有一个奇怪的年龄：")
            print(single_data)

    for i in range(0, len(label)):
        print([label[i], data[i]])

    axis_height = set_axis_height(max(data))

    fig, ax = plt.subplots(figsize=(16, 8), tight_layout=True)
    bar_container = ax.bar(label, data)
    ax.set(ylabel='人数', title='全区初中教师年龄统计', ylim=(0, axis_height))
    ax.bar_label(bar_container)
    plt.savefig(save_path + "\\学段统计图\初中\年龄统计_00.svg", format="svg")
    plt.savefig(save_path + "\\学段统计图\初中\年龄统计_00.jpg", dpi=500)
    # plt.show()
    plt.close()


def draw_figure_for_current_age_AND_vocational_school(stat_for_vocational_school):
    print("中职年龄分布：")
    print(stat_for_vocational_school)

    data = [0, 0, 0, 0, 0, 0, 0, 0]
    label = ["25岁以下", "25-29岁", "30-34岁", "35-39岁", "40-44岁", "45-49岁", "50-54岁", "55岁及以上"]

    list_temp = []

    for current_age, number in stat_for_vocational_school.items():
        list_temp.append([number, current_age])

    print(list_temp)

    for single_data in list_temp:

        if (int(single_data[1]) < 25):
            data[0] = data[0] + int(single_data[0])

        elif (int(single_data[1]) >= 25 and int(single_data[1]) < 30):
            data[1] = data[1] + int(single_data[0])

        elif (int(single_data[1]) >= 30 and int(single_data[1]) < 35):
            data[2] = data[2] + int(single_data[0])

        elif (int(single_data[1]) >= 35 and int(single_data[1]) < 40):
            data[3] = data[3] + int(single_data[0])

        elif (int(single_data[1]) >= 40 and int(single_data[1]) < 45):
            data[4] = data[4] + int(single_data[0])

        elif (int(single_data[1]) >= 45 and int(single_data[1]) < 50):
            data[5] = data[5] + int(single_data[0])

        elif (int(single_data[1]) >= 50 and int(single_data[1]) < 55):
            data[6] = data[6] + int(single_data[0])

        elif (int(single_data[1]) >= 55):
            data[7] = data[7] + int(single_data[0])

        else:
            print("有一个奇怪的年龄：")
            print(single_data)

    for i in range(0, len(label)):
        print([label[i], data[i]])

    axis_height = set_axis_height(max(data))

    fig, ax = plt.subplots(figsize=(16, 8), tight_layout=True)
    bar_container = ax.bar(label, data)
    ax.set(ylabel='人数', title='全区中职教师年龄统计', ylim=(0, axis_height))
    ax.bar_label(bar_container)
    plt.savefig(save_path + "\\学段统计图\中职\年龄统计_00.svg", format="svg")
    plt.savefig(save_path + "\\学段统计图\中职\年龄统计_00.jpg", dpi=500)
    # plt.show()
    plt.close()


def draw_figure_for_current_age_AND_primary_school(stat_for_primary_school):
    print("小学年龄分布：")
    print(stat_for_primary_school)

    data = [0, 0, 0, 0, 0, 0, 0, 0]
    label = ["25岁以下", "25-29岁", "30-34岁", "35-39岁", "40-44岁", "45-49岁", "50-54岁", "55岁及以上"]

    list_temp = []

    for current_age, number in stat_for_primary_school.items():
        list_temp.append([number, current_age])

    print(list_temp)

    for single_data in list_temp:

        if (int(single_data[1]) < 25):
            data[0] = data[0] + int(single_data[0])

        elif (int(single_data[1]) >= 25 and int(single_data[1]) < 30):
            data[1] = data[1] + int(single_data[0])

        elif (int(single_data[1]) >= 30 and int(single_data[1]) < 35):
            data[2] = data[2] + int(single_data[0])

        elif (int(single_data[1]) >= 35 and int(single_data[1]) < 40):
            data[3] = data[3] + int(single_data[0])

        elif (int(single_data[1]) >= 40 and int(single_data[1]) < 45):
            data[4] = data[4] + int(single_data[0])

        elif (int(single_data[1]) >= 45 and int(single_data[1]) < 50):
            data[5] = data[5] + int(single_data[0])

        elif (int(single_data[1]) >= 50 and int(single_data[1]) < 55):
            data[6] = data[6] + int(single_data[0])

        elif (int(single_data[1]) >= 55):
            data[7] = data[7] + int(single_data[0])

        else:
            print("有一个奇怪的年龄：")
            print(single_data)

    for i in range(0, len(label)):
        print([label[i], data[i]])

    axis_height = set_axis_height(max(data))

    fig, ax = plt.subplots(figsize=(16, 8), tight_layout=True)
    bar_container = ax.bar(label, data)
    ax.set(ylabel='人数', title='全区小学教师年龄统计', ylim=(0, axis_height))
    ax.bar_label(bar_container)
    plt.savefig(save_path + "\\学段统计图\小学\年龄统计_00.svg", format="svg")
    plt.savefig(save_path + "\\学段统计图\小学\年龄统计_00.jpg", dpi=500)
    # plt.show()
    plt.close()


def draw_figure_for_current_age_AND_kindergarten(stat_for_kindergarten):
    print("幼儿园年龄分布：")
    print(stat_for_kindergarten)

    data = [0, 0, 0, 0, 0, 0, 0, 0]
    label = ["25岁以下", "25-29岁", "30-34岁", "35-39岁", "40-44岁", "45-49岁", "50-54岁", "55岁及以上"]

    list_temp = []

    for current_age, number in stat_for_kindergarten.items():
        list_temp.append([number, current_age])

    print(list_temp)

    for single_data in list_temp:

        if (int(single_data[1]) < 25):
            data[0] = data[0] + int(single_data[0])

        elif (int(single_data[1]) >= 25 and int(single_data[1]) < 30):
            data[1] = data[1] + int(single_data[0])

        elif (int(single_data[1]) >= 30 and int(single_data[1]) < 35):
            data[2] = data[2] + int(single_data[0])

        elif (int(single_data[1]) >= 35 and int(single_data[1]) < 40):
            data[3] = data[3] + int(single_data[0])

        elif (int(single_data[1]) >= 40 and int(single_data[1]) < 45):
            data[4] = data[4] + int(single_data[0])

        elif (int(single_data[1]) >= 45 and int(single_data[1]) < 50):
            data[5] = data[5] + int(single_data[0])

        elif (int(single_data[1]) >= 50 and int(single_data[1]) < 55):
            data[6] = data[6] + int(single_data[0])

        elif (int(single_data[1]) >= 55):
            data[7] = data[7] + int(single_data[0])

        else:
            print("有一个奇怪的年龄：")
            print(single_data)

    for i in range(0, len(label)):
        print([label[i], data[i]])

    axis_height = set_axis_height(max(data))

    fig, ax = plt.subplots(figsize=(16, 8), tight_layout=True)
    bar_container = ax.bar(label, data)
    ax.set(ylabel='人数', title='全区幼儿园教师年龄统计', ylim=(0, axis_height))
    ax.bar_label(bar_container)
    plt.savefig(save_path + "\\学段统计图\幼儿园\年龄统计_00.svg", format="svg")
    plt.savefig(save_path + "\\学段统计图\幼儿园\年龄统计_00.jpg", dpi=500)
    # plt.show()
    plt.close()


def figure_for_different_period_AND_current_age_00():
    print(result_for_different_period)
    stat_for_high_school = {}
    stat_for_middle_school = {}
    stat_for_vocational_school = {}
    stat_for_primary_school = {}
    stat_for_kindergarten = {}

    for single_data in result_for_different_period:
        if (single_data[0] != "其他"):

            if (single_data[0] == "高中"):
                if (single_data[2] in stat_for_high_school):
                    stat_for_high_school[single_data[2]] = stat_for_high_school[single_data[2]] + 1
                else:
                    stat_for_high_school[single_data[2]] = 1

            elif (single_data[0] == "初中"):
                if (single_data[2] in stat_for_middle_school):
                    stat_for_middle_school[single_data[2]] = stat_for_middle_school[single_data[2]] + 1
                else:
                    stat_for_middle_school[single_data[2]] = 1

            elif (single_data[0] == "中职"):
                if (single_data[2] in stat_for_vocational_school):
                    stat_for_vocational_school[single_data[2]] = stat_for_vocational_school[single_data[2]] + 1
                else:
                    stat_for_vocational_school[single_data[2]] = 1

            elif (single_data[0] == "小学"):
                if (single_data[2] in stat_for_primary_school):
                    stat_for_primary_school[single_data[2]] = stat_for_primary_school[single_data[2]] + 1
                else:
                    stat_for_primary_school[single_data[2]] = 1

            elif (single_data[0] == "幼儿园"):
                if (single_data[2] in stat_for_kindergarten):
                    stat_for_kindergarten[single_data[2]] = stat_for_kindergarten[single_data[2]] + 1
                else:
                    stat_for_kindergarten[single_data[2]] = 1

            else:
                print("出现了奇怪的学段")

    # draw_figure_for_current_age_AND_high_school(stat_for_high_school)
    gc.collect()

    draw_figure_for_current_age_AND_middle_school(stat_for_middle_school)
    gc.collect()

    # draw_figure_for_current_age_AND_vocational_school(stat_for_vocational_school)
    gc.collect()

    draw_figure_for_current_age_AND_primary_school(stat_for_primary_school)
    gc.collect()

    draw_figure_for_current_age_AND_kindergarten(stat_for_kindergarten)
    gc.collect()


def draw_figure_for_educational_background_AND_high_school(stat_for_high_school):
    print("高中学历统计原始数据：")
    print(stat_for_high_school)

    list_temp = []

    for educational_background, number in stat_for_high_school.items():
        list_temp.append([number, educational_background])

    print(list_temp)

    list_reorder = sorted(list_temp, key=lambda x: educational_background_order[x[1]])

    print("高中list_reorder:")
    print(list_reorder)

    data = []
    label = []

    for single_data in list_reorder:
        data.append(single_data[0])
        label.append(single_data[1])

    axis_height = set_axis_height(max(data))

    fig, ax = plt.subplots(figsize=(16, 8), tight_layout=True)
    bar_container = ax.bar(label, data)
    ax.set(ylabel='人数', title='全区高中教师学历统计', ylim=(0, axis_height))
    ax.bar_label(bar_container)
    plt.savefig(save_path + "\\学段统计图\高中\学历统计_00.svg", format="svg")
    plt.savefig(save_path + "\\学段统计图\高中\学历统计_00.jpg", dpi=500)
    # plt.show()
    plt.close()


def draw_figure_for_educational_background_AND_middle_school(stat_for_middle_school):
    print("初中学历统计原始数据：")
    print(stat_for_middle_school)

    list_temp = []

    for educational_background, number in stat_for_middle_school.items():
        list_temp.append([number, educational_background])

    print(list_temp)

    list_reorder = sorted(list_temp, key=lambda x: educational_background_order[x[1]])

    print("初中list_reorder:")
    print(list_reorder)

    data = []
    label = []

    for single_data in list_reorder:
        data.append(single_data[0])
        label.append(single_data[1])

    axis_height = set_axis_height(max(data))

    fig, ax = plt.subplots(figsize=(16, 8), tight_layout=True)
    bar_container = ax.bar(label, data)
    ax.set(ylabel='人数', title='全区初中教师学历统计', ylim=(0, axis_height))
    ax.bar_label(bar_container)
    plt.savefig(save_path + "\\学段统计图\初中\学历统计_00.svg", format="svg")
    plt.savefig(save_path + "\\学段统计图\初中\学历统计_00.jpg", dpi=500)
    # plt.show()
    plt.close()


def draw_figure_for_educational_background_AND_vocational_school(stat_for_vocational_school):
    print("中职学历统计原始数据：")
    print(stat_for_vocational_school)

    list_temp = []

    for educational_background, number in stat_for_vocational_school.items():
        list_temp.append([number, educational_background])

    print(list_temp)

    list_reorder = sorted(list_temp, key=lambda x: educational_background_order[x[1]])

    print("中职list_reorder:")
    print(list_reorder)

    data = []
    label = []

    for single_data in list_reorder:
        data.append(single_data[0])
        label.append(single_data[1])

    axis_height = set_axis_height(max(data))

    fig, ax = plt.subplots(figsize=(16, 8), tight_layout=True)
    bar_container = ax.bar(label, data)
    ax.set(ylabel='人数', title='全区中职教师学历统计', ylim=(0, axis_height))
    ax.bar_label(bar_container)
    plt.savefig(save_path + "\\学段统计图\中职\学历统计_00.svg", format="svg")
    plt.savefig(save_path + "\\学段统计图\中职\学历统计_00.jpg", dpi=500)
    # plt.show()
    plt.close()


def draw_figure_for_educational_background_AND_primary_school(stat_for_primary_school):
    print("小学学历统计原始数据：")
    print(stat_for_primary_school)

    list_temp = []

    for educational_background, number in stat_for_primary_school.items():
        list_temp.append([number, educational_background])

    print(list_temp)

    list_reorder = sorted(list_temp, key=lambda x: educational_background_order[x[1]])

    print("小学list_reorder:")
    print(list_reorder)

    data = []
    label = []

    for single_data in list_reorder:
        data.append(single_data[0])
        label.append(single_data[1])

    axis_height = set_axis_height(max(data))

    fig, ax = plt.subplots(figsize=(16, 8), tight_layout=True)
    bar_container = ax.bar(label, data)
    ax.set(ylabel='人数', title='全区小学教师学历统计', ylim=(0, axis_height))
    ax.bar_label(bar_container)
    plt.savefig(save_path + "\\学段统计图\小学\学历统计_00.svg", format="svg")
    plt.savefig(save_path + "\\学段统计图\小学\学历统计_00.jpg", dpi=500)
    # plt.show()
    plt.close()


def draw_figure_for_educational_background_AND_kindergarten(stat_for_kindergarten):
    print("幼儿园学历统计原始数据：")
    print(stat_for_kindergarten)

    list_temp = []

    for educational_background, number in stat_for_kindergarten.items():
        list_temp.append([number, educational_background])

    print(list_temp)

    list_reorder = sorted(list_temp, key=lambda x: educational_background_order[x[1]])

    print("幼儿园list_reorder:")
    print(list_reorder)

    data = []
    label = []

    for single_data in list_reorder:
        data.append(single_data[0])
        label.append(single_data[1])

    axis_height = set_axis_height(max(data))

    fig, ax = plt.subplots(figsize=(16, 8), tight_layout=True)
    bar_container = ax.bar(label, data)
    ax.set(ylabel='人数', title='全区幼儿园教师学历统计', ylim=(0, axis_height))
    ax.bar_label(bar_container)
    plt.savefig(save_path + "\\学段统计图\幼儿园\学历统计_00.svg", format="svg")
    plt.savefig(save_path + "\\学段统计图\幼儿园\学历统计_00.jpg", dpi=500)
    # plt.show()
    plt.close()


def figure_for_different_period_AND_educational_background_00():
    print(result_for_different_period)
    stat_for_high_school = {}
    stat_for_middle_school = {}
    stat_for_vocational_school = {}
    stat_for_primary_school = {}
    stat_for_kindergarten = {}

    for single_data in result_for_different_period:
        if (single_data[0] != "其他"):

            if (single_data[0] == "高中"):
                if (single_data[3] in stat_for_high_school):
                    stat_for_high_school[single_data[3]] = stat_for_high_school[single_data[3]] + 1
                else:
                    stat_for_high_school[single_data[3]] = 1

            elif (single_data[0] == "初中"):
                if (single_data[3] in stat_for_middle_school):
                    stat_for_middle_school[single_data[3]] = stat_for_middle_school[single_data[3]] + 1
                else:
                    stat_for_middle_school[single_data[3]] = 1

            elif (single_data[0] == "中职"):
                if (single_data[3] in stat_for_vocational_school):
                    stat_for_vocational_school[single_data[3]] = stat_for_vocational_school[single_data[3]] + 1
                else:
                    stat_for_vocational_school[single_data[3]] = 1

            elif (single_data[0] == "小学"):
                if (single_data[3] in stat_for_primary_school):
                    stat_for_primary_school[single_data[3]] = stat_for_primary_school[single_data[3]] + 1
                else:
                    stat_for_primary_school[single_data[3]] = 1

            elif (single_data[0] == "幼儿园"):
                if (single_data[3] in stat_for_kindergarten):
                    stat_for_kindergarten[single_data[3]] = stat_for_kindergarten[single_data[3]] + 1
                else:
                    stat_for_kindergarten[single_data[3]] = 1

            else:
                print("出现了奇怪的学段")

    # draw_figure_for_educational_background_AND_high_school(stat_for_high_school)
    gc.collect()

    draw_figure_for_educational_background_AND_middle_school(stat_for_middle_school)
    gc.collect()

    # draw_figure_for_educational_background_AND_vocational_school(stat_for_vocational_school)
    gc.collect()

    draw_figure_for_educational_background_AND_primary_school(stat_for_primary_school)
    gc.collect()

    draw_figure_for_educational_background_AND_kindergarten(stat_for_kindergarten)
    gc.collect()


def call_update_database():
    # 更新数据库
    os.system(r'python .\update_database.py')


def update_folder():
    global save_path

    save_path = r".\output\search_by_area" + '\\' + current_time + '\\' + area_name

    print(save_path)

    if (os.path.exists(r".\output\search_by_area" + '\\' + current_time)):
        pass
    else:
        os.mkdir(r".\output\search_by_area" + '\\' + current_time)

    if (os.path.exists(save_path)):
        shutil.rmtree(save_path)
        os.mkdir(save_path)
        os.mkdir(save_path + "\\学历分布图")
        os.mkdir(save_path + "\\职称分布图")
        os.mkdir(save_path + "\\年龄分布图")
        os.mkdir(save_path + "\\学科分布图")
        os.mkdir(save_path + "\\毕业院校分布图")
        os.mkdir(save_path + "\\骨干教师统计图")
        os.mkdir(save_path + "\\学段统计图")
        os.mkdir(save_path + "\\三名统计图")
        os.mkdir(save_path + "\\支教统计图")
        os.mkdir(save_path + "\\现任行政职务统计图")
        os.mkdir(save_path + "\\学段统计图\\高中")
        os.mkdir(save_path + "\\学段统计图\\初中")
        os.mkdir(save_path + "\\学段统计图\\中职")
        os.mkdir(save_path + "\\学段统计图\\小学")
        os.mkdir(save_path + "\\学段统计图\\幼儿园")
        print("文件夹已更新")
    else:
        os.mkdir(save_path)
        os.mkdir(save_path + "\\学历分布图")
        os.mkdir(save_path + "\\职称分布图")
        os.mkdir(save_path + "\\年龄分布图")
        os.mkdir(save_path + "\\学科分布图")
        os.mkdir(save_path + "\\毕业院校分布图")
        os.mkdir(save_path + "\\骨干教师统计图")
        os.mkdir(save_path + "\\学段统计图")
        os.mkdir(save_path + "\\三名统计图")
        os.mkdir(save_path + "\\支教统计图")
        os.mkdir(save_path + "\\现任行政职务统计图")
        os.mkdir(save_path + "\\学段统计图\\高中")
        os.mkdir(save_path + "\\学段统计图\\初中")
        os.mkdir(save_path + "\\学段统计图\\中职")
        os.mkdir(save_path + "\\学段统计图\\小学")
        os.mkdir(save_path + "\\学段统计图\\幼儿园")
        print("已创建新文件夹")


def draw_charts():
    gc.collect()

    figure_for_educational_background_00()
    gc.collect()

    # figure_for_educational_background_01()
    gc.collect()

    # figure_for_educational_background_02()
    gc.collect()

    figure_for_highest_title_00()
    gc.collect()

    # figure_for_highest_title_01()
    gc.collect()

    # figure_for_highest_title_02()
    gc.collect()

    figure_for_current_age_00()
    gc.collect()

    # figure_for_current_age_01()
    gc.collect()

    # figure_for_current_age_02()
    gc.collect()

    figure_for_major_discipline_00()
    gc.collect()

    # figure_for_major_discipline_01()
    gc.collect()

    # figure_for_major_discipline_02()
    gc.collect()

    figure_for_school_title_00()
    gc.collect()

    figure_for_cadre_teacher_00()
    gc.collect()

    # figure_for_cadre_teacher_01()
    gc.collect()

    # figure_for_cadre_teacher_02()
    gc.collect()

    figure_for_title_01_00()
    gc.collect()

    figure_for_current_administrative_position_00()
    gc.collect()

    figure_for_area_of_supporting_education_00()
    gc.collect()

    figure_for_different_period_00()
    gc.collect()

    figure_for_different_period_AND_major_discipline_00()
    gc.collect()

    figure_for_different_period_AND_educational_background_00()
    gc.collect()

    figure_for_different_period_AND_current_age_00()
    gc.collect()

    print(area_name + "的统计图已生成")
    print(" ")


def draw_pyecharts_for_district():
    pyechart_for_educational_background = (
        Pie(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add("", [list(z) for z in zip(label_for_educational_background, data_for_educational_background)],
             center=["50%", "60%"], radius="65%")
        .set_global_opts(title_opts=opts.TitleOpts(title="学历"), legend_opts=opts.LegendOpts(pos_left='10%'))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"),
                         tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{b}: {d}%"))
        # .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c},占比{d}%"),tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{b}: {c} ({d}%)"))    )
    )
    pyechart_for_educational_background.render_notebook()

    label_for_highest_title_updated = ['未取得职称', '三级教师', '二级教师', '一级教师', '高级教师', '正高级教师',
                                       '其他职称（非教师）']
    data_for_highest_title_updated = [0, 0, 0, 0, 0, 0, 0]

    for i in range(0, len(label_for_highest_title)):
        for k in range(0, len(label_for_highest_title_updated)):
            if (label_for_highest_title[i] == label_for_highest_title_updated[k]):
                data_for_highest_title_updated[k] = data_for_highest_title[i]
            elif (label_for_highest_title[i] in ['初级职称（非中小学系列）', '中级职称（非中小学系列）',
                                                 '高级职称（非中小学系列）']):
                data_for_highest_title_updated[6] = data_for_highest_title_updated[6] + data_for_highest_title[i]

    data_for_highest_title_updated[6] = int(data_for_highest_title_updated[6] / len(label_for_highest_title_updated))

    pyechart_for_highest_title = (
        Pie(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS))
        .add("", [list(z) for z in zip(label_for_highest_title_updated, data_for_highest_title_updated)],
             center=["50%", "60%"], radius="65%")
        .set_global_opts(title_opts=opts.TitleOpts(title="职称"), legend_opts=opts.LegendOpts(pos_left='10%'))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"),
                         tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{b}: {d}%"))
        # .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c},占比{d}%"),tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{b}: {c} ({d}%)"))    )
    )
    pyechart_for_highest_title.render_notebook()

    pyechart_for_current_age = (
        Pie(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS))
        .add("", [list(z) for z in zip(label_for_current_age, data_for_current_age)], center=["50%", "60%"],
             radius="65%")
        .set_global_opts(title_opts=opts.TitleOpts(title="年龄"), legend_opts=opts.LegendOpts(pos_left='10%'))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"),
                         tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{b}: {d}%"))
        # .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c},占比{d}%"),tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{b}: {c} ({d}%)"))    )
    )
    pyechart_for_current_age.render_notebook()

    pyechart_for_major_discipline = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.WALDEN))
        .add_xaxis(list(reversed(label_for_major_discipline)))
        .add_yaxis("总人数", list(reversed(data_for_major_discipline)))
        .reversal_axis()
        .set_series_opts(label_opts=opts.LabelOpts(position="right"))
        .set_global_opts(title_opts=opts.TitleOpts(title="主教学科"))

    )
    pyechart_for_major_discipline.render_notebook()

    label_for_current_administrative_position_updated = label_for_current_administrative_position[0:5]
    data_for_current_administrative_position1_updated = [data_for_current_administrative_position[0],
                                                         data_for_current_administrative_position[1],
                                                         data_for_current_administrative_position[2],
                                                         data_for_current_administrative_position[3], sum(
            data_for_current_administrative_position[i] for i in
            range(4, len(data_for_current_administrative_position)))]

    # print(label_for_current_administrative_position_updated)
    # print(data_for_current_administrative_position1_updated)

    pyechart_for_current_administrative_position = (
        Pie(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS))
        .add("", [list(z) for z in zip(label_for_current_administrative_position_updated,
                                       data_for_current_administrative_position1_updated)], center=["50%", "60%"],
             radius="65%")
        .set_global_opts(title_opts=opts.TitleOpts(title="行政职务"), legend_opts=opts.LegendOpts(pos_left='20%'))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"),
                         tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{b}: {d}%"))
        # .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c},占比{d}%"),tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{b}: {c} ({d}%)"))
    )
    pyechart_for_current_administrative_position.render_notebook()

    # pyechart_for_school_title = (
    #     Pie(init_opts=opts.InitOpts(theme=ThemeType.WONDERLAND))
    #     .add("", [list(z) for z in zip(label_for_school_title, data_for_school_title)],center=["50%", "60%"],radius="65%")
    #     .set_global_opts(title_opts=opts.TitleOpts(title="学校级别"),legend_opts=opts.LegendOpts(pos_left='15%'))
    #     .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c},占比{d}%"),tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{b}: {c} ({d}%)"))
    # )
    # pyechart_for_school_title.render_notebook()

    label_for_school_title_updated = ['985院校', '部属师范院校', '211院校', '其他院校']
    data_for_school_title_updated = [data_for_school_title[2], data_for_school_title[3], data_for_school_title[1],
                                     data_for_school_title[0]]

    pyechart_for_school_title = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add_xaxis(label_for_school_title_updated)
        .add_yaxis("总人数", data_for_school_title_updated)
        .set_global_opts(title_opts=opts.TitleOpts(title="毕业院校级别"))
    )
    pyechart_for_school_title.render_notebook()

    label_for_cadre_teacher_updated = ['无', '白云区骨干教师', '广州市骨干教师', '广东省骨干教师']
    data_for_cadre_teacher_updated = [0, 0, 0, 0]

    for i in range(0, len(label_for_cadre_teacher)):
        for k in range(0, len(label_for_cadre_teacher_updated)):
            if (label_for_cadre_teacher[i] == label_for_cadre_teacher_updated[k]):
                data_for_cadre_teacher_updated[k] = data_for_cadre_teacher[i]
            elif (label_for_cadre_teacher[i] in ['无', '其他']):
                data_for_cadre_teacher_updated[0] = data_for_cadre_teacher_updated[0] + data_for_cadre_teacher[i]

    data_for_cadre_teacher_updated[0] = int(data_for_cadre_teacher_updated[0] / len(label_for_cadre_teacher_updated))

    pyechart_for_cadre_teacher = (
        Pie()
        .add("", [list(z) for z in zip(label_for_cadre_teacher_updated, data_for_cadre_teacher_updated)],
             center=["50%", "60%"], radius="65%")
        .set_global_opts(title_opts=opts.TitleOpts(title="骨干教师"),
                         legend_opts=opts.LegendOpts(pos_left='15%')).set_series_opts(
            label_opts=opts.LabelOpts(formatter="{b}: {d}%"),
            tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{b}: {d}%"))
        # .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c},占比{d}%"),tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{b}: {c} ({d}%)"))
    )
    pyechart_for_cadre_teacher.render_notebook()

    pyechart_for_title_01 = (
        Pie()
        .add("", [list(z) for z in zip(label_for_title_01, data_for_title_01)], center=["50%", "60%"], radius="65%")
        .set_global_opts(title_opts=opts.TitleOpts(title="三名工作室"), legend_opts=opts.LegendOpts(pos_left='25%'))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"),
                         tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{b}: {d}%"))
        # .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c},占比{d}%"),tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{b}: {c} ({d}%)"))
    )
    pyechart_for_title_01.render_notebook()

    pyechart_for_area_of_supporting_education = (
        Pie()
        .add("", [list(z) for z in zip(label_for_area_of_supporting_education, data_for_area_of_supporting_education)],
             center=["50%", "60%"], radius="65%")
        .set_global_opts(title_opts=opts.TitleOpts(title="支教情况"), legend_opts=opts.LegendOpts(pos_left='15%'))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"),
                         tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{b}: {d}%"))
        # .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c},占比{d}%"),tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{b}: {c} ({d}%)"))
    )
    pyechart_for_area_of_supporting_education.render_notebook()

    big_title = (
        Pie()  # 不画图，只显示一个标题，用来构成大屏的标题
        .set_global_opts(
            title_opts=opts.TitleOpts(title=area_name + "片区可视化大屏",
                                      title_textstyle_opts=opts.TextStyleOpts(font_size=32), text_align="Center",
                                      pos_top=10),
            legend_opts=opts.LegendOpts(is_show=False)
        )
    )
    big_title.render_notebook()

    page = Page()
    page.add(
        big_title,
        pyechart_for_major_discipline,
        pyechart_for_current_age,
        pyechart_for_highest_title,
        pyechart_for_school_title,
        pyechart_for_educational_background,
        pyechart_for_current_administrative_position,
        pyechart_for_cadre_teacher,
        pyechart_for_title_01,
        pyechart_for_area_of_supporting_education
    )
    # page.render_notebook()
    page.render(save_path + '\\' + area_name + '数据大屏.html')

    with open(save_path + '\\' + area_name + "数据大屏.html", "r+", encoding='utf-8') as html:
        html_bf = BeautifulSoup(html, 'html.parser')
        divs = html_bf.select('.chart-container')  # 根据css定位标签，选中图像的父节点标签
        divs[0][
            "style"] = "width:50%;height:30%;position:absolute;top:0%;left:41%;border-style:dashed;border-color:#89641;border-width:0px;"
        divs[1][
            "style"] = "width:47%;height:90%;position:absolute;top:10%;left:3%;border-style:solid;border-color:#ffffff;border-width:2px;"
        divs[2][
            "style"] = "width:47%;height:45%;position:absolute;top:10%;left:50%;border-style:solid;border-color:#ffffff;border-width:2px;"
        divs[3][
            "style"] = "width:47%;height:45%;position:absolute;top:55%;left:50%;border-style:solid;border-color:#ffffff;border-width:2px;"
        divs[4][
            "style"] = "width:47%;height:45%;position:absolute;top:100%;left:3%;border-style:solid;border-color:#ffffff;border-width:2px;"
        divs[5][
            "style"] = "width:47%;height:45%;position:absolute;top:100%;left:50%;border-style:solid;border-color:#ffffff;border-width:2px;"
        divs[6][
            "style"] = "width:47%;height:45%;position:absolute;top:150%;left:3%;border-style:solid;border-color:#ffffff;border-width:2px;"
        divs[7][
            "style"] = "width:47%;height:45%;position:absolute;top:150%;left:50%;border-style:solid;border-color:#ffffff;border-width:2px;"
        divs[8][
            "style"] = "width:47%;height:45%;position:absolute;top:200%;left:3%;border-style:solid;border-color:#ffffff;border-width:2px;"
        divs[9][
            "style"] = "width:47%;height:45%;position:absolute;top:200%;left:50%;border-style:solid;border-color:#ffffff;border-width:2px;"

        body = html_bf.find("body")  # 根据标签名称定位到body标签
        # body["style"] = img.imread('') # 修改背景颜色
        body["style"] = "background-color:#ffffff;"  # 修改背景颜色
        # body["style"] = "background-image:(博客\kj.jpeg);" # 修改背景颜色
        html_new = str(html_bf)  # 将BeautifulSoup对象转换为字符
        html.seek(0, 0)  # 光标移动至
        html.truncate()  # 删除光标后的所有字符内容
        html.write(html_new)  # 将由BeautifulSoup对象转换得到的字符重新写入html文件
        html.close()


def draw_pyecharts():
    draw_pyecharts_for_district()
    gc.collect()


if __name__ == '__main__':

    if (os.path.exists(save_path + "doc.txt")):
        os.remove(save_path + "doc.txt")

    call_update_database()

    # 用来连接数据库
    conn = sqlite3.connect(database_name)
    c = conn.cursor()

    for i in range(0, len(area_list)):
        area_name = area_list[i]

        print("正在生成" + area_name + "的数据")

        update_folder()

        with open(save_path + "\\" + "doc.txt", mode="w", encoding="utf-8") as file:
            draw_charts()

        draw_pyecharts()

    conn.close()
