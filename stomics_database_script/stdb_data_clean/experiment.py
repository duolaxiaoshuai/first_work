from tools import data_clean

inputfile1 = './input_liver1021/Sample_liver_1026_singlecell_csv.csv'
inputfile2 = './input_liver1021/Sample_liver_1018_spatial.csv'
outputfile = './output_1028/experiment.csv'
fieldnames = ['id', 'design', 'protocol_description', 'project_id']


def dict_handle(rowdict: dict):
    rowdict['id'] = int(rowdict['experiment_id'].replace('EPT', ''))
    rowdict['design'] = rowdict['experiment_discription']
    rowdict['protocol_description'] = rowdict['protocol_description']
    rowdict['project_id'] = int(rowdict['project_id'].replace('PRO', ''))
    return rowdict


if __name__ == '__main__':
    data_clean(inputfile1, outputfile, fieldnames, dict_handle, auto_id=False, distinct=True)
    data_clean(inputfile2, outputfile, fieldnames, dict_handle, auto_id=False, distinct=True,
               writeheader=False, write_mode='a')
