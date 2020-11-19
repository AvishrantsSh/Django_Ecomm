import pandas as pd
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.analysis import StandardAnalyzer
from whoosh.lang.morph_en import variations
import os.path
from whoosh import index
from whoosh.index import create_in
from whoosh.qparser import QueryParser
from whoosh.query import *
from whoosh.qparser import QueryParser
from whoosh.lang.morph_en import variations
from whoosh import qparser, query, scoring
my_analyzer = StandardAnalyzer()
myschema = Schema( id = ID(stored=True), name =TEXT(stored=True,analyzer=my_analyzer))

class Indexer(object):
    def __init__(self):
        pass

    def populate_index(self, dirname,dataframe):
        if not os.path.exists(dirname):
            os.mkdir(dirname)
        ix = create_in(dirname, myschema)
        writer=ix.writer()
        print(dataframe)
        data = pd.DataFrame(dataframe[1:], columns=dataframe[0])
        # print(data)
        papers = [data]
        for paper_set in papers:
            for index, row in paper_set.iterrows():
                writer.add_document(id = row['id'], name = row['name'])
                # print(row['id'], row['name'])
        writer.commit()
            
    #creating index searcher
    def index_search(self, search_query):
        if '/' in search_query:
            return []
        search_query = [token.text for token in my_analyzer(search_query)]
        search_query = '~ '.join(search_query)
        search_query += '~'
        ix=index.open_dir("index")
        with ix.searcher(weighting=scoring.Frequency) as s:
            og = qparser.OrGroup.factory(0.8)
            qp = qparser.QueryParser("name", schema=ix.schema, termclass=MyFuzzyTerm, group=og)
            qp.add_plugin(qparser.FuzzyTermPlugin())
            qp.add_plugin(qparser.SequencePlugin())
            q = qp.parse(search_query)
            results = s.search(q, terms=True,limit=None)
            print(q)
            print(len(results))
            list=[]
            for res in results:
                # list.append(res['name'])
                list.append(res['id'])
            return list

class MyFuzzyTerm(FuzzyTerm):
        def __init__(self, fieldname, text, boost=1.0, maxdist=2, prefixlength=1, constantscore=True):
            super(MyFuzzyTerm, self).__init__(fieldname, text, boost, maxdist, prefixlength, constantscore)

# ind = Indexer()
# ind.populate_index("index", data)
