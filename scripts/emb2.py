import json
from app.main import get_qdrant
from app.vector_store import upsert, search

with open('../data/dataset.json', encoding='utf-8') as f:
    records = json.load(f)

client = get_qdrant()
upsert(client, records)
print('Upsert ok, points:', client.get_collection('search').points_count)

results = search(client, 'забыли пароль', top_k=5)
for r in results:
    print(r['id'], r['score'], r['text'])

client.close()