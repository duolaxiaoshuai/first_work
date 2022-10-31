# 数据清洗

## 安装

```shell
pip install -r requirements.txt
```

## Navicat导入向导

1. 右键表 → 导入向导
2. 导入类型为CSV文件
3. 日期排序看情况
4. 导入模式为追加或更新
5. 高级 → 勾选使用NULL取代空白字符串
6. 高级 → 取消勾选遇到错误时继续

## 遇到的问题

1. 内容字段类型不对应，如字段设计为 tinyint，导入的却是字符串，会报错
2. 导入编码为 UTF-8 可能有异常文字
3. 一篇 article 只放一个 pubmed_id
4. 部分数据实际为空，需要过滤掉，如 article 从 project 中提取，判断标题是否存在，不存在则跳过
5. pandas 读取 Excel 的字段类型为日期类型时，若遇到空值，会得到 pd.NaT，需转换为 None
6. Navicat Premium 导出的数据可能有问题，尽量用 Navicat for MySQL

## 参考文献

1. [时空数据表结构初始版](https://ns546spfdg.feishu.cn/sheets/shtcnScRuSnx3WHVeJq9TgjIR5b)
2. [时空数据表](https://ns546spfdg.feishu.cn/base/bascnt2mm7wnteQkqDpLnonmW3g)