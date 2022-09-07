## Tips for using Linux at work

##### 1.Linux特殊命令：

```
批量修改Linux下文件夹的名字：rename STU PRO STU*
后台执行脚本文件：nohup python -u aa.py > xx.log 2>& 1&
查看Linux下文件总数：ls |wc -l
```

##### 2.Linux快捷键指向配置：

```
.bashrc文件:
alias sshM='ssh 10.53.4.142'
alias sshO='ssh cngb-software-0-1'
alias sshN='ssh cngb-supermem-f19-7'
alias stereopy_str="source activate /work_home/zhujiahui/mambaforge/envs/py-stereopy"
alias cddata='cd /hwfssz1/ST_BIOINTEL/P20Z10200N0039/06.user/luoshuai1'
```

## Tips for using Python at work

##### 1.conda的常用命令：

```
conda create -n XX python=3.6    创建一个虚拟环境
conda env list                   显示虚拟环境的列表
conda activate base（自己的环境）   默认为base环境
conda deactivate base(自己的环境)   退出base环境
conda list  查看自己已经安装的包
```

##### 2.Python特殊第三方包的使用：

```
collections.defaultdict
fuzzywuzzy
```

##### 3.dtype属性取值问题：

```
 print(dtype.names)   # return <list>
```

##### 4.Python如何打印Try-Except错误信息：

```
except Exception as e:
    print(error_)
    print("异常类：{}".format(e.__class__.__name__))
    print("异常描述: {}".format(e))
```

##### 5.Python的DataFrame的特殊用法：

```
df['a'].value_counts().items()  # return <dict>
```

## Tips for using Git at work

##### 1.Git使用过程中高频出现问题：

```
a.Question:
“error: failed to push some refs to 'ssh://gitlab.genomics.cn:2200/biointelligence/stereomics/stomics_database_script.git”
Solve:
git pull --rebase origin master
git push origin master
```

## Tips for using Note at work

##### 1.工作文件笔记：

```
cell_annotation1.py    批量查找annotation_X的数据集代码
cell_annotation_other.py  批量批注annotation_exp/au/db-SCEA的数据集的代码
merge_table.py                 表合并的代码
cell_annotation_onlo.py   批量查找cell_ontology的数据集的代码
cell_annotation_class_singlecell_trans_id.py  将omics表中的spatialtrans_id列加到annotation_文件中的代码
cell_annotation_sample_new.py   将project表中的指定列加入到annotation表中代码 (k-p，u，v，w，AE,AD)
new_table.py  所有需要的数据的最终表

cell_annotation_class_update.py 更改annotation_class信息表的数据，比如AABC→ABC,ABBC→ABC，ABCC→ABC

test_tsv_annotation.py 批量处理后PRO中h5ad中的tsv文件的数据 (annotation_db_SCEA_cluster)
annotation_pca_all.py 批量对所有的annotation_X的h5ad的文件进行PCA，tsne和umap进行降维处理
annotation_rank_genes_groups.py   批量对所有的annotation_X的h5ad的文件进行rank_genes_group处理
table_step.py  生成具有反馈信息的step表

rename_rank_group.py  修改rank_group的文件名字
cell_rank_group_result.py  生成annotation的rank_group的结果集
link_ln_file.py  批处理硬链接的文件的批量化脚本
csv_to_txt.py 将csv文件转为txt文件(用逗号分隔)
annotation_no_result.py  没有annotation的所有数据的汇总
sample_cell_number.py  统计所有的h5ad的文件中以sample_name为分组依据的cell_number
merge_rank_result.py  多表合并 将所有的rank_result的数据进行合并
data_table_result.py  关于data表数据的整合操作

celltype_check.py 生成annotation_au和annotation_db-SCEA的celltype和celltype标准的
```

##### 2.raw counts判断：

|                 | int  | 稀疏 | 数值 | 最大值 |
| --------------- | ---- | ---- | ---- | ------ |
| raw             | √    | √    | 较小 | 可能大 |
| normalize_total | ×    | √    | 较大 | 大     |
| log1p           | ×    | √    | 较小 | 小     |
| sacle           | ×    | ×    | 较小 | 可能大 |

