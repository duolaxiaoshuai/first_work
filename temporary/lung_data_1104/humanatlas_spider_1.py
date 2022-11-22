import csv
import time

import pandas as pd
import re
import requests
from fake_useragent import UserAgent


class Humanatlas_Spider:
    def __init__(self):
        self.url = 'https://pubmed.ncbi.nlm.nih.gov/{}'

    def get_data(self):
        df_mouse_info = pd.read_excel('./project_liver_new.xlsx')
        L, mark = [], []
        # for pmid in list(set(df_mouse_info['pmid'].to_list())):
        for pmid in ['34216724']:
            try:
                ua = UserAgent(path = './useragent_info.json').random
                headers = {'User-Agent': ua}
                print(pmid)
                html = requests.get(url=self.url.format(pmid), headers=headers, verify=False).text

                author_info = html.split('data-ga-action="author_link"')[1:-1]
                author = self.get_author_info(author_info)

                journal_name_full_name = html.split('<meta name="citation_journal_title"')[-1].split('">')[0].strip().split('content="')[-1].strip()
                print(journal_name_full_name)

                keywords = html.split('<strong class="sub-title">')[-1].split('</strong>')[1].split('</p>')[0].strip()
                if '>' in keywords or '<' in keywords:
                    keywords = '-'
                print(keywords)

                associated_data = html.split('<div id="supplemental-data" class="supplemental-data">')[-1].split('</button>')[0].split('>')[-1].strip()
                if '>' in associated_data or '<' in associated_data or '[' in associated_data:
                    associated_data = '-'
                print(associated_data)

                mersh_term_list = html.split('<div id="mesh-terms" class="mesh-terms keywords-section">')[-1].split('keyword-actions-mesh-terms')
                mersh_term_result = []
                for value in mersh_term_list[1::2]:
                    value = value.split('</button>')[0].split('>')[-1].strip()
                    mersh_term_result.append(value.split('>')[-1].strip())
                mersh_term = ';'.join(mersh_term_result)
                if '>' in mersh_term or '<' in mersh_term or 'Email' in mersh_term:
                    mersh_term = '-'
                print(mersh_term)

                L.append([pmid, journal_name_full_name, author, associated_data, keywords, mersh_term])
                time.sleep(2)
            except:
                mark.append([pmid])
                break
        self.save_csv(L, './resut_1122_.csv')
        self.save_csv(mark, './mark_1104.csv')

    def get_author_info(self,author_info):
        b = []
        if author_info:
            for key in author_info:
                author_list = []
                for value in key.split('</a>')[:-1]:
                    author_list.append(value.split('>')[-1].strip())
                if b:
                    if author_list[0] in b[0]:
                        break
                b.append(author_list)
        else:
            b.append('-')
        author_ = str(b)
        if author_ == '-':
            author_ = '-'
        else:
            b_ = []
            for i in re.findall("\[.*?\]", author_, re.S):
                b_.append(i.split("['")[-1].split("',")[0].strip())
            author_ = ','.join(b_)
        return author_


    def save_csv(self, L, name):
        with open(name, 'a', encoding='utf_8_sig', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(L)


if __name__ == '__main__':
    humanatlas_spider = Humanatlas_Spider()
    humanatlas_spider.get_data()


