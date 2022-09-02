import pandas as pd
import scanpy as sc
import os
import numpy as np


class Cell_Annotation(object):
    def __init__(self):
        self.q = Queue()  # creat Queue
        self.h5ad_out_dir = '/hwfssz1/ST_BIOINTEL/P20Z10200N0039/06.groups/caolei2/Project_2000/Share/Project_final_1_changeDEG'
        self.save_dir = '/hwfssz1/ST_BIOINTEL/P20Z10200N0039/06.user/caolei2/Project_2000/Project_final_pca'

    def get_h5ad_file(self):
        """
        get all .h5ad dir to list
        :return: data list
        """
        listdir, target_list = os.listdir(self.h5ad_out_dir), []
        for file_name in listdir:
            if file_name[-5:] == '.h5ad':
                target_list.append(file_name)
        return target_list

    def get_annotation_data(self):
        """
        Read the elements of the object and then execute the object's methods
        :return: target txt file
        """
        target_list = self.get_h5ad_file()
        result_isempty = pd.DataFrame()
        for file_name in target_list:
            adata = sc.read_h5ad(os.path.join(self.h5ad_out_dir, file_name))
            df_isempty = self.get_cell_annotation(adata,file_name)
            if df_isempty.empty:
                continue
            else:
                result_csvfile = self.get_cell_annotation_ontology(adata,file_name)
             
            if result_isempty.empty:
               result_isempty = result_csvfile
            else:
               result_isempty = pd.concat([result_isempty, result_csvfile])
        self.annotation_table_result(result_isempty)
        return

    def get_cell_annotation(self, adata,file_name):
        """
        get all celltype and celltype_number information
        :param adata: h5ad
        :return: csv file
        """
        df_isempty = pd.DataFrame()
        for j in adata.obsm:
            if 'annotation' in j and not adata.obsm[j].empty:
                # celltype_list : [celltype, celltype_sub , celltype_su2...]
                celltype_list = [i for i in adata.obsm[j].columns if 'celltype' in i and 'ontology' not in i]
                annotation_info = adata.obsm[j][celltype_list].reset_index()
                annotation_info.rename(columns={annotation_info.columns[0]: 'index'}, inplace=True)

                # acquire  'sample_id', 'sample_name' data
                cell_info = adata.obs[['sample_id','sample_name']].reset_index()
                cell_info.rename(columns={cell_info.columns[0]: 'index'}, inplace=True)

                annotation_info_all = pd.merge(annotation_info, cell_info, how='left')

                # groupby
                cell_type_List = ['sample_id']
                for x in celltype_list:
                    cell_type_List.append(x)
                    annotation_info_all[x + '_number'] = annotation_info_all.groupby(cell_type_List)[
                        'sample_name'].transform('count')
                annotation_info_all['project_id'] = file_name.split('_')[0]
                annotation_info_all['experiment_id'] = file_name.split('_')[1]
                annotation_info_all['omics_id'] = file_name.split('_')[-1].split('.')[0]
                result_table = annotation_info_all.drop_duplicates()
                result_table = result_table.reset_index(drop=True)

                # add columns of annotation_X
                a_ = result_table.columns
                result_table['class'] = j
                a_ = a_.insert(1, 'class')
                df_class_data = result_table[a_]
                if df_isempty.empty:
                    df_isempty = df_class_data
                else:
                    df_isempty = pd.concat([df_isempty, df_class_data])
        return df_isempty

    def get_cell_annotation_ontology(self, adata,file_name):
        """
         get all celltype and celltype_ontology information
        :param adata:
        :return: txt file
        """
        celltype_dict_all = dict()  # celltype and celltype_ontology
        if adata.obsm:
            for clo_name in adata.obsm:
                if 'annnotation_' in clo_name:
                    celltype_ontology_list = [celltype_ontology for celltype_ontology in adata.obsm[clo_name].columns if
                                              'ontology' in celltype_ontology]
                    celltype_list = ['_'.join(celltype.split('_')[:-1]) for celltype in celltype_ontology_list]
                    for celltype in celltype_list:
                        for celltype_number in range(len(adata.obsm[clo_name][celltype])):
                            celltype_dict_all[adata.obsm[clo_name][celltype][celltype_number]] = \
                                adata.obsm[clo_name][celltype_ontology_list[celltype_list.index(celltype)]][
                                    celltype_number]
        data_txt = np.loadtxt(
            '/hwfssz1/ST_BIOINTEL/P20Z10200N0039/06.groups/caolei2/Project_2000/Share/Temporary_table/common_cell_ontology.node.txt',
            delimiter='\t', usecols=[0, 1], unpack=False, dtype=str)

        # lower of celltype
        for i in data_txt[1:]:
            celltype_dict_all[i[1].strip().lower()] = i[0].strip()
        data_annotation_celltype_ontology1 = self.get_cell_annotation(adata,file_name)

        # map matches ontology information
        df_mark = data_annotation_celltype_ontology1[
            [celltype for celltype in data_annotation_celltype_ontology1.columns if
             'celltype' in celltype and 'number' not in celltype]]
        try:
            df_mark.fillna('-', inplace=True)
        except:
            pass
        for column in df_mark.columns:
            df_mark[column + '_new'] = df_mark[column].map(lambda x: str(x).strip().lower())
            df_mark[column + '_ontology'] = df_mark[column + '_new'].map(celltype_dict_all)
        for ontology in [ontology for ontology in df_mark.columns if 'ontology' in ontology]:
            data_annotation_celltype_ontology1[ontology] = df_mark[ontology]
        data_annotation_celltype_ontology1.replace({'': np.NAN}, inplace=True)
        data_annotation_celltype_ontology1.to_csv(
            '/hwfssz1/ST_BIOINTEL/P20Z10200N0039/06.groups/luoshuai1/mark_file/temp_annotation_txt/{}.txt'.format(
                file_name.split('.h5ad')[0]), index=False, encoding='utf_8_sig',sep='\t')
        print(data_annotation_celltype_ontology1)
        return data_annotation_celltype_ontology1

    def annotation_table_result(self,file_info):
        """
         get final result set
        :param adata:
        :return: txt file
        """
        file_info = file_info[file_info['class'] != 'annotation_db_SCEA_cluster']
        file_info = file_info[file_info['class'] != 'annotation_exp']
        file_info.drop_duplicates(inplace=True)
        file_info.reset_index(drop=True,inplace =True)
        file_info = file_info.sort_values('project_id')

        # add annotation_id
        file_info['mark'] = file_info['omics_id'] + file_info['class']
        id_dict, num = dict(), 0
        for value in file_info['mark']:
           if value not in id_dict:
               num += 1
               id_dict[value] = num

        number_list = []
        for k, v in id_dict.items():
           if len(str(v)) == 1:
               values = '00' + str(v)
           elif len(str(v)) == 2:
               values = '0' + str(v)
           else:
               values = str(v)
           number_list.append('ANO000000' + values)

        number_list_ = []
        for k, v in id_dict.items():
           number_list_.append(k)
        result = dict(zip(number_list_, number_list))
        file_info['annotation_id'] = file_info['mark'].map(result)

        # add celltype_merged
        file_info['celltype_merge'] = file_info['celltype']
        for i in [x for x in file_info.columns if 'celltype' in x and 'sub' in x]:
            file_info['celltype_merge'] = file_info['celltype_merge'].str.cat(file_info[i].astype('str'), sep='_')
        file_info['celltype_merge'].fillna('-',inplace=True)
        file_info['celltype_merge'] = file_info['celltype_merge'].map(lambda x:x.replace('_nan',''))
        file_info.to_csv('./annotation_0815.txt',index=False,encoding='utf_8_sig',sep='\t')
        return 

    def get_degene_result(self):
        """
         get final degene result set
        :return: txt file
        """
        rank_h5ad_file_list = self.get_h5ad_file()
        line_list = []
        for rank_name in rank_h5ad_file_list:
            project_id = rank_name.split('_')[0]
            experiment_id = rank_name.split('_')[1]
            omics_id = rank_name.split('_')[-1].split('.')[0]
            target_file = os.path.join(project_dir,rank_name)
            adata =sc.read_h5ad(target_file)
            print(adata)
            celltype_list = []
            for value in adata.uns.keys():
                if 'rank_genes_groups_' in value:
                    celltype_list.append(value)
            for key in celltype_list:
                try:
                    for j in range(len(adata.uns[key]['names'].dtype.names)):
                        i = 0
                        while i<= 29:
                            annotation_class = key
                            celltype = adata.uns[key]['names'].dtype.names[j]
                            logfoldchanges = adata.uns[key]['logfoldchanges'][i][j]
                            names = adata.uns[key]['names'][i][j]
                            method = key.split('_')[-1]
                            pvals = adata.uns[key]['pvals'][i][j]
                            pvals_adj = adata.uns[key]['pvals_adj'][i][j]
                            scores = adata.uns[key]['scores'][i][j]
                            line_list.append([project_id,experiment_id,omics_id,annotation_class,celltype,logfoldchanges,names,method,pvals,pvals_adj,scores])
                            i += 1
                except:
                    for x in adata.uns[key].keys():
                        for j in range(len(adata.uns[key][x]['names'].dtype.names)):
                            i = 0
                            while i<= 29:
                                annotation_class = key + '/' +  x 
                                celltype = adata.uns[key][x]['names'].dtype.names[j]
                                logfoldchanges = adata.uns[key][x]['logfoldchanges'][i][j]
                                names = adata.uns[key][x]['names'][i][j]
                                method = annotation_class.split('_')[-1]
                                pvals = adata.uns[key][x]['pvals'][i][j]
                                pvals_adj = adata.uns[key][x]['pvals_adj'][i][j]
                                scores = adata.uns[key][x]['scores'][i][j]
                                L.append([project_id,experiment_id,omics_id,annotation_class,celltype,logfoldchanges,names,method,pvals,pvals_adj,scores])
                                line_list += 1
        file_write = open("degene_0815.txt","w")
        for line in line_list:
            file_write.write(line+'\n')
        file_write.close()
        return

    def get_cell_number_info(self):
        """
        get final cell number result set
        :return: txt file
        """
        df_empty = pd.DataFrame(columns=['sample_name','cell_number','project_id'])
        h5ad_file_list = self.get_h5ad_file()
        for file_name in h5ad_file_list:
            adata = sc.read_h5ad(file_name)
            adata.obs['cell_number'] = adata.obs.groupby('sample_name')['sample_name'].transform('count')
            df_result = adata.obs.reset_index()
            df_result = df_result[['sample_name','cell_number']]
            df_result['project_id'] = file_name.split('/')[-1].strip()
            df_result.drop_duplicates(inplace=True)
            df_empty = pd.concat([df_empty,df_result])
        df_empty.to_csv('/hwfssz1/ST_BIOINTEL/P20Z10200N0039/06.groups/luoshuai1/mark_file/Cell_number_0811.txt',index =False,encoding='utf_8_sig',sep='\t')
        return

    def data_table(self):
        """
        get file infomation set
        :return: txt file
        """
        project_dir = '/jdfssz2/ST_BIOINTEL/P20Z10200N0157/liuke/STOmicsDB/study/rawdata/10.Mosta/Image'
        target_step1_dir , target_step2_dir = [],[] 
        h5ad_arranged_file = '/hwfssz1/ST_BIOINTEL/P20Z10200N0039/06.groups/caolei2/Project_2000/Share/Project_final_2/{}'
        file_write = []
        rank_file_dir = self.get_h5ad_file()
        for rank_file in rank_file_dir:
            mark_file = 'md5sum_result'
            file_name = rank_file
            file_type = 'h5ad'
            adata = sc.read_h5ad(rank_file)
            os.system("md5sum {} > {}.txt".format(rank_file,mark_file))
            df = pd.read_csv('./{}.txt'.format(mark_file),header=None)
            result = df.values[0][0]
            file_checksum = result.split()[0] + ',' + result.split()[1].split('/')[-1]
            project_id = file_name.split('_')[0]
            experiment_id = file_name.split('_')[1]
            omics_id = file_name.split('_')[2].split('.')[0]
            omice_type = file_name.split('_')[2][:3]
            file_context = 'expression_annotation'
            file_name_ = file_name
            file_type_ = file_type
            L.append([project_id,experiment_id,omics_id,omice_type,file_context,file_name_,file_type_,file_checksum])        
        file_write = open("file_0815.txt","w")
        for line in line_list:
            file_write.write(line+'\n')
        file_write.close()
        return


    def run(self):
        self.get_h5ad_file()
        self.get_annotation_data()




if __name__ == '__main__':
    cell_object = Cell_Annotation()
    cell_object.run()
    # cell_object.new_table_result()
