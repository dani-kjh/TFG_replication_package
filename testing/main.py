import requests
import json
from datetime import datetime
import os
import sys
import numpy

RESULTS_PATH = "../results"


class MakeApiCall:
    def formatted_print(self, obj):
        text = json.dumps(obj, sort_keys=True, indent=4)
        print(text)

    def get_results(self, api, tag, latencies):
        url = api + "/results"
        response = requests.get(url)
        current_datetime = datetime.now().strftime("%Y-%m-%d;%H:%M:%S")
        if response.status_code == 200:
            print("sucessfully fetched the data")
            output_path = os.path.join(RESULTS_PATH, tag, current_datetime)
            if not (os.path.isdir(output_path)):
                os.makedirs(output_path)
            # Save codecarbon logs
            with open(os.path.join(output_path, "API_results.csv"), "wb") as file:
                file.write(response.content)

            # Save latencies into csv
            numpy.savetxt(os.path.join(output_path, "latency_results.csv"), latencies, delimiter=",", header="latency")
        else:
            print(f"Hello person, there's a {response.status_code} error with your request")

    def make_requests(self, api, sentences):
        url = api + "/invocations"
        requests_latency = []
        it = 0
        for sentence in sentences:
            myobj = {"language": "German", "text": sentence}
            response = requests.post(url, json=myobj)
            if response.status_code == 200:
                print("sucessfully fetched the data with parameters provided")
                self.formatted_print(response.json())
                requests_latency.append(response.elapsed.total_seconds())
                print("Latency in seconds of the request[" + str(it) + "]: " + str(response.elapsed.total_seconds()))
            else:
                print(f"Hello person, there's a {response.status_code} error with your request")
            it = it + 1

        return requests_latency

    def __init__(self):

        sentences_to_post = []
        with open("sentences.txt") as my_file:
            sentences_to_post = my_file.read().splitlines()

        cloud_providers = [
            ["https://azurehuggingfacetranslator.azurewebsites.net", "azure"],
            ["https://docker-fastapi-translator.herokuapp.com", "heroku"],
            ["https://awsfastapitext-production.up.railway.app", "railway"],
            ["", "aws"],
        ]
        for provider in cloud_providers:
            print("Requesting provider: " + provider[1])
            latencies = self.make_requests(provider[0], sentences_to_post)
            self.get_results(provider[0], provider[1], latencies)


if __name__ == "__main__":
    api_call = MakeApiCall()
