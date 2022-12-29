import requests
import json
from numpy import loadtxt


class MakeApiCall:

    def get_results(self, api):
        url = api + "/results"
        response = requests.get(url)
        if response.status_code == 200:
            print("sucessfully fetched the data")
            with open("results", "wb") as file:
                file.write(response.content)
        else:
            print(
                f"Hello person, there's a {response.status_code} error with your request")

    def make_requests(self, api, sentences):
        url = api + "/invocations"
        for sentence in sentences:
            myobj = {
                "language": "German",
                "text": sentence
            }
            response = requests.post(url, json = myobj)
            if response.status_code == 200:
                print("sucessfully fetched the data with parameters provided")
                self.formatted_print(response.json())
            else:
                print(
                    f"Hello person, there's a {response.status_code} error with your request")

    def formatted_print(self, obj):
        text = json.dumps(obj, sort_keys=True, indent=4)
        print(text)

    def __init__(self, api):

        sentences_to_post = []
        with open("sentences.txt") as my_file:
            sentences_to_post = my_file.read().splitlines()

        self.make_requests(api, sentences_to_post)
        self.get_results(api)


if __name__ == "__main__":
    api_call = MakeApiCall("https://docker-fastapi-translator.herokuapp.com")