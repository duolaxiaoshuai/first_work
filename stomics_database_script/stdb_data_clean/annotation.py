import csv
from copy import deepcopy

from enums import annotation_type_map
from tools import get_reader, dict_standardize

inputfile = './input_liver1021/annotation_1028.txt' # update
outputfile = './output_1028/annotation.csv'
fieldnames = ['id', 'annotation_id', 'type', 'project_id', 'experiment_id', 'omics_id',
              'sample_id', 'celltype_id', 'celltype_name', 'celltype_ontology',
              'root_celltype_id', 'father_celltype_id', 'path', 'celltype_number']

reader, mode = get_reader('./input_liver1021/celltype_1028.csv')
celltype_ontology_map = {}  # celltype_ontology对应的celltype_id
celltype_name_map = {}  # celltype_name对应的celltype_id
for i in reader:
    if mode == 'xlsx':
        i = i[1].to_dict()
    i = dict_standardize(i)
    if i['celltype_ontology']:
        if i['celltype_ontology'] in celltype_ontology_map:  # 如果有重复的则输出
            print(1, i)
        celltype_ontology_map[i['celltype_ontology']] = i['celltype_id']
    if i['celltype_standard']:
        if i['celltype_standard'] in celltype_name_map:
            print(2, i)
        celltype_name_map[i['celltype_standard']] = i['celltype_id']


def create_node(rowdict, celltype, celltype_number, ontology, root_celltype_id=None, father_celltype_id=None,
                path=None):
    """生成叶子结点"""
    if celltype or ontology:
        rowdict = deepcopy(rowdict)
        rowdict['celltype_id'] = celltype_ontology_map.get(ontology) or celltype_name_map.get(celltype)
        if rowdict['celltype_id'] is None:
            rowdict['celltype_id'] = ''
        else:
            rowdict['celltype_id'] = int(rowdict['celltype_id'].replace('CTP', ''))
        rowdict['celltype_name'] = celltype
        rowdict['celltype_number'] = celltype_number
        rowdict['celltype_ontology'] = ontology
        rowdict['root_celltype_id'] = root_celltype_id or rowdict['celltype_id']
        rowdict['father_celltype_id'] = father_celltype_id
        if path is None:
            rowdict['path'] = '/{}'.format(rowdict['celltype_id'])
        else:
            rowdict['path'] = path + '/' + str(rowdict['celltype_id'])
        return rowdict
    else:
        return None


def dict_handle(rowdict: dict):
    rowdict['annotation_id'] = rowdict['annotation_id']
    rowdict['type'] = annotation_type_map[rowdict['class']]
    rowdict['project_id'] = int(rowdict['project_id'].replace('PRO', ''))
    rowdict['experiment_id'] = int(rowdict['experiment_id'].replace('EPT', ''))
    rowdict['omics_id'] = rowdict['omics_id']
    rowdict['sample_id'] = rowdict['sample_id']

    for k, v in rowdict.items():
        if 'ontology' in k:
            if v:
                rowdict[k] = v.replace('_', ':')

    celltype = rowdict['celltype']
    celltype_number = rowdict['celltype_number']
    celltype_ontology = rowdict['celltype_ontology']

    celltype_sub = rowdict['celltype_sub']
    celltype_sub_number = rowdict['celltype_sub_number']
    celltype_sub_ontology = rowdict['celltype_sub_ontology']

    celltype_sub2 = rowdict['celltype_sub2']
    celltype_sub2_number = rowdict['celltype_sub2_number']
    celltype_sub2_ontology = rowdict['celltype_sub2_ontology']

    celltype_sub3 = rowdict['celltype_sub3']
    celltype_sub3_number = rowdict['celltype_sub3_number']
    celltype_sub3_ontology = rowdict['celltype_sub3_ontology']

    rowdicts = []
    if not (celltype or celltype_ontology):
        return rowdicts

    new_rowdict = create_node(rowdict, celltype, celltype_number, celltype_ontology)  # 根节点
    root_celltype_id = new_rowdict['celltype_id']
    if new_rowdict:
        rowdicts.append(new_rowdict)
        father_celltype_id = new_rowdict['celltype_id']
        path = new_rowdict['path']
    else:
        return rowdicts

    new_rowdict = create_node(rowdict, celltype_sub, celltype_sub_number, celltype_sub_ontology,
                              root_celltype_id, father_celltype_id, path)  # 一级结点
    if new_rowdict:
        rowdicts.append(new_rowdict)
        father_celltype_id = new_rowdict['celltype_id']
        path = new_rowdict['path']
    else:
        return rowdicts

    new_rowdict = create_node(rowdict, celltype_sub2, celltype_sub2_number, celltype_sub2_ontology,
                              root_celltype_id, father_celltype_id, path)  # 二级结点
    if new_rowdict:
        rowdicts.append(new_rowdict)
        father_celltype_id = new_rowdict['celltype_id']
        path = new_rowdict['path']
    else:
        return rowdicts

    new_rowdict = create_node(rowdict, celltype_sub3, celltype_sub3_number, celltype_sub3_ontology,
                              root_celltype_id, father_celltype_id, path)  # 三级结点
    if new_rowdict:
        rowdicts.append(new_rowdict)
    return rowdicts


if __name__ == '__main__':
    id = 230602  # 原来是227441
    fieldnames_distinct = fieldnames.copy()
    fieldnames_distinct.remove('id')
    reader, mode = get_reader(inputfile)
    with open(outputfile, 'w', encoding='utf-8', newline='') as writer:
        writer = csv.DictWriter(writer, fieldnames, extrasaction='ignore')
        writer.writeheader()  # 写入首行
        distinct_rowdicts = {}  # 保存已写入的数据
        for rowdict in reader:
            rowdict = dict_standardize(rowdict)
            rowdicts = dict_handle(rowdict)
            for rowdict in rowdicts:
                needless_keys = set(rowdict.keys()) - set(fieldnames)
                for key in needless_keys:  # 去掉无关数据
                    rowdict.pop(key)

                key = tuple(rowdict[i] for i in fieldnames_distinct)
                if key not in distinct_rowdicts:
                    distinct_rowdicts[key] = True
                    rowdict['id'] = id
                    writer.writerow(rowdict)
                    id += 1
