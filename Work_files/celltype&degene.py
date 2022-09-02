import pandas as pd
import numpy as np
def deal_with_celltype():
	df = pd.read_csv('./annotation_0815.txt',sep='\t')
	celltype = ['celltype','celltype_ontology','celltype_sub','celltype_sub_ontology',
	            'celltype_sub2','celltype_sub2_ontology','celltype_sub3','celltype_sub3_ontology']
	df1 = df[celltype]
	df1.fillna('-',inplace=True)
	df1['celltype_ontology'] = df1['celltype_ontology'].map(lambda x:x.replace('_',':'))
	df1['celltype_sub_ontology'] = df1['celltype_sub_ontology'].map(lambda x:x.replace('_',':'))
	df1['celltype_sub2_ontology'] = df1['celltype_sub2_ontology'].map(lambda x:x.replace('_',':'))
	df1['celltype_sub3_ontology'] = df1['celltype_sub3_ontology'].map(lambda x:x.replace('_',':'))

	celltype_list = df1['celltype'].tolist() + df1['celltype_sub'].tolist() + df1['celltype_sub2'].tolist() + df1['celltype_sub3'].tolist()
	celltype_all = []
	for key in list(set(celltype_list)):
	    celltype_all.append(key.strip('-'))

	a_dict1 = dict(zip(df1['celltype_ontology'],df1['celltype']))
	a_dict2 = dict(zip(df1['celltype_sub_ontology'],df1['celltype_sub']))
	a_dict3 = dict(zip(df1['celltype_sub2_ontology'],df1['celltype_sub2']))
	a_dict4 = dict(zip(df1['celltype_sub3_ontology'],df1['celltype_sub3']))

	dict_all = {} # 定义一个空字典
	dict_all.update(a_dict1)
	dict_all.update(a_dict2)
	dict_all.update(a_dict3)
	dict_all.update(a_dict4)
	value_list = []
	for k,v in dict_all.items():
	    if v in celltype_all:
	        value_list.append(v)

	df_standard = pd.read_csv('./common_cell_ontology.node.txt',sep='\t')
	df_standard['Cell'] = df_standard['Cell'].map(lambda x:x.replace('_',':'))
	df_standard.head()

	df_cell = dict(zip(df_standard['Cell'],df_standard['name']))

	dict_all.pop('-')
	b = []
	c = dict()
	for k,v in dict_all.items():
	    c[k] = df_cell[k]
	    b.append(df_cell[k])

	cell_standard = pd.DataFrame({'celltype_standard':c.values(),'celltype_ontology':c.keys()})
	cell_standard

	df_111 = dict(zip(df_standard['Cell'],df_standard['def']))

	cell_standard['def'] = cell_standard['celltype_ontology'].map(df_111)
	last = list(set(celltype_all)-set(value_list)) 
	cell_standard11 = pd.DataFrame({'celltype_standard':last})
	def_mark = cell_standard11.loc[1:]

	df_3 = pd.concat([cell_standard,def_mark])
	# df_3.to_excel('./celltype_0815.xlsx',index=False)


def deal_with_degene():
	df_deg_all = pd.read_csv('./degene_0815_new.csv')
	df_deg_all = df_deg_all.sort_values(['project_id','method'])
	print(df_deg_all)

	df_deg_all['layer'] = df_deg_all['annotation_class'].map(lambda x: x.split('=')[0].split('_')[-1])
	df_deg_all['layer_value'] = df_deg_all['annotation_class'].map(lambda x: x.split('=')[-1].split('_')[0])
	df_deg_all

	df_deg_all['layer'] = df_deg_all['layer'].map(lambda x:x if x == 'celltype' else 'celltype_' + x)
	df_deg_all['layer'].replace({'celltype':1,'celltype_sub':2,'celltype_sub2':3},inplace=True)
	df_deg_all['layer_value'].replace({'all':'root'},inplace=True)
	df_deg_all.rename(columns={'layer_value':'father_uplayer'},inplace=True)
	df_deg_all

	df_deg_all['annotation_class'] = df_deg_all['annotation_class'].map(lambda x:x.split('_celltype')[0])
	df_deg_all['annotation_class'] = df_deg_all['annotation_class'].map(lambda x:x.split('groups_')[-1])
	df_deg_all_ = df_deg_all[df_deg_all['annotation_class'] != 'annotation_exp']
	df_deg_all_ = df_deg_all_[df_deg_all_['annotation_class'] != 'annotation_db_SCEA_cluster']
	df_deg_all_

	import numpy as np
	df_deg_all_['pvals'] = [np.float32('%.3g' %x) for x in df_deg_all_['pvals']]
	df_deg_all_['logfoldchanges'] = [np.float32('%.3g' %x) for x in df_deg_all_['logfoldchanges']]
	df_deg_all_['pvals_adj'] = [np.float32('%.3g' %x) for x in df_deg_all_['pvals_adj']]
	df_deg_all_['scores'] = [np.float32('%.3g' %x) for x in df_deg_all_['scores']]
	df_deg_all_
	df_deg_all_['mark'] = df_deg_all_['omics_id'] + '_' + df_deg_all_['annotation_class']
	df_deg_all_

	df_annotation = pd.read_csv('./annotation_0815.txt',sep='\t')
	df_annotation['mark'] = df_annotation['omics_id'] + '_' + df_annotation['class']
	df_id = dict(zip(df_annotation['mark'],df_annotation['annotation_id']))
	df_deg_all_['annotation_id'] = df_deg_all_['mark'].map(df_id)
	df_deg_all_.to_csv('./degene_0815_11.csv',index=False)