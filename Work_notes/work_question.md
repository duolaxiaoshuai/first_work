### Problems encountered in using Server & Linux at work

##### 1.再不进入到指定生产路径下工作时，会报错：

```
解决办法： rm -rf .catch
```

### Problems encountered in using Python at work

##### 1.进行批量化数据清洗时，会出现乱码问题：

```
解决办法：
encoding=‘utf_8_sig’
```

##### 2.在读取h5ad文件信息时，读取文件信息内容速度过慢：

```
解决办法：
转换数据格式，将h5ad文件转为jsonl格式文件，然后用seek方法读取
```

##### 3.如何判断文件内容是否是二进制内容：

```
形如：b'fdsgsdgdsg'
```

##### 4.需要自己实现一个“模糊匹配”的规则：

```
问题描述：在https://pubmed.ncbi.nlm.nih.gov/32968047/ 网站上找2018-2022年的mouse和human的数据下载，然后分离出来想要的数据的具体字段信息，最后对比一个表的数据的数据，形成结果集？
难点：数据格式太乱，很难在已经给出的数据集上分离出来想要数据信息。
解决办法：Python爬虫+正则表达式re+网站提供部分关键信息的提取+匹配规则的设计+最后匹配
具体思路：先从给出的杂乱的数据集上找到拼接url的关键信息"pmid"，然后通过每个"pmid"的数据，去拼接爬虫需要的url，最后在爬取想要的信息,数据量太大，考虑了多线程，但是多线程导致部分数据错乱，最后考虑多个线程脚本去执行该任务。
（编辑距离算法参考连接：https://blog.csdn.net/as604049322/article/details/117591615?ops_request_misc=&request_id=&biz_id=102&utm_term=%E6%A8%A1%E7%B3%8A%E5%8C%B9%E9%85%8D%E7%9A%84%E7%AE%97%E6%B3%95&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduweb~default-0-117591615.142^v42^pc_rank_34,185^v2^control&spm=1018.2226.3001.4187）
```

##### 5.Python的pandas模块读取文件内容过大，会出现Memory问题：

```
解决办法：
import gc （garbage collector）
del a
gc.collect()
```

### Problems encountered in using Web Crawler at work

##### 1.进行selenium操作时，每次都会提示让登录Google账号，导致批量爬虫任务无法实现：

```
解决办法:研究get请求头，最后发现在使用同一cookies信息的时候，可以只登录一次所需网站的Google账号，即可完成网络爬虫任务。
参考信息：requests.session
requests库的session会话对象可以跨请求保持某些参数**，说白了，就是比如你使用session成功的登录了某个网站，则在再次使用该session对象请求该网站的其他网页都会默认使用该session之前使用的cookie等参数。
```

### Problems encountered in using MySQL at work

##### 1.数据库的多表查询效率过低：

```
解决办法：
把原来的强外键关联(原本是A=A)换成弱外键关联(把A的值用“1”代替，然后多表连接的条件变成了1=1)：
```

### Perception of Work

```
1.做事情要及时反馈；
2.每次完成一次任务，都要考虑事情的容错和回滚，比如批量化生成数据，要考虑数据的状态，比如为什么这些数据有，那些数据没有；
3.遇到比较难的问题，
```

