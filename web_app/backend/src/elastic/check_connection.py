import logging
from elasticsearch import Elasticsearch


def connect_elasticsearch():
    _es = None
    _es = Elasticsearch([{'scheme':'http', 'host': 'localhost', 'port': 9200}], )
    if _es.ping():
        print('ElasticSearch Connect')
    else:
        print('Not connect!')
    return _es.ping()


if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)
    connect_elasticsearch()
