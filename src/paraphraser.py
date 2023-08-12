# -*- coding: utf-8 -*-

import requests
import json
import urllib.parse
from paraphraser_exceptions.para_exceptions import InvalidModeError, LanguageNotSupportedError
from urllib.error import HTTPError, URLError
from requests.exceptions import JSONDecodeError, ConnectTimeout, ConnectionError, ReadTimeout, ContentDecodingError


def langs():
    with open("text_paraphraser/artifacts/supported_langs.json", "r") as supported_languages:
        langs = json.load(supported_languages)
    return langs


supported_langs = langs()

class Paraphraser:
    def __init__(self, _text, _mode, _lang):
        self._text = _text
        self._mode = _mode
        self._lang = _lang

    def paraphrase(self):
        mode = {
            1: "Fluency",
            2: "Standard"
        }
        params = {
            "data": self._text,
            "mode": self._mode,
            "lang": self._lang,
            "captcha": ""
        }
        errors = []
        if self._mode not in mode.keys():
            errors.append(InvalidModeError(
                f"Only two summarization modes allowes one of: {list(mode.keys())}, given '{self._mode}' instead."))
        if type(self._text) != str:
            errors.append(TypeError(
                f"Expected input of type {str} for '_text', received '{type(self._text)}' instead."))
        if type(self._lang) != str:
            errors.append(TypeError(
                f"Expected input of type {str} for '_lang', received '{type(self._lang)}' instead."))
        if len(self._lang.strip()) == 0:
            errors.append(ValueError(
                f"'_lang' parameter cannot be empty. Give default value 'en'."))
        if self._lang not in supported_langs.values():
            errors.append(LanguageNotSupportedError(
                f"'_lang' can only be one of {list(supported_langs.values())}, received '{self._lang}' instead."))

        output = {}

        if len(errors) != 0:
            output["Parameter Errors"] = True
            output["Parameter Errors - Dictionary"] = {type(errors[index]).__name__: str(
                errors[index]) for index in range(len(errors))}
            output["Connection Errors"] = ""
            output["Connection Errors - Dictionary"] = {}
            output["Paraphrased Text"] = ""
            return output
        else:
            output["Parameter Errors"] = False
            output["Parameter Errors - Dictionary"] = {}
            connection_errors = []
            try:
                url = "https://www.paraphraser.io/frontend/rewriteArticleBeta"
                payload = urllib.parse.urlencode(params)
                headers = {
                    'authority': 'www.paraphraser.io',
                    'accept': 'application/json, text/javascript, */*; q=0.01',
                    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'origin': 'https://www.paraphraser.io',
                    'referer': 'https://www.paraphraser.io/',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'x-requested-with': 'XMLHttpRequest'
                }
                response = requests.request(
                    "POST", url, headers=headers, data=payload).json()
                text = response["result"]["paraphrase"]
                replace = [("<span class='sw'>", ""), ("</span>", ""), ("<b>", ""),
                           ("</b>", ""), ("<br>", ""), ("</br>", "")]
                [text := text.replace(a, b) for a, b in replace]
                paraphrased_text = text
            except HTTPError:
                connection_errors.append(HTTPError("Client Error Occured."))
            except URLError:
                connection_errors.append(URLError(
                    "Either URL entered is incorrect or there is an internet connectivity issue."))
            except ConnectionError:
                connection_errors.append(ConnectionError(
                    "Connection error occured while sending request to the target site."))
            except ContentDecodingError:
                connection_errors.append(ContentDecodingError(
                    "Python web request content decoding failed."))
            except JSONDecodeError:
                connection_errors.append(
                    JSONDecodeError("Failed to decode json data."))
            except ConnectTimeout:
                connection_errors.append(ConnectTimeout(
                    "Request timed out while connecting to the remote server."))
            except ReadTimeout:
                connection_errors.append(ReadTimeout(
                    "Server failed to send data in allocated time."))
            if len(connection_errors) == 0:
                output["Connection Errors"] = False
                output["Connection Errors - Dictionary"] = {}
                output["Paraphrased Text"] = paraphrased_text
                return output
            else:
                output["Connection Errors"] = True
                output["Connection Errors - Dictionary"] = {type(connection_errors[index]).__name__: str(
                    connection_errors[index]) for index in range(len(connection_errors))}
                output["Paraphrased Text"] = ""
                return output


def paraphrase(text, mode, lang):
    paraphrase_text = Paraphraser(
        _text=text, _mode=mode, _lang=lang).paraphrase()
    text = paraphrase_text["Paraphrased Text"].strip()
    if len(text) != 0:
        return text
    else:
        return paraphrase_text