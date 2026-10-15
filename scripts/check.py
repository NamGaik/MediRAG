import json
d = json.load(open('preprocessed/chunks_manifest.json'))
text = open(d[0]['chunk_file']).read()
print(text)