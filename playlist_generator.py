import os
from urllib.request import Request
import google.auth
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from google_auth_oauthlib import flow
import requests
import json
import openai
import webbrowser
import pandas as pd
from bs4 import BeautifulSoup

openai.api_key = "api_key"

def generate_response(weather, mood, genre, number, country):

    URL = "https://api.openai.com/v1/chat/completions"

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user",
                      "content": f"You are an AI tool that recommends songs based on the weather and the user's mood."
                                 f"Users will give user weather, current mood, genre user want, number of songs user want, and country information user want."
                                 f"Based on this information, please organize the title of the singer and song."
                                 f"Please answer in the same format as 'Song title - Singer'."
                                 f"The information provided by the user is as follows."
                                 f"user weather: {weather}"
                                 f"current mood: {mood}"
                                 f"genre user want: {genre}"
                                 f"number of songs user want: {number}"
                                 f"country information user want: {country}"}],
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


def weather_parser():
    url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EB%82%A0%EC%94%A8'

    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')

    temp = soup.find('div', {'class': 'temperature_text'}).text
    summary = soup.find('dl', {'class': 'summary_list'}).text

    weather = f'{temp}{summary}'
    return weather

# Set up YouTube API credentials
CLIENT_SECRETS_FILE = 'client_secret.json'
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

# Authenticate the user and build the YouTube API client
def get_authenticated_service():
    auth_flow = flow.InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = auth_flow.run_local_server(port=0)
    credentials = service_account.Credentials.from_service_account_file(
        "youtube-api-practice-383016-60d0496991b8.json", scopes=SCOPES)
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


# Get the YouTube video ID for a given song
def get_video_id(title, artist):
    query = f"{title} {artist} official video"
    api_key = "YOUTUBE-API-KEY"
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&key={api_key}&maxResults=1&type=video"
    response = requests.get(url)
    json_data = json.loads(response.text)
    video_id = json_data['items'][0]['id']['videoId']
    return video_id

# Create a new private playlist on YouTube
def create_playlist(youtube, title):
    try:
        playlists_insert_response = youtube.playlists().insert(
            part="snippet,status",
            body=dict(
                snippet=dict(
                    title=title,
                    description="A playlist created with the YouTube API v3"
                ),
                status=dict(
                    privacyStatus="private"
                )
            )
        ).execute()

        return playlists_insert_response["id"]

    except HttpError as error:
        print("An error occurred: %s" % error)
        return None

# Add a video to a YouTube playlist
def add_video_to_playlist(youtube, video_id, playlist_id):
    try:
        add_video_request=youtube.playlistItems().insert(
            part="snippet",
            body=dict(
                snippet=dict(
                    playlistId=playlist_id,
                    resourceId=dict(
                        kind="youtube#video",
                        videoId=video_id
                    )
                )
            )
        ).execute()

        return add_video_request
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None

# Create a new YouTube playlist and add all songs in the dictionary to it
def create_and_add_songs_to_playlist(playlist_title, songs):
    # Authenticate the user and build the YouTube API client
    youtube = get_authenticated_service()

    # Create a new private playlist on YouTube
    playlist_id = create_playlist(youtube, f"{playlist_title}")

    # Add each song in the dictionary to the playlist
    for title, artist in songs.items():
        video_id = get_video_id(title, artist)
        add_video_to_playlist(youtube, video_id, playlist_id)

    playlist_url = f"https://www.youtube.com/playlist?list={playlist_id}"


    print("All songs added to the playlist!")
    print(f"{playlist_url}")



def main():
    playlist_title = input("playlist title: ")


    weather = weather_parser()
    mood = input("현재 기분: ")
    genre = input("원하는 장르: ")
    country = input("원하는 국가: ")
    number = input("원하는 곡 수: ")


    response = generate_response(weather, mood, genre, number, country)
    texts = response.split('\n')
    print(response)
    print(texts)

    result = []
    for item in texts:
        if item and item[0].isdigit():
            result.append(item)


    songs = {}
    for text in result:
        title = text.split(' ')[1]
        artist = text.split(' ')[-1]
        dic = {title: artist}
        songs.update(dic)

    create_and_add_songs_to_playlist(playlist_title, songs)

if __name__ == '__main__':
    main()