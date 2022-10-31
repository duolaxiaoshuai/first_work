import csv
import math
from pathlib import Path
from copy import deepcopy
from collections import Counter

import pandas as pd
from more_itertools import chunked

from stdb_data_clean import db


def dict_standardize(rowdict):
    """字典标准化"""
    for k, v in rowdict.items():
        # 去掉前后空白字符
        if isinstance(v, str):
            rowdict[k] = v.strip()

        # nan设为None
        if isinstance(v, float) and math.isnan(v):
            rowdict[k] = None

        # -设为None
        if v == '-':
            rowdict[k] = None

        # 空字符串设为None
        if v == '':
            rowdict[k] = None

    return rowdict


def get_reader(inputfile, sheet_name=0):
    """读取文件路径返回迭代器和文件类型

    :param inputfile: 输入文件
    :param sheet_name: 输入Excel文件的Sheet名，默认为第一张Sheet
    """
    if Path(inputfile).suffix == '.csv':
        mode = 'csv'
        reader = csv.DictReader(open(inputfile, encoding='utf-8-sig', newline=''))
        # reader = csv.DictReader(open(inputfile, encoding='utf-8', newline=''))
        # reader = csv.DictReader(open(inputfile, newline=''))
    elif Path(inputfile).suffix == '.txt':
        mode = 'csv'
        reader = csv.DictReader(open(inputfile, encoding='utf-8', newline=''), delimiter='\t')
    elif Path(inputfile).suffix == '.xlsx':
        mode = 'xlsx'
        df = pd.read_excel(inputfile, sheet_name)
        df = df.replace({pd.NaT: None})
        reader = df.iterrows()
    else:
        mode = None
        reader = []
    return reader, mode


def get_column_distinct(inputfile, column, sheet_name=0, count=False, length=False):
    """统计某一列不重复值的出现频率、最大长度

    :param inputfile: 输入文件
    :param column: 列名
    :param sheet_name: 输入Excel文件的Sheet名，默认为第一张Sheet
    :param count: 统计出现频率
    :param length: 统计最大长度
    """
    reader, mode = get_reader(inputfile, sheet_name)
    # if mode == 'xlsx':
    #     rowdict = rowdict[1].to_dict()
    if count:
        result = Counter([i[column] for i in reader])
    elif length:
        result = max(reader, key=lambda i: len(i[column]))
        result = len(result[column])
    else:
        result = sorted({i[column] for i in reader})
        result = dict(enumerate(result, start=1))
    return result


distinct_ids = set()


def data_clean(inputfile, outputfile, fieldnames, dict_handle, sheet_name=0,
               id=155277, auto_id=True, writeheader=True,
               distinct=False, test=False, write_mode='w',
               root_id_key=None):
    """数据清洗

    :param inputfile: 输入文件
    :param outputfile: 输出CSV文件
    :param fieldnames: 输出CSV文件首行字段
    :param dict_handle: 处理CSV文件每一行数据的函数名，返回dict
    :param sheet_name: 输入Excel文件的Sheet名，默认为第一张Sheet
    :param id: 起始id，默认为1
    :param auto_id: 是否以处理顺序作为id
    :param writeheader: 是否写入首行
    :param distinct: 是否去重
    :param test: 是否输出小样本
    :param write_mode: 写入模式，默认为w，还可为a追加
    :param root_id_key: 是否根据root_id_key设置root_id
    """
    reader, mode = get_reader(inputfile, sheet_name)

    root_id_map = {}  # 存放root_id
    with open(outputfile, write_mode, encoding='utf-8', newline='') as writer:
        writer = csv.DictWriter(writer, fieldnames, extrasaction='ignore')
        if writeheader:
            writer.writeheader()  # 写入首行

        distinct_values = set()  # 用于去重
        for rowdict in reader:
            if mode == 'xlsx':
                rowdict = rowdict[1].to_dict()
            rowdict = dict_standardize(rowdict)
            rowdicts = dict_handle(rowdict)
            if rowdicts is None:  # 为空则跳过
                continue

            if not isinstance(rowdicts, list):
                rowdicts = [rowdicts]

            for rowdict in rowdicts:
                if root_id_key:
                    if rowdict[root_id_key] not in root_id_map:
                        root_id_map[rowdict[root_id_key]] = id
                    rowdict['root_id'] = root_id_map[rowdict[root_id_key]]

                needless_keys = set(rowdict.keys()) - set(fieldnames)
                for key in needless_keys:  # 去掉无关数据
                    rowdict.pop(key)

                if distinct:  # 需要去重
                    key = tuple(rowdict.items())
                    if key not in distinct_values:
                        distinct_values.add(key)
                        rowdict = deepcopy(rowdict)
                        if auto_id:
                            rowdict['id'] = id
                        else:
                            if rowdict['id'] not in distinct_ids:
                                distinct_ids.add(rowdict['id'])
                            else:  # id有重复时跳过
                                break
                        writer.writerow(rowdict)
                        id += 1
                else:
                    if auto_id:
                        rowdict['id'] = id
                    writer.writerow(rowdict)
                    id += 1

            if test and id == 50:
                break
    return id


