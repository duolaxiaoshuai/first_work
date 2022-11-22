##### 1.project表：

| 列名                | 标准1 | 标准2 | 标准3 |
| ------------------- | ----- | ----- | ----- |
| project_id          |       |       |       |
| source              |       |       |       |
| source_project_id   |       |       |       |
| project_title       |       |       |       |
| project_description |       |       |       |
| related_article_ids |       |       |       |
| research_topic      |       |       |       |
| GEO                 |       |       |       |
| data_source_URL     |       |       |       |
| data_pubdate        |       |       |       |
| article             |       |       |       |
| journal             |       |       |       |
| DOI                 |       |       |       |
| pmid                |       |       |       |
| author              |       |       |       |
| abstract            |       |       |       |
| mesh_term           |       |       |       |
| keywords            |       |       |       |
| mesh_key_values     |       |       |       |
| keywords_supplement |       |       |       |
| article_pubdate     |       |       |       |
| pubstatus           |       |       |       |
| fulltext_link       |       |       |       |
| project_status      |       |       |       |

##### 2.sample表：

| 列名                   | 标准1 | 标准2 | 标准3 |
| ---------------------- | ----- | ----- | ----- |
| project_id             |       |       |       |
| GEO                    |       |       |       |
| experiment_id          |       |       |       |
| experiment_discription |       |       |       |
| protocol_description   |       |       |       |
| species                |       |       |       |
| species_id             |       |       |       |
| sample_id              |       |       |       |
| sample_name            |       |       |       |
| source_sample_id       |       |       |       |
| sample_description     |       |       |       |
| organ                  |       |       |       |
| organ_ontology         |       |       |       |
| organ_tax2             |       |       |       |
| organ_tax2_ontology    |       |       |       |
| organ_note             |       |       |       |
| individual_id          |       |       |       |
| individual_name        |       |       |       |
| gender                 |       |       |       |
| age                    |       |       |       |
| age_unit               |       |       |       |
| development_stage      |       |       |       |
| individual_status      |       |       |       |
| ethnic_group           |       |       |       |
| current_diagnostic     |       |       |       |
| phenotype              |       |       |       |
| treatment              |       |       |       |
| treatment_duration     |       |       |       |
| disease                |       |       |       |
| disease_id             |       |       |       |
| singlecell_trans_id    |       |       |       |
| library_strategy       |       |       |       |
| library_layout         |       |       |       |
| library_selection      |       |       |       |
| tech_company           |       |       |       |
| technology_name        |       |       |       |
| release_time           |       |       |       |
| sequencer_name         |       |       |       |
| sequencer_company      |       |       |       |

##### 3.omics表：

| 列名          | 标准1 | 标准2 | 标准3 |
| ------------- | ----- | ----- | ----- |
| project_id    |       |       |       |
| sample_name   |       |       |       |
| sample_id     |       |       |       |
| omics_id      |       |       |       |
| experiment_id |       |       |       |
| species       |       |       |       |
| description   |       |       |       |
| organ         |       |       |       |

##### 4.模块一：PubMed01模板;

| 列名            | 内容                 | 实例1(输入) | 实例2(输入) |
| --------------- | -------------------- | ----------- | ----------- |
| note            | 不入选的原因/1(入选) | 1           | Bulk RNA    |
| research_topic  | 名词，属于哪个种类   | cancer      | cell_atlas  |
| article_status  | 1/0                  | 1           | 0           |
| pmid            | \                    | \           | \           |
| factor          | \                    | \           | \           |
| article         | \                    | \           | \           |
| journal         | \                    | \           | \           |
| DOI             | \                    | \           | \           |
| abstract        | \                    | \\          | \           |
| article_pubdate | \                    | \           | \           |

