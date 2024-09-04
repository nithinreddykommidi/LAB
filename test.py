import re

def extract_uuid(url):
  match = re.search(r'([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})', url)
  if match:
    return match.group(1)
  else:
    return None

s = "http://127.0.0.1:8000/0bd78cef-34d3-44aa-97f9-d539c4f1691d/Eye"
uuid = extract_uuid(s)
print(uuid)