def create_tree_dicts(rowdict, record_keys):
    """一条记录拆成树状的多条记录。由于不需要做去重，没有多叉树的结构

    :param rowdict: 一条完整记录
    :param record_keys: [['原key', '新key', ...], [...]]，第一层为每条记录，第二层为要键名映射

    >>> create_tree_dicts({'organ': 1, 'organ_ontology': 1, 'organ_tax2': 2, 'organ_tax2_ontology': 3, 'organ_tax3': 3, 'organ_tax3_ontology': 3}, [['organ', 'root_organ', 'organ', 'organ', 'organ_ontology', 'root_organ_ontology', 'organ_ontology', 'organ_ontology'], ['organ', 'root_organ', 'organ_tax2', 'organ', 'organ_ontology', 'root_organ_ontology', 'organ_tax2_ontology', 'organ_ontology'], ['organ', 'root_organ', 'organ_tax3', 'organ', 'organ_ontology', 'root_organ_ontology', 'organ_tax3_ontology', 'organ_ontology']])
    [{'organ': 1, 'organ_ontology': 1, 'organ_tax2': 2, 'organ_tax2_ontology': 3, 'organ_tax3': 3, 'organ_tax3_ontology': 3, 'root_organ': 1, 'root_organ_ontology': 1}, {'organ': 2, 'organ_ontology': 3, 'organ_tax2': 2, 'organ_tax2_ontology': 3, 'organ_tax3': 3, 'organ_tax3_ontology': 3, 'root_organ': 1, 'root_organ_ontology': 1}, {'organ': 3, 'organ_ontology': 3, 'organ_tax2': 2, 'organ_tax2_ontology': 3, 'organ_tax3': 3, 'organ_tax3_ontology': 3, 'root_organ': 1, 'root_organ_ontology': 1}]
    >>> create_tree_dicts({'celltype': 1, 'celltype_ontology': 1, 'celltype_sub': 2, 'celltype_sub_ontology': 2, 'celltype_sub2': 3, 'celltype_sub2_ontology': 3, 'celltype_sub3': 4, 'celltype_sub3_ontology': 4}, [[None, 'father_key', 'celltype', 'key', ['celltype'], 'path', 'celltype_ontology', 'ontology'], ['celltype', 'father_key', 'celltype_sub', 'key', ['celltype', 'celltype_sub'], 'path', 'celltype_sub_ontology', 'ontology'], ['celltype_sub', 'father_key', 'celltype_sub2', 'key', ['celltype', 'celltype_sub', 'celltype_sub2'], 'path', 'celltype_sub2_ontology', 'ontology'], ['celltype_sub2', 'father_key', 'celltype_sub3', 'key', ['celltype', 'celltype_sub', 'celltype_sub2', 'celltype_sub3'], 'path', 'celltype_sub3_ontology', 'ontology']])
    [{'celltype': 1, 'celltype_ontology': 1, 'celltype_sub': 2, 'celltype_sub_ontology': 2, 'celltype_sub2': 3, 'celltype_sub2_ontology': 3, 'celltype_sub3': 4, 'celltype_sub3_ontology': 4, 'father_key': None, 'key': 1, 'path': '/1', 'ontology': 1}, {'celltype': 1, 'celltype_ontology': 1, 'celltype_sub': 2, 'celltype_sub_ontology': 2, 'celltype_sub2': 3, 'celltype_sub2_ontology': 3, 'celltype_sub3': 4, 'celltype_sub3_ontology': 4, 'father_key': 1, 'key': 2, 'path': '/1/2', 'ontology': 2}, {'celltype': 1, 'celltype_ontology': 1, 'celltype_sub': 2, 'celltype_sub_ontology': 2, 'celltype_sub2': 3, 'celltype_sub2_ontology': 3, 'celltype_sub3': 4, 'celltype_sub3_ontology': 4, 'father_key': 2, 'key': 3, 'path': '/1/2/3', 'ontology': 3}, {'celltype': 1, 'celltype_ontology': 1, 'celltype_sub': 2, 'celltype_sub_ontology': 2, 'celltype_sub2': 3, 'celltype_sub2_ontology': 3, 'celltype_sub3': 4, 'celltype_sub3_ontology': 4, 'father_key': 3, 'key': 4, 'path': '/1/2/3/4', 'ontology': 4}]
    """
    rowdicts = []
    for keys in record_keys:
        new_rowdict = deepcopy(rowdict)
        append = False  # 是否插入，任一值存在才插入
        for from_key, to_key in chunked(keys, 2):
            if isinstance(from_key, list) and to_key == 'path':  # 路径的话用/连接
                new_rowdict[to_key] = '/{}'.format('/'.join([str(new_rowdict[i]) for i in from_key]))
                append = True
            elif rowdict.get(from_key):
                new_rowdict[to_key] = new_rowdict.get(from_key)
                append = True
            elif from_key is None:  # 设为空
                new_rowdict[to_key] = None
                append = True
            elif to_key == 'key':  # 构成key却没值时跳过整条数据
                if not rowdict.get(from_key):
                    append = False
                    break
        if append:
            rowdicts.append(new_rowdict)
    rowdicts = unique(rowdicts)
    return rowdicts


