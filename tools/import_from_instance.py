#!/usr/bin/env python3
import json
import redis
from ransomlook.default import get_socket_path
import requests

remote_instance='https://www.ransomlook.io/api'

def fetch_screenshot(group_data):
    """
    Checks for a 'screen' key in each element of the group data array and fetches the content if it exists.
    
    :param group_data: The array of group data elements.
    """
    for element in group_data:
        if element.get("screen") not in (None, "", []):
            screenshot_url = element["screen"]
            try:
                # Determine the local path to save the screenshot
                local_path = os.path.join("../source", screenshot_url.strip("/"))
                if os.path.isfile(local_path):
                    print("Image already exists.")
                    continue

                # Make a request to the screenshot URL
                screenshot_response = requests.get(remote_instance + "/" + screenshot_url)
                if screenshot_response.status_code == 200:
                    os.makedirs(os.path.dirname(local_path), exist_ok=True)

                    # Write the screenshot content to the local path
                    with open(local_path, "wb") as screenshot_file:
                        screenshot_file.write(screenshot_response.content)

                    print(f"Screenshot saved to {local_path}")
                else:
                    print(f"Failed to fetch screenshot, URL: {screenshot_url}")
            except requests.RequestException as e:
                print(f"Error fetching screenshot, URL: {screenshot_url}: {e}")
        else:
            print(element)
            
print('Importing Groups')
groups = requests.get(remote_instance +'/export/0').json()
red = redis.Redis(unix_socket_path=get_socket_path('cache'), db=0)
for key in groups:
    red.set(key, json.dumps(groups[key]))

print('Importing Posts')
groups = requests.get(remote_instance +'/export/2').json()
red = redis.Redis(unix_socket_path=get_socket_path('cache'), db=2)
for key in groups:
    red.set(key, json.dumps(groups[key]))
    fetch_screenshot(groups[key])

print('Importing Forums')
groups = requests.get(remote_instance +'/export/3').json()
red = redis.Redis(unix_socket_path=get_socket_path('cache'), db=3)
for key in groups:
    red.set(key, json.dumps(groups[key]))

print('Importing Leaks')
groups = requests.get(remote_instance +'/export/4').json()
red = redis.Redis(unix_socket_path=get_socket_path('cache'), db=4)
for key in groups:
    red.set(key, json.dumps(groups[key]))

print('Importing Telegram channels')
groups = requests.get(remote_instance +'/export/5').json()
red = redis.Redis(unix_socket_path=get_socket_path('cache'), db=5)
for key in groups:
    red.set(key, json.dumps(groups[key]))

print('Importing Telegram message')
groups = requests.get(remote_instance +'/export/6').json()
red = redis.Redis(unix_socket_path=get_socket_path('cache'), db=6)
for key in groups:
    red.set(key, json.dumps(groups[key]))
    fetch_screenshot([{"screen":"screenshots/telegram/"+key+".png"}])
