from flask import Flask, render_template, request
import ssl
import os 
import json
import urllib.request

app = Flask(__name__, template_folder='templates')

@app.route('/', methods=['GET', 'POST'])
def handle_form():
    if request.method == 'POST':
        query = request.form.get('user-input')
        if query:
            data = {"query": f"{query}"}

            body = str.encode(json.dumps(data))

            url = 'https://satyakebakshi95-1243-wowxp.eastus2.inference.ml.azure.com/score'

            api_key = 'XRslYLl7ptUEI1bFWYci2L4eP6AsIfJf'
            if not api_key:
                raise Exception("A key should be provided to invoke the endpoint")

            headers = {'Content-Type': 'application/json', 'Authorization': ('Bearer ' + api_key), 'azureml-model-deployment': 'satyakebakshi95-1243-wowxp-1'}

            req = urllib.request.Request(url, body, headers)

            try:
                response = urllib.request.urlopen(req)
                result = response.read()
                result_json = json.loads(result.decode('utf-8'))
                reply = result_json['reply']
                return render_template('chatbot.html', reply=reply)

            except urllib.error.HTTPError as error:
                print("The request failed with status code: " + str(error.code))
                print(error.info())
                print(error.read().decode("utf8", 'ignore'))
                return render_template('chatbot.html', error="There was an error processing your request.")
        else:
            return render_template('chatbot.html', error="No query provided.")
    
    return render_template('chatbot.html')

if __name__ == '__main__':
    app.run(debug=True)
a