def create_keys_map(model, from_keys, value_key):
    """读取数据库获取多键映射一值的字典

    :param model: 读取目标
    :param from_keys: 多键的字段
    :param value_key: 一值的字段
    """
    query = db.session.query(model)
    result = {}
    for x in query:
        k = tuple(getattr(x, key) for key in from_keys)
        v = getattr(x, value_key)
        result[k] = v
    return result


def dict_to_em(d):
    """字典转DDL的em注释"""
    return '|em:' + ';'.join([f'{v}-{k}' for k, v in d.items()]) + ';'


def unique(l):
    """列表去重

    >>> unique([1, 2, 1, 2])
    [1, 2]
    >>> unique([[1, 2], [1, 2]])
    [[1, 2]]
    >>> unique([{"a": 1}, {"a": 1}, {"a": 3}, {"b": 4}])
    [{'a': 1}, {'a': 3}, {'b': 4}]
    """
    try:
        return list(set(l))
    except TypeError:
        t = []
        for i in l:
            if i not in t:
                t.append(i)
        return t


def txt_to_csv(inputfile, outputfile):
    """txt转csv"""
    reader, mode = get_reader(inputfile)
    fieldnames = reader.fieldnames
    with open(outputfile, 'w', encoding='utf-8', newline='') as writer:
        writer = csv.DictWriter(writer, fieldnames, extrasaction='ignore')
        writer.writeheader()
        for rowdict in reader:
            writer.writerow(rowdict)
