import base64
from typing import Dict, NamedTuple
import requests
import json
from .constants import *


def recursive_to_json(obj : NamedTuple) -> Dict:
    _json = {}
    if isinstance(obj, tuple):
        datas = obj._asdict()
        for data in datas:
            if isinstance(datas[data], tuple):
                _json[data] = (recursive_to_json(datas[data]))
            else:
                _json[data] = (datas[data])
    return _json


def create_request(filepath : str) -> Dict:
    request = RecognizeRequest(
        config=RecognitionConfigShort(
            encoding='FLAC',
            languageCode='ru-RU',
            profanityFilter=True,
        ),
        audio=RecognitionAudioShort(
            content=str(filepath)
        )
    )
    return recursive_to_json(request)


def parse_google_response(response : json) -> str:
    text = ''
    if response.get('error'):
        print("Please only send audios that are no longer than 1 minute")
    else:
        for i in range(len(response["results"])):
            if response['results'][i]['alternatives'][0]['confidence'] > CONFIDENT_ENOUGH:
                text += response['results'][i]['alternatives'][0]['transcript']
                return text


def send_request2google(req : Dict) -> str: #send data to google
    r = (requests.post(url = f'https://speech.googleapis.com/v1/speech:recognize?alt=json&key={API_KEY}', data = json.dumps(req))) #idc
    return parse_google_response(r.json())


def data_to_base64(filepath : str):
    file = open(filepath, 'rb')
    data = base64.b64encode(file.read()).decode('ascii')
    return data


def transcribe(path2file : str):
    form = create_request(data_to_base64(path2file))
    google_response = send_request2google(form)
    if google_response:
        return google_response

