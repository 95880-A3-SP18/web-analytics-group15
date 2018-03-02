import django,os
from django.conf import settings
import pandas as pd
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

settings.configure()
django.setup()


def course_relation_all_graphs(filepath, picpath):
    course_df = pd.read_csv(filepath)
    prerequisites_df = course_df[course_df.Prerequisites != 'None'][['Course_id', 'Prerequisites']]
    corequisites_df = course_df[course_df.Corequisites != 'None'][['Course_id', 'Corequisites']]

    cor_G = nx.Graph()
    for index in range(len(corequisites_df)):
        course = corequisites_df.iloc[index]['Course_id']
        cor = corequisites_df.iloc[index]['Corequisites']
        try:
            for item in cor.split():
                if item != ',':
                    cor_G.add_edge(course, item)
        except:
            pass
    plt.figure(3, figsize=(16, 16))
    nx.draw(cor_G, with_labels=True, node_color='lightskyblue', edge_color='turquoise', node_size=80, alpha=0.8)
    plt.savefig("{}cor_all.png".format(picpath))
    plt.close()

    G_pre = nx.DiGraph()
    for index in range(len(prerequisites_df)):
        course = prerequisites_df.iloc[index]['Course_id']
        pre = prerequisites_df.iloc[index]['Prerequisites']
        try:
            for pre_course in pre.replace("(", " ").replace(")", " ").replace("and", " ").replace("or", " ").split():
                G_pre.add_edge(pre_course, course)
        except:
            pass
    plt.figure(3, figsize=(16, 16))
    nx.draw(G_pre, with_labels=True, node_color='lightskyblue', edge_color='turquoise', node_size=80, alpha=0.8)
    plt.savefig("{}pre_all.png".format(picpath))
    plt.close()


def bar_all_graphs(filepath, picpath):
    all_spring_df = pd.read_csv(filepath)
    all_spring_df = all_spring_df.drop('Unnamed: 0', axis=1)

    department_groups = all_spring_df.groupby('Department')
    dep_list, dep_count = [], []
    for name, group in department_groups:
        dep_list.append(name)
        dep_count.append(len(group))
    plt.figure(1, figsize=(20, 20))
    y_pos = np.arange(len(dep_list))
    plt.barh(y_pos, dep_count, align='center', color='turquoise', alpha=0.8)
    plt.yticks(y_pos, dep_list, fontsize = 18)
    for i, num in enumerate(dep_count):
        plt.text(-5.0, i, "{}".format(num), color='blue', fontsize=18, fontweight='bold')
    plt.savefig("{}department_all.png".format(picpath), bbox_inches='tight')
    plt.close()

    bldg_room_list = all_spring_df['Bldg/Room']
    bldg_list = []
    for bldg in bldg_room_list:
        bldg_list.append(bldg.split()[0])
    ctr = Counter(bldg_list)
    bldg_list, bldg_count = [],[]
    for key in ctr:
        bldg_list.append(key)
        bldg_count.append(ctr[key])
    plt.figure(1, figsize=(20, 15))
    y_pos = np.arange(len(bldg_list))
    plt.barh(y_pos, bldg_count, align='center', color='turquoise', alpha=0.8)
    plt.yticks(y_pos, bldg_list, fontsize = 15)
    for i, num in enumerate(bldg_count):
        plt.text(0.0, i, "{}".format(num), color='blue', fontsize=132, fontweight='bold')
    plt.savefig("{}bldg_all.png".format(picpath), bbox_inches='tight')
    plt.close()

    mini_list = all_spring_df['Mini']
    is_mini, not_mini = 0, 0
    for mini in mini_list:
        if mini == 'N':
            is_mini += 1
        else:
            not_mini += 1
    plt.figure(1, figsize=(8, 8))
    labels = 'Mini Course', 'Not Mini Course'
    sizes = [is_mini, not_mini]
    colors = ['turquoise', 'lightskyblue']
    explode = (0.1, 0)  # explode 1st slice
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')
    plt.savefig("{}mini_all.png".format(picpath), bbox_inches='tight')
    plt.close()


# I don't know how the generate this pictures before running the system
#
#
# if __name__ == "__main__":
#     picpath = '{}/courses/static/courses/images/'.format(os.getcwd())
#     if os.path.exists('{}bldg_all.png'.format(picpath)) \
#         and os.path.exists('{}mini_all.png'.format(picpath)) \
#         and os.path.exists('{}department_all.png'.format(picpath)):
#         print("pass bar")
#         pass
#     else:
#         bar_all_graphs('../parser/all_spring_courses.csv', picpath)
#
#     if os.path.exists('{}pre_all.png'.format(picpath)) \
#         and os.path.exists('{}cor_all.png'.format(picpath)):
#         print("pass cor and pre")
#         pass
#     else:
#         course_relation_all_graphs('../parser/course_detail_csv/Spring_2018_description.csv', picpath)