import pandas as pd
import re

# 初始化空的DataFrame，每个DataFrame代表一个表格
papers_info = pd.DataFrame(columns=['UT', 'PY', 'SO', 'SN', 'DI', 'IS', 'VL'])
abstracts_info = pd.DataFrame(columns=['UT', 'AB'])
titles_info = pd.DataFrame(columns=['UT', 'TI'])
authors_info = pd.DataFrame(columns=['UT', 'AF', 'AU', 'Order'])
authors_affiliations = pd.DataFrame(columns=['UT', 'AF', 'Order', 'C1'])
references_info = pd.DataFrame(columns=['UT', 'CR'])

# 初始化变量
current_ut = ""
current_ab = ""
current_ti = ""
current_au = []
current_af = []
current_cr = []

# 定义一个函数来处理作者信息
def process_authors(ut, authors):
    for order, author in enumerate(authors):
        family_name, given_name = author.split(", ")
        authors_info.loc[len(authors_info)] = [ut, author, family_name, given_name, order + 1]

# 定义一个函数来处理作者与单位的信息
def process_affiliations(ut, authors, affiliations):
    for order, (author, affiliation) in enumerate(zip(authors, affiliations)):
        authors_affiliations.loc[len(authors_affiliations)] = [ut, author, order + 1, affiliation, order + 1]

# 读取文件
with open('qje2014_2023.txt', 'r',encoding='utf-8') as file:
    lines = file.readlines()

# 解析每一行
for line in lines:
    line = line.strip()
    if line.startswith('UT'):
        current_ut = line.split(' ')[1]
    elif line.startswith('PY'):
        papers_info.loc[len(papers_info), 'PY'] = line.split(' ')[1]
    elif line.startswith('SO'):
        papers_info.loc[len(papers_info), 'SO'] = line.split(' ')[1]
    elif line.startswith('SN'):
        papers_info.loc[len(papers_info), 'SN'] = line.split(' ')[1]
    elif line.startswith('DI'):
        papers_info.loc[len(papers_info), 'DI'] = line.split(' ')[1]
    elif line.startswith('IS'):
        papers_info.loc[len(papers_info), 'IS'] = line.split(' ')[1]
    elif line.startswith('VL'):
        papers_info.loc[len(papers_info), 'VL'] = line.split(' ')[1]
    elif line.startswith('AB'):
        current_ab = line[3:]
    elif line.startswith('TI'):
        current_ti = line[3:]
    elif line.startswith('AU'):
        current_au = line[3:].split('; ')
    elif line.startswith('AF'):
        current_af = line[3:].split('; ')
    elif line.startswith('CR'):
        current_cr.append(line[3:])
    elif line.startswith('ER'):  # End of record
        papers_info.loc[len(papers_info), 'UT'] = current_ut
        abstracts_info.loc[len(abstracts_info)] = [current_ut, current_ab]
        titles_info.loc[len(titles_info)] = [current_ut, current_ti]
        process_authors(current_ut, current_au)
        process_affiliations(current_ut, current_au, current_af)
        for ref in current_cr:
            references_info.loc[len(references_info)] = [current_ut, ref]
        # Reset the variables for the next record
        current_ab = ""
        current_ti = ""
        current_au = []
        current_af = []
        current_cr = []

# 保存DataFrame到CSV
papers_info.to_csv('papers_info.csv', index=False)
abstracts_info.to_csv('abstracts_info.csv', index=False)
titles_info.to_csv('titles_info.csv', index=False)
authors_info.to_csv('authors_info.csv', index=False)
authors_affiliations.to_csv('authors_affiliations.csv', index=False)
references_info.to_csv('references_info.csv', index=False)