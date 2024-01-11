import requests
import base64

keys = {
    'wp_key': 'XXXX XXXX XXXX XXXX XXXX XXXX',
    'user': 'username'
    }

# Define your WP URL
url = 'https://www.bizlatinhub.com/wp-json/wp/v2'

# Define WP Keys
user = keys['wp_key']
password = keys['user']

# Create WP Connection
wp_connection = user + ':' + password

# Encode the connection of your website
token = base64.b64encode(wp_connection.encode())

# Prepare the header of our request
headers = {
    'Authorization': 'Basic ' + token.decode('utf-8')
    }


links_file_path = "/home/felo/workspace/github.com/jabuta/wp-mass-edit/files/links_remove.txt"


def load_links(links_file_path):
    from urllib.parse import urlparse
    links_remove = []
    links_f = open(links_file_path, "r")
    for link in links_f:
        links_remove.append(urlparse(link.rstrip("\n"))[2].replace("/",""))
    links_f.close()
    print(links_remove)
    return links_remove



def post_id_from_slug(slugs):
    slugids = []
    for slug in slugs:
        r = requests.get(url + f'/posts?slug={slug}&_fields=id')
        slugids.append((slug,r.json()[0]['id']))
        print((r.json()[0]['id'],slug))
    return slugids

remove_links = load_links(links_file_path)

print(post_id_from_slug(remove_links))