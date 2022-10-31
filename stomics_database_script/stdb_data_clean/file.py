from tools import data_clean

inputfile = './input_liver1021/file_1028.csv'
outputfile = 'output_1028/file.csv'
fieldnames = ['id', 'name', 'desc', 'type',
              'md5', 'omics_id', 'omics_type']


def dict_handle(rowdict: dict):
    # rowdict['id'] = int(rowdict['data_id'].replace('OSD', ''))
    rowdict['name'] = rowdict['file_name']
    rowdict['desc'] = rowdict['file_context']
    rowdict['type'] = rowdict['file_type']
    rowdict['md5'] = rowdict['file_checknum'].split(',')[0]
    rowdict['omics_id'] = rowdict['omics_id']
    rowdict['omics_type'] = {'SCT': 1, 'SPT': 2}.get(rowdict['omics_type'])
    return rowdict


if __name__ == '__main__':
    data_clean(inputfile, outputfile, fieldnames, dict_handle)
