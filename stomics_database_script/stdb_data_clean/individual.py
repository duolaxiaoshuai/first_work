from tools import data_clean

inputfile1 = './input_liver1021/Sample_liver_1026_singlecell_csv.csv'
inputfile2 = './input_liver1021/Sample_liver_1018_spatial.csv'
outputfile = './output_1028/individual.csv'
fieldnames = ['id', 'name', 'gender', 'age', 'age_unit',
              'development_stage', 'individual_stage', 'ethnic_group', 'current_diagnostic',
              'phenotype', 'treatment', 'treatment_duration', 'disease', 'disease_id']


def dict_handle(rowdict: dict):
    rowdict['id'] = int(rowdict['individual_id'].replace('SID', ''))
    rowdict['name'] = rowdict['individual_name']
    rowdict['gender'] = rowdict['gender']
    rowdict['age'] = rowdict['age']
    rowdict['age_unit'] = rowdict['age_unit']
    rowdict['development_stage'] = rowdict['development_stage']
    rowdict['individual_stage'] = {'dead': 0}.get(rowdict['individual_status'])
    rowdict['ethnic_group'] = rowdict['ethnic_group']
    rowdict['current_diagnostic'] = rowdict['current_diagnostic']
    rowdict['phenotype'] = rowdict['phenotype']
    rowdict['treatment'] = rowdict['treatment']
    rowdict['treatment_duration'] = rowdict['treatment_duration']
    rowdict['disease'] = rowdict['disease']
    rowdict['disease_id'] = rowdict['disease_id']
    return rowdict


if __name__ == '__main__':
    data_clean(inputfile1, outputfile, fieldnames, dict_handle, auto_id=False, distinct=True)
    data_clean(inputfile2, outputfile, fieldnames, dict_handle, auto_id=False, distinct=True,
               writeheader=False, write_mode='a')
