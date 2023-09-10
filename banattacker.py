import subprocess
import re


def get_online_users(port):
    list_cmd = f"sudo lsof -i:{port} -n | grep -v root | grep ESTABLISHED"
    try:
        list_output = subprocess.check_output(
            list_cmd, shell=True, stderr=subprocess.DEVNULL).decode("utf-8")
        online_user_list = list_output.strip().split('\n')
        return online_user_list

    except:
        return []


def get_online_info(port):
    online_users = get_online_users(port)
    atacker_count = {}
    ip_pattern = r"(\d+\.\d+\.\d+\.\d+)"
    for user in online_users:
        user = re.sub('\s+', ' ', user)
        user_array = user.split(" ")

        if len(user_array) >= 3:
            matches = re.findall(ip_pattern, user_array[8])
            if len(matches) == 2:
                ipz = matches[1]
                atacker_count[ipz] = atacker_count.get(ipz, 0) + 1
    print (atacker_count)
    return atacker_count

def ban_ip(ip):
    banip_command = "sudo ufw insert 1 deny from {}".format(ip)
    reload_command = "sudo ufw --force reload"

    try:
        subprocess.run(banip_command, shell=True, check=True)
        subprocess.run(reload_command, shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(e)
        return False



badip_count = get_online_info(443)
if badip_count != None:
    for ip in badip_count:
        if badip_count[ip] > 3 :
            result = ban_ip(ip)
            print (ip)