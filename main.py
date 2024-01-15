import requests
import base64
from access import keys, url

# keys = {
#    'wp_key': 'XXXX XXXX XXXX XXXX XXXX XXXX',
#    'user': 'username'
#    }



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


file_folder_location = "/home/felo/workspace/github.com/jabuta/wp-mass-edit/files"


def load_links(files_path):
    from urllib.parse import urlparse
    import csv
    redirect_list = []
    with open(files_path + "/redirects.csv","r") as redirectfile:
        redirects = csv.reader(redirectfile, delimiter="	",)
        next(redirects, None)
        for redirect in redirects:
            from_url = urlparse(redirect[0]).path
            to_url = urlparse(redirect[1]).path if redirect[1] != "DELETE" else "DELETE"
            redirect_list.append([from_url,to_url])
    return redirect_list


def create_db_update_commands(redirect_list):
    commands = []
    for redirect in redirect_list:
        if redirect[1] == "Homepage":
            commands.append(f'wp search-replace "{redirect[0]}" "/" --precise --recurse-objects --all-tables-with-prefix --include-columns=post_content')
        elif redirect[1] != "DELETE":
            commands.append(f'wp search-replace "{redirect[0]}" "{redirect[1]}" --precise --recurse-objects --all-tables-with-prefix --include-columns=post_content')
    print(commands)
    return commands

def save_commands(commands, files_path):
    with open(files_path + "/commands.txt", "a") as f:
        f.write("\n".join(commands))
    print("commands are ready")


links_list = load_links(file_folder_location)
command_list = create_db_update_commands(links_list)

def ids_to_delete(redirect_list):
    ids_delete = []
    for slug in redirect_list:
        print(slug)
        slug[0].replace('/es/', '')      
        r = requests.get(url + f'/posts?slug={slug[0].replace("/","")}&_fields=id')
        if len(r.json()) == 0:
            continue
        ids_delete.append((r.json()[0]['id']))
    return ids_delete

def unpublish_commands(ids_unpublish):
    commands =[]
    for id in ids_unpublish:
        commands.append(f'wp post update {id} --post_status=draft')
    return commands

def delete_ids(ids_delete,headers,url):
    args = {'status': 'draft'}
    id_result = []
    for id in ids_delete:
        r = requests.post(url + "/posts/" + str(id), headers=headers, json=args)
        print(r.json())
        id_result.append((id,r.json()['code']))
    return id_result

def save_results(deleted_ids, files_path):
    with open(files_path + "/deleted_ids.txt", "w") as f:
        for deleted_id in deleted_ids:
            f.write(f'{deleted_id[0]}, {deleted_id[1]}')
            f.write("\n")
    print("saved results")

posts_to_delete = ids_to_delete(links_list)
unpublish = unpublish_commands(posts_to_delete)
save_commands(command_list + unpublish, file_folder_location)