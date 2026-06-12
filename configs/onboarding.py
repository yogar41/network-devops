import json
import os

from netmiko import ConnectHandler

USERNAME = os.environ["NET_USERNAME"]
PASSWORD = os.environ["NET_PASSWORD"]

with open("inventory/inventory.json") as f:
    devices = json.load(f)

for hostname, router in devices["routers"].items():

    device = {
        "device_type": router["device_type"],
        "host": router["host"],
        "username": USERNAME,
        "password": PASSWORD
    }

    print(f"\nConnecting to {hostname}")

    conn = ConnectHandler(**device)

    commands = [

        "banner motd #Managed by Jenkins#",

        "interface loopback10",

        "ip address 10.10.10.10 255.255.255.255",

        "description Created_By_Python"
    ]

    output = conn.send_config_set(commands)

    print(output)

    conn.disconnect()

print("Deployment completed")
