from tools import data_clean, get_column_distinct, dict_to_em

inputfile = './input_liver1021/omics_1028.csv'
outputfile = './output_1028/omics.csv'
fieldnames = ['id', 'omics_id', 'project_id', 'experiment_id', 'type', 'description', 'protocol',
              'sample_type', 'species', 'organs','sample_number','cell_number']

type_map = {
    'SCT': 1,
    'SPT': 2
}

sample_type_map = {
    'independent': 1,
    'serial_section': 2,
    'time_series': 3
}


def dict_handle(rowdict: dict):
    """处理第一张Sheet"""
    # rowdict['id'] = rowdict['omics_id']
    rowdict['omics_id'] = rowdict['omics_id']
    rowdict['project_id'] = int(rowdict['project_id'].replace('PRO', ''))
    rowdict['experiment_id'] = int(rowdict['experiment_id'].replace('EPT', ''))
    if rowdict['omics_id'].startswith('SCT'):
        rowdict['type'] = 1
    elif rowdict['omics_id'].startswith('SPT'):
        rowdict['type'] = 2
    rowdict['description'] = rowdict['description']
    rowdict['protocol'] = rowdict['protocol']
    rowdict['sample_type'] = sample_type_map[rowdict['sample_relationship']]
    rowdict['species'] = rowdict['species']
    rowdict['organs'] = rowdict['organ'].replace('|', ',')
    rowdict['sample_number'] = rowdict['sample_number']
    rowdict['cell_number'] = rowdict['cell_number']
    return rowdict


if __name__ == '__main__':
    # print(get_column_distinct(inputfile, 'sample_relationship'))
    # print(get_column_distinct(inputfile, 'protocol'))
    # print(dict_to_em(sample_type_map))
    # input()
    data_clean(inputfile, outputfile, fieldnames, dict_handle)
