from app.embeddings import encode, encode_batch
import math

# Один вектор
v = encode('Как сбросить пароль?')
print(len(v), type(v[0]), v[:3])

# Батч
texts = ['почему не работает аутентификация', 'у меня ошибка в браузере. что делать?']
vs = encode_batch(texts)
print(len(vs), len(vs[0]))

# Нормализованность
norm = math.sqrt(sum(x * x for x in vs[0]))
print(round(norm, 6))
