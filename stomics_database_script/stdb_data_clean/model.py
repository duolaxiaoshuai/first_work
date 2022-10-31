from stdb_data_clean import db
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.dialects.mysql import TINYINT


class Annotation(db.Model):
    """注释表"""
    id = Column(Integer, primary_key=True)
    type = Column(String(255), nullable=False, comment='注释类型')
    project_id = Column(Integer, nullable=False, comment='项目ID')
    experiment_id = Column(Integer, nullable=False, comment='实验ID')
    omics_id = Column(String(12), nullable=False, comment='组学ID')


class Celltype(db.Model):
    """细胞类型表"""
    id = Column(Integer, primary_key=True, comment='细胞类型ID')
    name = Column(String(255), comment='细胞类型名称')
    ontology = Column(String(255), comment='细胞类型统一编号')
    type = Column(TINYINT, comment='类型|em:1-standard;2-author_defined;')
    defination = Column(String(4096), comment='定义')
