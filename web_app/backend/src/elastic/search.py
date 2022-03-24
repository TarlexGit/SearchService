from elasticsearch import Elasticsearch


def search_word(query_word: str) -> dict:
    """search query data in elasticsearch

    Args:
        query_word (str): any 

    Returns:
        dict: {total_values:int, "name":{...}, ...}
    """
    es = Elasticsearch([{'scheme':'http', 'host': 'localhost', 'port': 9200}])

    resp = es.search(
        index="movies_data", query={
            "match": {
                "title": {
                    "query": query_word
                }
            }
        })

    data = {}
    duplicates = []
    data['total_values'] = resp['hits']['total']['value']
    
    for hit in resp['hits']['hits']:
        movie_data = hit['_source']
        movie_title = movie_data.pop('title')
        if movie_title in data:
            new_name = f"{movie_title}[{hit['_source']['release_date']}]"
            duplicates.append({new_name: movie_data})
        else:
            data[movie_title] = movie_data
    data['duplicates'] = duplicates

    return data