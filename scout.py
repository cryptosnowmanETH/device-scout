#https://discord.com/api/webhooks/860462222266335232/QF8Ar2_xtHjofdMVuCCFDLnwtB2s_FsUaIybp_QPb7NbWSWocAJ3cAU1lzjv7dRknvsQ

#create a program that gather devices on the network, but if device are taken offline it will send alert. Kind of like security monitoring. 


from os import device_encoding
from discord_webhook import DiscordEmbed, DiscordWebhook
import subprocess
import io 
import time 

#function for sending alert
#function for devices on the network 

def send_alert(webhook_url, offline_device, offline_ip, offline_mac):
    embed = DiscordEmbed(title = f'lost contact with {offline_device}', color = '1ca1ed') #embedding device IP device mac miscellaneous data we might need 
    webhook_object = DiscordWebhook(url = webhook_url) #will send relay/message 

    embed.add_embed_field(name = 'device ip', value = f'{offline_ip}')
    embed.add_embed_field(name = 'device mac', value = f'{offline_mac}')

    webhook_object.add_embed(embed)
    response = webhook_object.execute()

def fetch_devices():
    network_data = {
        'device_name': [],
        'ip_address': [],
        'mac_address': []
    }

    process = subprocess.Popen(['arp','-a'], stdout=subprocess.PIPE) #grabbing command line output 
    arp_resp = [line.strip() for line in io.TextIOWrapper(process.stdout, encoding='utf-8')]
    
    for name in arp_resp:
        network_data["device_name"].append(name.split()[0])

    for ip in arp_resp:
        network_data["ip_address"].append(ip.split()[1])

    for mac in arp_resp:
        network_data["mac_address"].append(mac.split()[3])

    return network_data


print(fetch_devices())

def monitor():
    network_patch = fetch_devices()
    
    while True: 
        active_patch = fetch_devices()
        for name, ip, mac in zip(network_patch['device_name'],network_patch['ip_address'],network_patch['mac_address']):
            if name in active_patch['device_name']:
                print(f'{ip} is online')
                time.sleep(2.5)
                continue

            else:
                send_alert("https://discord.com/api/webhooks/860462222266335232/QF8Ar2_xtHjofdMVuCCFDLnwtB2s_FsUaIybp_QPb7NbWSWocAJ3cAU1lzjv7dRknvsQ",
                            name, ip, mac)

                time.sleep(1.5)
                continue 

monitor()


#send_alert('https://discord.com/api/webhooks/860462222266335232/QF8Ar2_xtHjofdMVuCCFDLnwtB2s_FsUaIybp_QPb7NbWSWocAJ3cAU1lzjv7dRknvsQ', 'user', "201.241.24.21", 'xxxxxx')

