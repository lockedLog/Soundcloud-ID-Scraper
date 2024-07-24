import pycurl
import json
import os
import threading
from itertools import cycle
from io import BytesIO

if not os.path.exists('validsoundclouds.json') or os.path.getsize('validsoundclouds.json') == 0:
    soundcloud_data = {}
else:
    with open('validsoundclouds.json', 'r') as file:
        try:
            soundcloud_data = json.load(file)
            if not isinstance(soundcloud_data, dict):
                soundcloud_data = {}
        except json.JSONDecodeError:
            soundcloud_data = {}

with open("usernames.txt", "r") as file:
    display_names = file.read().splitlines()


with open("auths.txt", "r") as file:
    auth_tokens = file.read().splitlines()

auth_cycle = cycle(auth_tokens)

lock = threading.Lock()

def grab_id(display_name):
    global soundcloud_data, auth_cycle, auth_tokens

    buffer = BytesIO()
    curl = pycurl.Curl()
    curl.setopt(pycurl.SSL_VERIFYPEER, 0)
    curl.setopt(pycurl.SSL_VERIFYHOST, 0)
    curl.setopt(pycurl.TIMEOUT, 25)
    curl.setopt(pycurl.WRITEDATA, buffer)

    url = f"https://api-v2.soundcloud.com/resolve?url=https%3A//soundcloud.com/{display_name}"
    curl.setopt(pycurl.URL, url)

    while True:
        with lock:
            if not auth_tokens:
                print("No valid tokens available. Exiting.")
                return
            auth_token = next(auth_cycle)
        
        headers = [
            f"Authorization: OAuth {auth_token}"
        ]
        curl.setopt(pycurl.HTTPHEADER, headers)

        try:
            buffer.seek(0)
            buffer.truncate()
            curl.perform()
            response_code = curl.getinfo(pycurl.RESPONSE_CODE)
            response_data = buffer.getvalue().decode('utf-8')

            if response_code == 200:
                data = json.loads(response_data)
                if 'id' in data:
                    user_id = data['id']
                    with lock:
                        print(f"User: {display_name} | ID: {user_id}")
                        soundcloud_data[display_name] = user_id
                else:
                    print(f"id not found for {display_name}.")
                break  
            elif response_code == 401:
                with lock:
                    print(f"Token: {auth_token} is not valid.")
                    auth_tokens.remove(auth_token)  
                    auth_cycle = cycle(auth_tokens)  
            else:
                print(f"Request failed for {display_name} | status code: {response_code}")
                break
        except pycurl.error:
            break
    curl.close()

threads = []
for display_name in display_names:
    if len(display_name) > 2:
        thread = threading.Thread(target=grab_id, args=(display_name,))
        threads.append(thread)
        thread.start()

for thread in threads:
    thread.join()

with open('validsoundclouds.json', 'w') as file:
    json.dump(soundcloud_data, file, indent=4)



