from flask import Flask, request, render_template

import numpy as np
import math

import json


app = Flask(__name__)

def get_json():
    if (request.json != None):
        return request.json
    elif (request.data != None and request.data.decode("utf8") != u''):
        return json.loads(request.data.decode("utf8"))


@app.route("/", methods = ['GET'])
def index():
    return render_template("index.html")

@app.route("/calculate", methods = ['POST'])
def calculate():
    #expects the json data to be in the form
    #{"variable_margin": [day1, day2, day3 ...]
    #returns json in format {"mean":123, "std_dev":123,"mean_ln":123, "std_lm":123}
    package = get_json()
    data = np.array(package['variable_margin'])
    result = {}

    #sample standard deviation since that is what is being used in the excel
    mean = data.mean()
    std = data.std(ddof=1)
    result['mean']= mean
    result['std_dev'] = std
    result['mean_ln'] = math.log(mean**2/((mean**2-std**2)**.5))
    result['std_ln'] = (math.log(1+((std**2)/(mean**2))))**0.5

    js = json.dumps(result)
    encoded_js = js.encode('utf8')

    #if any of the numbers are NaN, this will break the js code

    return app.response_class(response=encoded_js, mimetype='application/json')


if __name__=="__main__":
    app.run(debug=True)