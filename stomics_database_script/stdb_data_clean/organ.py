from tools import data_clean, create_tree_dicts

inputfile = './input_liver1021/organ_uberon_all_1020.csv'
outputfile = './output_liver1021/organ.csv'
fieldnames = ['id', 'root_id', 'root_key', 'father_key', 'key', 'path', 'name']
record_keys = [
    [None, 'father_key',
     'organ_ontology', 'key',
     ['organ_ontology'], 'path',
     'organ', 'name'],

    ['organ_ontology', 'father_key',
     'organ_tax2_ontology', 'key',
     ['organ_ontology', 'organ_tax2_ontology'], 'path',
     'organ_tax2', 'name'],

    ['organ_tax2_ontology', 'father_key',
     'organ_tax3_ontology', 'key',
     ['organ_ontology', 'organ_tax2_ontology', 'organ_tax3_ontology'], 'path',
     'organ_tax3', 'name'],

    ['organ_tax3_ontology', 'father_key',
     'organ_tax4_ontology', 'key',
     ['organ_ontology', 'organ_tax2_ontology', 'organ_tax3_ontology', 'organ_tax4_ontology'], 'path',
     'organ_tax4', 'name'],

    ['organ_tax4_ontology', 'father_key',
     'organ_tax5_ontology', 'key',
     ['organ_ontology', 'organ_tax2_ontology', 'organ_tax3_ontology', 'organ_tax4_ontology',
      'organ_tax5_ontology'], 'path',
     'organ_tax5', 'name'],

    ['organ_tax5_ontology', 'father_key',
     'organ_tax6_ontology', 'key',
     ['organ_ontology', 'organ_tax2_ontology', 'organ_tax3_ontology', 'organ_tax4_ontology',
      'organ_tax5_ontology', 'organ_tax6_ontology'], 'path',
     'organ_tax6', 'name'],

    ['organ_tax6_ontology', 'father_key',
     'organ_tax7_ontology', 'key',
     ['organ_ontology', 'organ_tax2_ontology', 'organ_tax3_ontology', 'organ_tax4_ontology',
      'organ_tax5_ontology', 'organ_tax6_ontology', 'organ_tax7_ontology'], 'path',
     'organ_tax7', 'name'],

    ['organ_tax7_ontology', 'father_key',
     'organ_tax8_ontology', 'key',
     ['organ_ontology', 'organ_tax2_ontology', 'organ_tax3_ontology', 'organ_tax4_ontology',
      'organ_tax5_ontology', 'organ_tax6_ontology', 'organ_tax7_ontology',
      'organ_tax8_ontology'], 'path',
     'organ_tax8', 'name'],

    ['organ_tax8_ontology', 'father_key',
     'organ_tax9_ontology', 'key',
     ['organ_ontology', 'organ_tax2_ontology', 'organ_tax3_ontology', 'organ_tax4_ontology',
      'organ_tax5_ontology', 'organ_tax6_ontology', 'organ_tax7_ontology',
      'organ_tax8_ontology', 'organ_tax9_ontology'], 'path',
     'organ_tax9', 'name'],

    ['organ_tax9_ontology', 'father_key',
     'organ_tax10_ontology', 'key',
     ['organ_ontology', 'organ_tax2_ontology', 'organ_tax3_ontology', 'organ_tax4_ontology',
      'organ_tax5_ontology', 'organ_tax6_ontology', 'organ_tax7_ontology',
      'organ_tax8_ontology', 'organ_tax9_ontology', 'organ_tax10_ontology'], 'path',
     'organ_tax10', 'name'],
]


def dict_handle(rowdict: dict):
    for k, v in rowdict.items():
        if 'ontology' in k:
            if v:
                rowdict[k] = v.replace('_', ':')

    rowdict['root_key'] = rowdict['organ_ontology']
    rowdicts = create_tree_dicts(rowdict, record_keys)
    return rowdicts


if __name__ == '__main__':
    data_clean(inputfile, outputfile, fieldnames, dict_handle, distinct=True, root_id_key='organ_ontology')
