import json
import requests
import sys

answers = []
address = sys.argv[1]
port = sys.argv[2]
response = requests.get(f'http://{address}:{port}').json()
smallest = 20
not_mult = 3
keys = []
i = 3
while i < len(sys.argv):
    if sys.argv[i] == '--smallest':
        smallest = int(sys.argv[i + 1])
        i += 1
    elif sys.argv[i] == '--not_mult':
        not_mult = int(sys.argv[i + 1])
        i += 1
    else:
        keys.append(sys.argv[i])
    i += 1
for name in response:
    s = response[name]
    a = []
    f = name in keys
    for i in s:
        if (i < smallest or i % not_mult == 0) and f:
            pass
        else:
            a.append(i)
    if a == []:
        a = [0]
    pr = {
        "name": name,
        "min": min(a),
        "max": max(a),
        "avg": round(sum(a) / len(a))
    }
    answers.append(pr)
answers = sorted(answers, key=lambda x: x['name'])
with open('electric_eels.json', 'w') as cat_file:
    json.dump(answers, cat_file)
