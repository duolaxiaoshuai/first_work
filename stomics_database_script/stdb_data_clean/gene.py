from tools import data_clean, get_column_distinct

inputfile = './input/Gene.node_0817.csv'
outputfile = './output/gene.csv'
fieldnames = ['id', 'name', 'symbol', 'description', 'type',
              'species', 'species_id', 'ensembl_id', 'hgnc_id', 'mgi_id',
              'chromosome', 'map_location', 'tf_family', 'tf_source',
              'is_ligand_receptor_gene_id', 'is_ligand_receptor_gene_symbol',
              'is_ligand_source','is_receptor_ligand_gene_id',
              'is_receptor_ligand_gene_symbol','is_receptor_source']

type_map = {
    'other': 1,
    'unknown': 2,
    'protein-coding': 3,
    'biological-region': 4,
    'pseudo': 5,
    'rRNA': 6,
    'tRNA': 7,
    'ncRNA': 8,
    'scRNA': 9,
    'snRNA': 10,
    'snoRNA': 11
}

chromosome_map = {
    '10|19|3': 998,
    'Un': 999,
    'X': 1000,
    'Y': 1001,
    'X|Y': 1002,
    'MT': 1003
}


def dict_handle(rowdict: dict):
    rowdict['id'] = rowdict['Gene_id']
    rowdict['name'] = rowdict['Gene']
    rowdict['symbol'] = rowdict['Symbol']
    rowdict['description'] = rowdict['description']
    rowdict['type'] = type_map.get(rowdict['type_of_gene'])
    rowdict['species'] = rowdict['specie']
    rowdict['species_id'] = rowdict['species_id']
    rowdict['ensembl_id'] = rowdict['Ensembl_id']
    rowdict['hgnc_id'] = rowdict['HGNC_id']
    rowdict['mgi_id'] = rowdict['MGI_id']
    rowdict['chromosome'] = rowdict['chromosome']
    if rowdict['chromosome'] in chromosome_map:
        rowdict['chromosome'] = chromosome_map[rowdict['chromosome']]
    rowdict['map_location'] = rowdict['map_location']
    rowdict['tf_family'] = rowdict['TF_Family']
    rowdict['tf_source'] = rowdict['TF_Source']
    rowdict['is_ligand_receptor_gene_id'] = rowdict['isLigand_receptor_gene_id']
    rowdict['is_ligand_receptor_gene_symbol'] = rowdict['isLigand_receptor_gene_symbol']
    rowdict['is_ligand_source'] = rowdict['isLigand_Source']
    rowdict['is_receptor_ligand_gene_id'] = rowdict['isReceptor_ligand_gene_id']
    rowdict['is_receptor_ligand_gene_symbol'] = rowdict['isReceptor_ligand_gene_symbol']
    rowdict['is_receptor_source'] = rowdict['isReceptor_Source']
    return rowdict


if __name__ == '__main__':
    # print(get_column_distinct(inputfile, 'type_of_gene', count=True))
    # print(get_column_distinct(inputfile, 'chromosome', count=True))
    # print(get_column_distinct(inputfile, 'map_location', length=True))
    # print(get_column_distinct(inputfile, 'isReceptor_ligand_gene_id', length=True))
    # print(get_column_distinct(inputfile, 'Symbol', length=True))
    data_clean(inputfile, outputfile, fieldnames, dict_handle, auto_id=False)
