import pandas as pd 
import numpy as np 
def fun(x):
    a_list = x.split(';')
    a= []
    for key in a_list:
        if len(key.split('/')) == 1:
            a.append(key.strip())
    a_ = set(a)
    return ','.join(list(a_))


def fun1(x):
    a_list = x.split(';')
    b = []
    for key in a_list:
        if len(key.split('/')) == 1:
            pass
        else:
            b.append(key.split('/')[0].strip())
    b_ = set(b)
    return ','.join(list(b_))

def fun2(x):
	if x[0] == ',':
		return x[1:]
	elif x[-1]:
		return x[:-1]
	return x

def mesh_term():
	# df = pd.read_csv("./Project-batch1and2_20220816.csv")
	df = pd.read_csv('./result_1122_.csv')
	df1 = df[['project_id','mesh_term']]
	df1['mesh_term'].fillna('-',inplace=True)
	df1['x'] = df1['mesh_term'].map(fun)
	df1['y'] = df1['mesh_term'].map(fun1)

	df_mesh_x = pd.read_excel('./mesh_standard.xlsx',sheet_name='x')
	df_mesh_y = pd.read_excel('./mesh_standard.xlsx',sheet_name='y')
	result_x ,	result_y = [] , []
	x_list = df_mesh_x['x'].tolist()
	for key in df1['x'].tolist():
	    key_list = key.split(',')
	    a_x = []
	    for i in key_list:
	        if i.strip() not in x_list:
	            a_x.append(i.strip().split('*')[0])
	    result = ','.join(a_x)
	    result_x.append(result)
	y_list = df_mesh_y['y'].tolist()
	for key in df1['y'].tolist():
	    key_list = key.split(',')
	    a_y = []
	    for i in key_list:
	        if i.strip() not in y_list:
	            a_y.append(i.strip().split('*')[0])
	    result = ','.join(a_y)
	    result_y.append(result)
	df1['result_x'] = result_x
	df1['result_y'] = result_y
	df1['result_final'] = df1['result_x'] + ',' + df1['result_y']
	df1 = df1[['project_id','mesh_term','result_final']]
	df1['result_final'] = df1['result_final'].map(fun2)
	df1.replace({'-':np.NAN},inplace=True)
	df1.to_csv('./mesh_key_result_1122.csv',index=False,encoding='utf_8_sig')

mesh_term()
