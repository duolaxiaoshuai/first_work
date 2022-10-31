from stdb_data_clean import db
from stdb_data_clean.model import Celltype
from stdb_data_clean.tools import get_reader

reader, mode = get_reader('common_cell_ontology.node.txt')
for i in reader:
    ontology = i['Cell']
    defination = i['def']
    db.session.query(Celltype).filter(Celltype.ontology == ontology).update({Celltype.defination: defination})
    db.session.commit()
    print(ontology)
