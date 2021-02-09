#! /usr/bin/env python
import os
import sys
import requests
import argparse
from dotenv import load_dotenv
from urllib.parse import urlunsplit, urlsplit


def createParser():
    parser = argparse.ArgumentParser(description='Программа для API Bitly')
    parser.add_argument("link", help="Ваша ссылка")
    return parser


def get_bitlink(split_link, bitly_api_token, group_guid="Bj84ivi7pJW", domain="bit.ly", title="YfffTest"):
    unsplit_link = split_link.geturl()
    access_token = f"Bearer {bitly_api_token}"
    headers = {"Authorization": access_token}
    payload = {"long_url": unsplit_link, "group_guid": group_guid, "domain": domain, "title": title}
    response = requests.post("https://api-ssl.bitly.com/v4/bitlinks", headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["link"]


def get_clicks(unsplit_link, bitly_api_token, period="day"):
    access_token = f"Bearer {bitly_api_token}"
    headers = {"Authorization": access_token}
    payload = {"unit": period, "units": "-1", "unit_reference": ""}
    response = requests.get(f"https://api-ssl.bitly.com/v4/bitlinks/{unsplit_link}/clicks/summary", headers=headers, params=payload)
    response.raise_for_status()
    return response.json()["total_clicks"]


def verify_bitlink(unsplit_link, bitly_api_token):
    access_token = f"Bearer {bitly_api_token}"
    headers = {"Authorization": access_token}
    response = requests.get(f"https://api-ssl.bitly.com/v4/bitlinks/{unsplit_link}", headers=headers)
    return response.ok


if __name__ == "__main__":
    load_dotenv()
    bitly_api_token = os.getenv("API_TOKEN")
    parser = createParser()
    input_args = parser.parse_args()
    input_link = input_args.link
    split_link = urlsplit(input_link)
    unsplit_link = split_link.netloc + split_link.path
    if verify_bitlink(split_link, bitly_api_token):
        print(get_clicks(split_link, bitly_api_token))
    else:
        print(get_bitlink(split_link, bitly_api_token))
