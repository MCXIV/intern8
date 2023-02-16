# -*- coding: utf-8 -*-
# --------------------------------------------------
# intern8 is a way to automate Ngrok tunneling on a Linux embedded device.
# Quentin 'MCXIV' Dufournet, 2023
# --------------------------------------------------
# Built-in
import sys
import time
import json
import argparse
import subprocess as sp

# 3rd party
import requests
from rich import print as rprint

# --------------------------------------------------
# Usage: python3 intern8.py -w 1 -u https://hooks.slack.com/services/xxx
#        python3 intern8.py -w 1 -u https://discord.com/api/webhooks/xxx
# --------------------------------------------------


class intern8():
    def __init__(self):
        self.args = self.parse_args()

    def parse_args(self):
        """
        It parses the arguments passed to the script and returns them as an object
        :return: The arguments passed to the script.
        """

        parser = argparse.ArgumentParser()

        parser.add_argument(
            '-w', help='Activate or not Webhook (Default is 0)',
            type=bool, nargs='?', default=0)
        parser.add_argument(
            '-u', help='Webhook URL',
            type=str, nargs='?', default=None)

        return parser.parse_args()

    def start_ngrok(self):
        """
        It starts ngrok in tcp mode on port 22.
        """

        self.ngrok = sp.Popen(['ngrok', 'tcp', '22'], stdout=sp.PIPE, stderr=sp.PIPE)
        time.sleep(1)

    def fetch_ngrok(self):
        """
        It fetches the address and port of the ngrok tunnel
        :return: The address and port of the ngrok tunnel.
        """

        data = requests.get('http://localhost:4040/api/tunnels', timeout=5)
        if data.status_code != 200:
            rprint('[red][bold]Error: Ngrok is not running.')
            sys.exit(1)

        data = data.json()['tunnels'][0]['public_url']
        data = {
            'address': data[6:].split(':')[0],
            'port': data.split(':')[2],
        }

        return data

    def kill_ngrok(self):
        """
        It kills the ngrok process.
        """

        self.ngrok.kill()
        rprint('[red][bold]Ngrok tunnel killed.')

    def discord_webhook(self, data, url):
        """
        It sends a webhook to Discord with the SSH address and port

        :param data: The data that will be sent to the webhook
        :param url: The URL of the webhook
        :return: The response from the webhook.
        """

        embed = {
            'title': 'Raspberry today\'s address',
            'description': f'Username : pi\nSSH address : {data["address"]}:{data["port"]}' +
            f'\n\nQuick command : `ssh pi@{data["address"]} -p {data["port"]}`',
        }

        data = {
            'content': '',
            'embeds': [embed]
        }

        return requests.post(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            timeout=5
        )

    def slack_webhook(self, data, url):
        """
        It takes the data from the `get_ip_address()` function and sends it to a Slack webhook

        :param data: The data to be sent to the webhook
        :param url: The URL of the Slack webhook
        :return: The return value is the response from the post request.
        """

        data = {
            'text': 'Raspberry today\'s address :\n\n' +
                    f'Username : pi\nSSH address : {data["address"]}:{data["port"]}' +
                    f'\n\nQuick command : `ssh pi@{data["address"]} -p {data["port"]}`',
        }

        return requests.post(
            url,
            data=json.dumps(data),
            timeout=5
        )

    def main(self):
        """
        It creates a tunnel to the internet and then prints the address and port of the tunnel.
        If the webhook argument is passed, it sends a webhook to the webhook URL.
        (Currently only supports Slack and Discord)
        """

        self.start_ngrok()
        data = self.fetch_ngrok()
        rprint(f'[green][bold]Ngrok tunnel created: [blue]{data["address"]}:{data["port"]}[/blue]')
        rprint(f'[green][bold]Quick command: [blue]ssh pi@{data["address"]} -p {data["port"]}[/blue]')

        if self.args.w:
            if 'slack' in self.args.u:
                self.slack_webhook(data, self.args.u)
            elif 'discord' in self.args.u:
                self.discord_webhook(data, self.args.u)


if __name__ == "__main__":
    intern8().main()
