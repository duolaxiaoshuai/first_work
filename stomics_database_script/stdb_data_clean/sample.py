from tools import data_clean, create_tree_dicts, dict_to_em, get_reader

reader, mode = get_reader('./input_liver1021/cell_number_1028.csv')
sample_id_cell_number_map = {}  # sample_id对应的cell_number
for i in reader:
    sample_id_cell_number_map[i['sample_id']] = i['cell_number']

inputfile1 = './input_liver1021/Sample_liver_1018_spatial.csv'
inputfile2 = './input_liver1021/Sample_liver_1026_singlecell_csv.csv'
outputfile = './output_1028/sample.csv'
fieldnames = ['id', 'sample_id', 'project_id', 'experiment_id', 'species_id', 'species_ids',
              'individual_id', 'name', 'description',
              'species', 'cell_number', 'root_organ', 'organ', 'root_organ_ontology', 'organ_ontology', 'organ_note',
              'source_sample_id', 'library_strategy', 'library_layout', 'library_selection', 'technology_name',
              'technology_company', 'release_date', 'sequencer_name', 'sequencer_company', 'section_thickness',
              'staining_protocol', 'RIN', 'DV200', 'reference_assembly']


# record_keys = [
#     ['organ', 'root_organ', 'organ', 'organ',
#      'organ_ontology', 'root_organ_ontology', 'organ_ontology', 'organ_ontology'],
#     ['organ', 'root_organ', 'organ_tax2', 'organ',
#      'organ_ontology', 'root_organ_ontology', 'organ_tax2_ontology', 'organ_ontology'],
#     ['organ', 'root_organ', 'organ_tax3', 'organ',
#      'organ_ontology', 'root_organ_ontology', 'organ_tax3_ontology', 'organ_ontology'],
# ]


def dict_handle(rowdict: dict):
    rowdict['sample_id'] = rowdict['sample_id']
    rowdict['project_id'] = int(rowdict['project_id'].replace('PRO', ''))
    rowdict['experiment_id'] = int(rowdict['experiment_id'].replace('EPT', ''))
    rowdict['species_id'] = rowdict['species_id'].split(';')[0]
    rowdict['species_ids'] = rowdict['species_id'].replace(';', ',')
    rowdict['individual_id'] = int(rowdict['individual_id'].replace('SID', ''))
    # rowdict['omics_id'] = rowdict.get('singlecell_trans_id') or rowdict.get('spatialTrans_id')
    rowdict['name'] = rowdict['sample_name']
    rowdict['description'] = rowdict['sample_description']
    rowdict['species'] = rowdict['species']
    rowdict['cell_number'] = sample_id_cell_number_map.get(rowdict['sample_id'], 0)

    rowdict['root_organ'] = rowdict['organ']
    rowdict['organ'] = rowdict['organ_tax2'] or rowdict['organ']
    rowdict['root_organ_ontology'] = rowdict['organ_ontology']
    rowdict['organ_ontology'] = rowdict['organ_tax2_ontology'] or rowdict['organ_ontology']

    rowdict['organ_note'] = rowdict['organ_note']
    rowdict['source_sample_id'] = rowdict['source_sample_id']
    rowdict['library_strategy'] = rowdict['library_strategy']
    rowdict['library_layout'] = rowdict['library_layout']
    rowdict['library_selection'] = rowdict['library_selection']
    rowdict['technology_name'] = rowdict['technology_name']
    rowdict['technology_company'] = rowdict['tech_company']
    rowdict['release_date'] = rowdict['release_time']
    rowdict['sequencer_name'] = rowdict['sequencer_name']
    rowdict['sequencer_company'] = rowdict['sequencer_company']
    rowdict['section_thickness'] = rowdict.get('section_thickness')
    rowdict['staining_protocol'] = rowdict.get('staining_protocol')
    rowdict['RIN'] = rowdict.get('RIN')
    rowdict['DV200'] = rowdict.get('DV200')
    rowdict['reference_assembly'] = rowdict.get('reference assembly')
    # rowdicts = create_tree_dicts(rowdict, record_keys)  # 拆成多条导入
    return rowdict


if __name__ == '__main__':
    id = data_clean(inputfile1, outputfile, fieldnames, dict_handle)
    print(id)
    id = data_clean(inputfile2, outputfile, fieldnames, dict_handle, id=id, writeheader=False, write_mode='a')
    print(id)