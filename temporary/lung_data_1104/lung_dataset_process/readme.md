1.最终搜索的输入：（lung）

```
((single cell) OR (atlas)) AND((mouse) OR (human)) AND ((lung) OR (respiratory) OR (pneumonia) OR (pulmonary) OR (pneuma) OR (pulmonic))   保留


((single cell[Title/Abstract]) OR (atlas[Title/Abstract])) AND((mouse[Title/Abstract]) OR (human[Title/Abstract])) AND ((lung[Title/Abstract]) OR (respiratory[Title/Abstract]) OR (pneumonia[Title/Abstract]) OR (pulmonary[Title/Abstract]) OR (pneuma[Title/Abstract]) OR (pulmonic[Title/Abstract]))    舍弃
   

对比的结果：
# 筛选1 ：['single cell','atlas','single-cell']
# 筛选2 ：['mouse','human']
# 筛选3 ：['lung','respiratory','pneumonia','pulmonary','pneuma','pulmonic']

#  严格筛选2次后  16,885  筛选1 + 筛选3 ------------------ 704   保留  
#  严格筛选2次后  16,885  筛选2 + 筛选3 ------------------ 765      舍弃
#  严格筛选3次后  16,885  筛选1 + 筛选2 + 筛选3 ------------------  311  舍弃  --------
#  直接加入title和abstract后，  1,525-------320    舍弃 
```

2.最终搜索的输入：（liver）

```
((single cell) OR (atlas)) AND((mouse) OR (human)) AND ((liver) OR (hepar) OR (hepatic)OR (hepatitis))
```





