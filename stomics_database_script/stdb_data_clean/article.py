from dateutil.parser import parse

from tools import data_clean

inputfile = './input_liver1021/Project_liver_1026_csv.csv'
outputfile = './output_1028/article.csv'
fieldnames = ['id', 'project_id', 'title', 'author',
              'abstract', 'journal', 'DOI', 'pubmed_id',
              'mesh_term', 'keywords', 'pubdate', 'pubstatus', 'url']


def dict_handle(rowdict: dict):
    rowdict['project_id'] = int(rowdict['project_id'].replace('PRO', ''))
    if rowdict['article']:
        rowdict['title'] = rowdict['article']
    else:
        return None
    rowdict['author'] = rowdict['author']
    rowdict['abstract'] = rowdict['abstract']
    rowdict['journal'] = rowdict['journal']
    rowdict['DOI'] = rowdict['DOI']
    rowdict['pubmed_id'] = int(rowdict['pmid'].split('.')[0]) if isinstance(rowdict['pmid'], str) else rowdict['pmid']
    rowdict['mesh_term'] = rowdict['mesh_term']
    rowdict['keywords'] = rowdict['keywords']
    if rowdict['article_pubdate']:
        rowdict['pubdate'] = parse(rowdict['article_pubdate'].split(';')[0]).strftime('%d/%m/%Y')
    rowdict['pubstatus'] = {'published': 1, 'preprint': 2}.get(rowdict['pubstatus'])
    rowdict['url'] = rowdict['fulltext_link']
    return rowdict


if __name__ == '__main__':
    data_clean(inputfile, outputfile, fieldnames, dict_handle)
