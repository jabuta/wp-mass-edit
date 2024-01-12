import requests
import base64
from access import keys, url


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

def test_authentication():
    # Attempt to create a post without data
    response = requests.post(url + '/posts', headers=headers)
    
    if response.status_code == 401 or response.status_code == 403:
        print("Authentication Failed", response.status_code, response.text)
    elif response.status_code == 400:
        print("Authentication Successful")
    else:
        print("Unexpected response", response.status_code, response.text)



test_authentication()
