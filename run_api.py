from flask import Flask,  request, Response
from werkzeug.serving import run_simple

from kafka_producer import Producer
from settings.url_crawler_settings import SETTINGS, NEW_URLS_TOPIC
from proto_message import UrlsMessage


def get_app():
    app = Flask(__name__, static_folder="templates/static")

    @app.route("/add_urls", methods=['POST'])
    def api():
        if request.headers['Content-Type'] == 'application/json':
            data = request.json
            if not data.get('urls'):
                return "Url list should map with 'urls' field"
            elif not isinstance(data.get('urls'), list):
                return "'urls' field should map with a list"
            else:
                urls = data['urls']
                producer.send_message(NEW_URLS_TOPIC, UrlsMessage.serialize(UrlsMessage(urls=urls)))
                return Response(status=200)
        else:
            return "Not expected data format."

    return app


if __name__ == '__main__':
    producer = Producer(bootstrap_servers=SETTINGS['BOOTSTRAP_SERVERS'])
    run_simple('localhost', 5000, get_app(), use_reloader=True, use_debugger=True, use_evalex=True)
