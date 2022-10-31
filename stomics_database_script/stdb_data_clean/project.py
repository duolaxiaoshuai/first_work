from dateutil.parser import parse

from tools import data_clean

inputfile = './input_liver1021/Project_liver_1026_csv.csv'
outputfile = './output_1028/project.csv'
fieldnames = ['id', 'title', 'description', 'topic',
              'source', 'data_pubdate', 'data_source_url',
              'source_project_id', 'status']


def dict_handle(rowdict: dict):
    rowdict['id'] = int(rowdict['project_id'].replace('PRO', ''))
    rowdict['title'] = rowdict['project_title']
    rowdict['description'] = rowdict['project_description']
    rowdict['topic'] = rowdict['research_topic']
    rowdict['source'] = rowdict['source']
    if rowdict['data_pubdate']:
        rowdict['data_pubdate'] = parse(str(rowdict['data_pubdate'])).strftime('%d/%m/%Y')
    rowdict['data_source_url'] = rowdict['data_source_URL']
    rowdict['source_project_id'] = rowdict['source_project_id']
    rowdict['status'] = {'unavailable': 0, 'available': 1}.get(rowdict['project_status'])
    return rowdict


if __name__ == '__main__':
    data_clean(inputfile, outputfile, fieldnames, dict_handle, auto_id=False)
