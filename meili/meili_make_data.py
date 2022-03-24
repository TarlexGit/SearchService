import meilisearch
import json
from os.path import abspath, join, dirname


DATASET_PATH = join('/'.join(dirname(abspath(__file__)).split('/')[:-1]), "datasets/movies.json")

client = meilisearch.Client('http://0.0.0.0:7700')

json_file = open(DATASET_PATH)
movies = json.load(json_file)
client.index('movies').add_documents(movies)

print('SEARCH CHECK:', client.index('movies').search('batman'))