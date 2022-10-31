import pandas as pd
organ_article = pd.read_csv('./input_liver1021/organ_article_1028.csv')
organ_article['project_id'] = organ_article['project_id'].map(lambda x:int(x.split('PRO')[-1]))
article = pd.read_csv('./input_liver1021/article.csv')
organ_id_dict = dict(zip(article['project_id'],article['id']))
organ_article['article_id'] = organ_article['project_id'].map(organ_id_dict)
organ_article.to_csv('./output_1028/organ_article.csv',index=False,encoding='utf_8_sig')