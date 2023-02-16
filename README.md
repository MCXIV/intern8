# intern8
```intern8``` is an automated tool which use **[Ngrok](https://ngrok.com/)** to connect your Linux embedded device to the internet.

## Why intern8 ?
It is **too long** to type ```ngrok tcp 22``` everytime you want to **connect your device** to the **internet**. So I created this tool to **automate** the **process**. You can add it as a **cron job** to **automatically connect your device**. (This is why It was created, as my own IP address changes every 24 hours)

It also, if you want, **sends** the ngrok link to **Discord** or **Slack** using **Webhooks**. 

## Output example
![intern8 output](img/output.png?raw=true "intern8 output example")

## Installation
```py
pip install -r requirements.txt
```

You will also need to install [Ngrok](https://ngrok.com/download) and add it to your PATH.

## Usage
```py
python3 intern8/src/intern8.py -h

usage: intern8.py [-h] [-w [W]] [-u [U]]

optional arguments:
  -h, --help  show this help message and exit
  -w [W]      Activate or not Webhook (Default is 0)
  -u [U]      Webhook URL


python3 src/intern8.py -w 1 -u https://discord.com/api/webhooks/123456789/123456789
```

## Contributing
Feel free to create a pull request if you want to add something to the project. I'll be happy to review it. :)

## License
[MIT](https://choosealicense.com/licenses/mit/)