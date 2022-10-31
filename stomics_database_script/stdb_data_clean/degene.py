from tools import data_clean
from stdb_data_clean import db
from stdb_data_clean.model import Celltype
from stdb_data_clean.annotation import annotation_type_map
inputfile = './input_liver1021/degene_1028.txt'
outputfile = './output_1028/degene.csv'
fieldnames = ['id', 'project_id', 'omics_id', 'annotation_id', 'annotation_type',
              'name', 'logfoldchange', 'method',
              'pval', 'pval_adj', 'score','layer','father_uplayer','gene_id',
              'celltype_id', 'celltype_ontology', 'celltype_name','logfoldchange_rank','pval_rank']


query = db.session.query(Celltype)
celltype_id_map = {i.name.lower(): i.id for i in query}


def dict_handle(rowdict: dict):
    print(rowdict.keys())
    rowdict['project_id'] = int(rowdict['project_id'].replace('PRO', ''))
    rowdict['omics_id'] = rowdict['omics_id']
    rowdict['annotation_id'] = rowdict['annotation_id']
    rowdict['annotation_type'] = annotation_type_map[rowdict['annotation_class']]
    rowdict['name'] = rowdict['names']
    rowdict['logfoldchange'] = rowdict['logfoldchange']
    rowdict['method'] = rowdict['method']
    rowdict['pval'] = rowdict['pval']
    rowdict['pval_adj'] = rowdict['pvals_adj']
    rowdict['score'] = rowdict['scores']
    rowdict['layer'] = rowdict['layer']
    rowdict['father_uplayer'] = rowdict['father_uplayer']
    rowdict['gene_id'] = rowdict['gene_id']
    try:
        rowdict['celltype_id'] = celltype_id_map.get((rowdict['celltype'].lower()))
    except:
        pass
    rowdict['celltype_ontology'] = rowdict['ontology']
    rowdict['celltype_name'] = rowdict['celltype_name']
    rowdict['logfoldchange_rank'] = rowdict['logfoldchange_rank']
    rowdict['pval_rank'] = rowdict['pval_rank']
    return rowdict


if __name__ == '__main__':
    data_clean(inputfile, outputfile, fieldnames, dict_handle)
