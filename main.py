#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import requests
import argparse
from dotenv import load_dotenv
load_dotenv()


def createParser():
  parser = argparse.ArgumentParser(
    description='Программа для API Bitly')
  parser.add_argument("link", help="Ваша ссылка")
  return parser


def get_bitlink(longer_url, token):
  access_token = "Bearer " + token
  headers = {"Authorization":access_token}
  payload = {"long_url":longer_url, "group_guid":"Bj84ivi7pJW", "domain":"bit.ly", "title":"YfffTest"}
  response = requests.post("https://api-ssl.bitly.com/v4/bitlinks", headers=headers, json=payload)
  response.raise_for_status()
  return response.json()["link"]


def get_clicks(bitlink_url, token):
  access_token = "Bearer " + token
  headers = {"Authorization":access_token}
  payload = {"unit":"day", "units":"-1", "unit_reference":""}
  response = requests.get("https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary".format(bitlink_url) , headers=headers, params=payload)
  response.raise_for_status()
  return response.json()["total_clicks"]


if __name__ == "__main__":
  parser = createParser()
  input_args = parser.parse_args(sys.argv[1:])
  api_token = os.getenv("API_TOKEN")
  input_link = input_args.link
  verify_link = input_link.startswith(("https://", "http://"))
  try:
    if verify_link == True:
      bitlink = get_bitlink(input_link, api_token)
      if bitlink is None:
        print("Ссылка некорректна")
      else:
        print(bitlink)
    elif verify_link == False:
      bitclicks = get_clicks(input_link, api_token)
      if bitclicks is None:
        print("Ссылка некорректна")
      else:
        print("Количество переходов по ссылке битли:", bitclicks)
  except requests.exceptions.HTTPError as error:
    exit("Bad link - {}".format(error))
  except ValueError:
    bitlink = None
    bitclicks = None