import meilisearch
import json
from os.path import abspath, join, dirname


DATASET_PATH = join(
    "/".join(dirname(abspath(__file__)).split("/")[:-1]), "datasets/movies.json"
)


def main(ip: str):
    client = meilisearch.Client(f"http://{ip}:7700", "nilsir")
    json_file = open(DATASET_PATH)
    movies = json.load(json_file)
    client.index("movies").add_documents(movies)


if __name__ == "__main__":
    main()
    print("INDEXES:", client.get_indexes())
    print("SEARCH CHECK:", client.index("movies").search("batman"))
