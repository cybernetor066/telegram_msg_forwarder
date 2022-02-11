from logging import exception
import os, sys, time, datetime, re, requests, zipfile, random
from datetime import datetime as dt
from urllib.request import urlopen as ureq
from sys import platform
from bs4 import BeautifulSoup as bs
import pandas as pd
from openpyxl import load_workbook
from queue import Queue
import threading, concurrent.futures
from deathbycaptcha import deathbycaptcha

# Using the Telethon telegram api
import json, configparser
from telethon.sync import TelegramClient, events
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import PeerChannel

# New imports(For Group Scraping)
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty

# New imports(For adding scraped users to group)
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest


# Accessing files in directories
if getattr(sys, 'frozen', False):
    # running in a bundled form
    base_dir = sys._MEIPASS # pylint: disable=no-member
else:
    # running normally
    base_dir = os.path.dirname(os.path.abspath(__file__))

# Locating helper files in the current working directory
config_file_path = os.path.join(base_dir, 'config.ini')




# Reading the configs
config = configparser.ConfigParser()
config.read(config_file_path)


# # Set print direction
# log_file = os.path.join(base_dir, 'logs.txt')
# sys.stdout = open(log_file, 'w')


# Then setting our config values
app_name = config['Telegram']['app_name']
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
api_hash = str(api_hash)
bot_token = config['Telegram']['bot_token']

phone_no = config['Telegram']['phone_no']
username = config['Telegram']['username']

destination_group_invite_link = config['Telegram']['tg_group_link']
destination_group_invite_link = str(destination_group_invite_link)

# # Confirmation
# print(app_name)
# print(api_id, api_hash, bot_token)
# print(phone_no, username)
# print(destination_group_invite_link)


# Create the client and connect
client = TelegramClient(username, api_id, api_hash)
client.start()
print("Client Created")
# Ensure you're authorized
if not client.is_user_authorized():
    client.send_code_request(phone_no)
    try:
        client.sign_in(phone_no, input('Enter the code: '))
    except SessionPasswordNeededError:
        client.sign_in(password=input('Password: '))


print('Connection successfull!')






# *********************************************************************************************************
# *********************************************************************************************************
# *********************************************************************************************************
# Listen to msgs in your telegram account and forward message to group(s)
entity=client.get_entity(destination_group_invite_link)

# @client.on(events.NewMessage)
@client.on(events.NewMessage(from_users='HarmonicsAppBot'))
async def my_event_handler(event):
    # print('{}'.format(event))
    get_message = event.message.to_dict()
    # real_msg = get_message["message"]
    # print(f'Dict message received from bot is: {get_message}')
    # print(f'message received from bot is: {real_msg}')

    # message_json = json.dumps(get_message)
    # print(f'Json message received from bot is: {message_json}')

    # await client.send_message(entity=entity,message=event.raw_text)
    await client.send_message(entity=entity,message=event.message)
    print('Msg forwarded successfully!')




client.start()
client.run_until_disconnected()



















