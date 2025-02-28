import requests

plugins = (
    "jetpack",
    "site-editor",
    "akismet"
)

base_url = "http://asucar.dl/wp-content/plugins/"

def check_plugin(plugin):
    url = f"{base_url}{plugin}/readme.txt"
    response = requests.get(url)
    if response.status_code == 200:
        print(f"[+] Plugin encontrado: {plugin}")
    else:
        pass

for plugin in plugins:
    check_plugin(plugin)
