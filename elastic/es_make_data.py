import csv
from os.path import abspath, join, dirname
import tqdm
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk


DATASET_PATH = join('/'.join(dirname(abspath(__file__)).split('/')[:-1]), "datasets/movies.csv")

def count_rows_in_csv():
    """returns the number of rows are in the .csv file.
    """
    with open(DATASET_PATH) as f:
        return sum([1 for _ in f]) - 1


def create_index(client):
    client.indices.create(
        index="movies_data",
        body={
            "settings": {"number_of_shards": 1},
            "mappings": {
                "properties": {
                    "id": {"type": "integer"},
                    "title": {"type": "text"},
                    "poster": {"type": "text"},
                    "overview": {"type": "text"},
                    "release_date": {"type": "date"},
                }
            },
        },
        ignore=400,
    )


def generate_actions():
    with open(DATASET_PATH, mode="r") as f:
        reader = csv.DictReader(f)
        print('***** go cikle')
        for row in reader:
            doc = {
                "_id": row["id"],
                "title": row["title"],
                "poster": row["poster"],
                "overview": row["overview"],
                "release_date": row["release_date"],
            }
            yield doc


def main():
    print("Loading dataset...")
    number_of_docs = count_rows_in_csv()

    client = Elasticsearch(
        [{'scheme':'http', 'host': 'localhost', 'port': 9200}]
    )
    print("Creating an index...")
    create_index(client)

    print("Indexing documents...")
    progress = tqdm.tqdm(unit="docs", total=number_of_docs)
    successes = 0
    for ok, action in streaming_bulk(
        client=client, index="movies_data", 
        actions=generate_actions(), 
        raise_on_error=False, # TODO - Indexed 19643/19699 documents
    ):
        progress.update(1)
        successes += ok
    print("Indexed %d/%d documents" % (successes, number_of_docs))


if __name__ == "__main__":
    main()