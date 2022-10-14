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

##### 3.Linux限制CPU的核数：

```
htop 查看有多少个核数
taskset -c 4,5 nohup python -u run_scanorama.py > scanorama.log 2>& 1&
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

##### 6.当Poject的数量比较多：

```
1.区分出优先级：1，2，3；
2.优先级的区别要合理；
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

##### 3.数据存放路径

```
10x+Visium和Stereo_Seq:/hwfssz1/ST_BIOINTEL/P20Z10200N0039/06.groups/05.Database/luoshuai1/mark_file
```

##### 4.下次更新数据的需求：

```
1.E9.5，10.5，11.5，12.5，13.5，14.5，15.5，16.5，下次数据更新的时候一并把这个顺序理顺一下，包括脑子的这些，放的顺序太乱了；
2.之后的数据整理如果有时序关系，或者不同组织的，要考虑一下放在一起；
```

##### 5.会议纪要：

```
### 关于Liver类别数据结果集的总结

会议时间：2022/10/10 09：00-09：30
会议地点：线上腾讯会议
参会人：方博，刘克，罗帅
会议内容：讨论Liver类别数据结果集的总结，并规划本周目标。

##### 待办事项：

1）后续刘克整理Project数据的时候，整理疾病信息的时候，注意补充GEO编号；（刘克）

2）向“北京-生信大队”群询问是否有“.bw和.cloupe数据类型的处理经验；（罗帅）

3）先整理和收集已经确定可以收录的数据；（刘克，罗帅）

4）后续确定是否需要收录只有表达量的数据；（刘克，罗帅）

##### 数据整理的参考意见：

1）下次筛选数据时，先看文章有没有具体的分群信息，如果有的话，可以作为“可处理”一类标签；

2）下次筛选数据时，标出备注“是否有原始数据+细胞类型”（因为有原始数据的时候，是可以处理的）。

（PS：筛选数据优先级1和2的规则，1是有官方编号的，2是相对数据不好找的，找到可能性更小的）

##### DeadLine：

本周五之前尽量处理完已经标记为“可处理”的数据！
```



## 年底目标

```
年底任务：
1.收集够100张芯片：
	a.如果Stereo-seq的数据能达到这个目标，就只要Stereo-seq的数据集；
	b.Stereo-seq数据集达不到这个标准，那么就加上10X-visimd的数据集；
2.细胞的数据量(cell_number)要达到2500万：
	指的是单细胞的细胞数据量，不包括时空的数据；
3.所需要完成目标收集的数据集：
	a.broad数据集 
	b.10X Visium / Stereo-seq 数据集 
	c.scibet / singleR数据集 
	d.MERFISH / SeqFISH / Visium pubmed
	e.mouse atlas 2000+ / human atlas   
	f.clinical data: 肿瘤数据+免疫数据 
```
