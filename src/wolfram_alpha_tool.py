import os
import requests
from transformers import Tool

class WolframAlpha(Tool):
    name = "wolfram_alpha"
    description = ("This is a tool that uses WolframAlpha to compute any mathematical query. It takes one input query, and returns a verbose result in xml format, which includes the solution.")

    inputs = ["query"]
    outputs = ["result"]

    def __init__(self, *args, **kwargs):
        self.base_url = 'http://api.wolframalpha.com/v2/query'

        self.app_id = os.environ.get('WOLFRAM_APP_ID')
        if self.app_id is None:
            raise ValueError("Please set the `WOLFRAM_APP_ID` as an environment variable in order to instantiate the Wolfram tool.\nTo do so, before instantiating the class, run:\nos.environ['WOLFRAM_APP_ID'] = 'YOUR_WOLFRAM_APP_ID'")

        print("Making sure APP_ID is valid... ", end="")
        dummy_params = {
            'input': '1+1',
            'output': 'xml',
            'appid': self.app_id,
        }
        response = self.make_request(params=dummy_params)
        if "Invalid appid" in response:
            appid_url = 'https://developer.wolframalpha.com/portal/myapps/index.html'
            raise ValueError(f"Please set a valid `WOLFRAM_APP_ID` as an environment variable.\nWolframAlpha is not validating APP_ID: {self.app_id}\nTo get an APP_ID, go to:\n{appid_url}\nand click on [Get an AppID]")
        print("APP_ID validated! Tool ready to use.")

    def __call__(self, query, output='xml', pod_format='plaintext'):
        

        output_opts = ['xml','json']
        format_opts = ['plaintext', 'image', 'image,imagemap', 'mathml', 'sound', 'wav']

        if output not in output_opts:
            return f"{output} is not a correct output parameter! It must be one of these: {output_opts}"

        if pod_format not in format_opts:
            return f"{pod_format} is not a correct pod_format parameter! It must be one of these: {format_opts}"

        params = {
            'input': query,
            'output': output,
            'appid': self.app_id,
        }
        
        response = self.make_request(params)

        return response
    
    def make_request(self, params):
        response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
            if params['output'] == 'xml':
                return response.text
            elif params['output'] == 'json':
                # Remove unnecessary empty spaces
                return str(response.json())
        else:
            return f"There was an error with the request, with response: {response}"