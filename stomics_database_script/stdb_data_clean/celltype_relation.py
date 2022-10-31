from tools import data_clean, dict_to_em, get_column_distinct

inputfile = './input_liver1021/celltype_relation_1028.txt'
outputfile = './output_1028/celltype_relation.csv'
fieldnames = ['id', 'celltype_id', 'celltype_name', 'type']

type_map = {'name': 1, 'alias': 2, 'ontology': 3}

def dict_handle(rowdict: dict):
    print(rowdict.keys())
    rowdict['celltype_id'] = int(rowdict['celltype_id'].replace('CTP', ''))
    rowdict['celltype_name'] = rowdict['\ufeffcelltype_name']
    rowdict['type'] = type_map[rowdict['name_type']]
    return rowdict


if __name__ == '__main__':
    print(dict_to_em(type_map))
    print(get_column_distinct(inputfile, 'name_type'))
    data_clean(inputfile, outputfile, fieldnames, dict_handle)
