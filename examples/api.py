# -*- coding: utf-8 -*-

from flask import Flask, Response, request, json, render_template
app = Flask(__name__)

from pollicino.config import CONFIG
from pollicino.geocoder import GeocoderClient


client = GeocoderClient.from_config(CONFIG)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/geocode/', methods=['GET'])
def gecocode():
    address = request.args.get('q')
    answer = []
    if address is not None:
        answer = client.geocode(address)

    answer = json.dumps(answer)
    return Response(answer, status=200, content_type="application/json")

if __name__ == '__main__':
    app.run()
