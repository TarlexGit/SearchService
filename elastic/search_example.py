from elasticsearch import Elasticsearch


es = Elasticsearch([{'scheme':'http', 'host': 'localhost', 'port': 9200}])

resp = es.search(
    index="movies_data", query={
        "match": {
            "title": {
                "query": "batman"
            }
        }
    })
print("Got %d Hits:" % resp['hits']['total']['value'])
for hit in resp['hits']['hits']:
    # id,title,poster,overview,release_date
    print("\n %(title)s (%(release_date)s): %(overview)s \n" % hit["_source"])