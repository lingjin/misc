from __future__ import print_function
from datetime import date
from datetime import datetime
import json
import base64
import urllib.request
import re
import os
import time

SERVER_CONFIG_FILE = '../server_config.json'
USERNAME = 'username'
PASSWORD = 'password'
LOOP_COUNT = 'loop_count'
SLEEP_TIMER = 'sleep_timer'


def init_server_data_from_json():
    with open(SERVER_CONFIG_FILE, 'r') as json_file:
        json_data = json.load(json_file)

    username = json_data[USERNAME]
    password = base64.b64decode(json_data[PASSWORD]).decode('ascii')
    loop_count = json_data[LOOP_COUNT]
    sleep_timer = json_data[SLEEP_TIMER]

    return username, password, loop_count, sleep_timer


def print_log(log):
    today = date.today()
    d1 = today.strftime("%d/%m/%Y")
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    print(d1 + ' ' + current_time + ': ' + log)
    return 

def delete_local_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print_log(file_path + ' has been deleted')
    else:
        print_log(file_path + ' does not exist') 

    return 

def wait_to_7pm():
    now = datetime.now()
    today7pm = now.replace(hour=19, minute=0, second=0, microsecond=0)
    while now < today7pm:
        print("Now the time is " + now.strftime("%H:%M:%S"))
        time.sleep(60*10)
        now = datetime.now()
    return

def connect_server():
    # create a password manager
    password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()

    # Add the username and password.
    # If we knew the realm, we could use it instead of None.
    username, password, loop_count, sleep_timer = init_server_data_from_json()
    top_level_url = "https://artifacts.mot.com/artifactory/banks/11/"
    password_mgr.add_password(None, top_level_url, username, password)

    handler = urllib.request.HTTPBasicAuthHandler(password_mgr)

    # create "opener" (OpenerDirector instance)
    opener = urllib.request.build_opener(handler)

    # use the opener to fetch a URL
    opener.open(top_level_url)

    # Install the opener.
    # Now all calls to urllib.request.urlopen use our opener.
    urllib.request.install_opener(opener)
    for i in range(loop_count):
        pagehandle = urllib.request.urlopen(top_level_url)
        html = pagehandle.read()
        html = html.decode('utf8')
        release_num = re.findall('>RRP31\.(.{0,3}\d)/</a>',html, re.S)

        for i in range(0, len(release_num)):
            release_label = "RRP31." + release_num[i]
            second_level_url = top_level_url + release_label + "/banks_retail/userdebug/intcfg_test-keys/"
            pagehandle = urllib.request.urlopen(second_level_url)
            html = pagehandle.read()
            html = html.decode('utf8')
            fastboot = re.findall('href="(fastboot.*?)">', html, re.S)
            if 0 == len(fastboot):
                print_log(release_label + " does not contain fastboot image, skip downloading")
            else:
                fastboot_file_name = fastboot[0]
                download_url = second_level_url + fastboot_file_name
                localfile_name = "./" + fastboot_file_name
                print_log("Loop " + i + ", Downloading " + fastboot_file_name)
                urllib.request.urlretrieve(download_url, localfile_name)
                delete_local_file(localfile_name)
                time.sleep(sleep_timer)
        
    return

if __name__ == "__main__":
    while True:
        wait_to_7pm()
        connect_server()

