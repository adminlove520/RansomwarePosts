import requests
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import datetime

env = Environment(
    loader=FileSystemLoader(searchpath="./templates"),
    autoescape=select_autoescape()
)

# 获取 groups
url = "https://ransomwhat.telemetry.ltd/groups"
r = requests.get(url)

groups_raw = []
if r.status_code == 200:
    try:
        groups_raw = r.json()
    except Exception as e:
        print(f"Error parsing groups JSON: {e}")
else:
    print(f"Groups API returned {r.status_code}: {r.text[:200] if r.text else 'empty'}")

groups = {}
for group in groups_raw:
    groups[group['name']] = None
    for location in group['locations']:
        if location['available']:
            groups[group['name']] = location['fqdn']
            break

# 获取 posts
url = "https://ransomwhat.telemetry.ltd/posts"
r = requests.get(url)

ransoms = []
if r.status_code == 200:
    try:
        ransoms = r.json()
    except Exception as e:
        print(f"Error parsing posts JSON: {e}")
else:
    print(f"Posts API returned {r.status_code}: {r.text[:200] if r.text else 'empty'}")

if ransoms:
    ransoms.reverse()

for ransom in ransoms:
    try:
        ransom['group_fqdn'] = groups.get(ransom['group_name'])
    except KeyError:
        ransom['group_fqdn'] = None

template = env.get_template("temp1.html")
with open('./index.html', 'w') as f:
    f.write(template.render(ransoms=ransoms, fecha=datetime.now().strftime('%d-%b-%Y %H:%M %Z')))
