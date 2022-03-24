from elasticsearch import Elasticsearch


def search_word(query_word: str) -> dict:
    """search query data in elasticsearch

    Args:
        query_word (str): any

    Returns:
        json object: {total:{}, max_score:float, hits:[dict]}
    """
    es = Elasticsearch([{"scheme": "http", "host": "localhost", "port": 9200}])

    resp = es.search(
        index="movies_data", query={"match": {"title": {"query": query_word}}}
    )
    return resp["hits"]
