from tools import data_clean

inputfile = './input_liver1021/omics_sample_1028.csv'
outputfile = './output_1028/omics_sample.csv'
fieldnames = ['id', 'omics_id', 'sample_id']


def dict_handle(rowdict: dict):
    rowdict['omics_id'] = rowdict['omics_id']
    rowdict['sample_id'] = rowdict['sample_id']
    return rowdict


if __name__ == '__main__':
    data_clean(inputfile, outputfile, fieldnames, dict_handle)
