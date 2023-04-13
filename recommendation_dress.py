import os
import openai
import requests
import json
from bs4 import BeautifulSoup

# PROMPT = "a woman's dress good for rainy and humid days is not draw is real picture"
openai.api_key = "OPENAI_API_KEY"

#-------ChatGPT
def generate_response(prompt):
  URL = "https://api.openai.com/v1/chat/completions"

  payload = {
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": f"{prompt}"}],
    "temperature": 1.0,
    "top_p": 1.0,
    "n": 1,
    "stream": False,
    "presence_penalty": 0,
    "frequency_penalty": 0,
  }

  headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {openai.api_key}"
  }

  response = requests.post(URL, headers=headers, json=payload, stream=False)
  resp = json.loads(response.content)
  return resp['choices'][0]['message']['content']

#-------Genrate Dress with Dall-e
def generate_image(recommend):

  response = openai.Image.create(
      prompt=recommend,
      n=1,
      size="256x256",
  )

  print(response["data"][0]["url"])

  ## save
  # response = openai.Image.create(
  #   prompt=PROMPT,
  #   n=1,
  #   size="256x256",
  #   response_format="b64_json",
  # )
  #
  # print(response["data"][0]["b64_json"][:50])

#-------Naver Weather Parsing
def weather_parser():
  url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EB%82%A0%EC%94%A8'

  response = requests.get(url)

  soup = BeautifulSoup(response.content, 'html.parser')

  temp = soup.find('div', {'class': 'temperature_text'}).text
  summary = soup.find('dl', {'class': 'summary_list'}).text

  weather = f'{temp}{summary}'
  return weather

def main():
  pass

if __name__ == '__main__':
    main()

