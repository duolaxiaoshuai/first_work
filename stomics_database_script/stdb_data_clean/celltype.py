from tools import data_clean, dict_to_em

inputfile = './input_liver1021/celltype_1028.csv'
outputfile = './output_1028/celltype.csv'
fieldnames = ['id', 'name', 'ontology', 'type', 'defination']

type_map = {'standard': 1, 'author_defined': 2}


def dict_handle(rowdict: dict):
    rowdict['id'] = int(rowdict['celltype_id'].replace('CTP', ''))
    rowdict['name'] = rowdict['celltype_standard']
    rowdict['ontology'] = rowdict['celltype_ontology']
    rowdict['type'] = type_map[rowdict['status']]
    rowdict['defination'] = rowdict['def']
    return rowdict


if __name__ == '__main__':
    print(dict_to_em(type_map))
    data_clean(inputfile, outputfile, fieldnames, dict_handle)
