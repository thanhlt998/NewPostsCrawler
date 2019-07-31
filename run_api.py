from flask import Flask, request, Response
from werkzeug.serving import run_simple

from kafka_producer import Producer
from settings.url_crawler_settings import SETTINGS, NEW_URLS_TOPIC
from settings.api_settings import BIND_ADDRESS, BIND_PORT, REDIS_SERVER, MYSQL_DB
from proto_message import UrlsMessage
from redis_server import RedisServer
from connection import MysqlConnection


def get_app():
    app = Flask(__name__)

    @app.route("/add_urls", methods=['POST'])
    def api():
        if request.headers['Content-Type'] == 'application/json':
            data = request.json
            if not data.get('urls'):
                return Response("Url list should map with 'urls' field", status=500)
            elif not isinstance(data.get('urls'), list):
                return Response("'urls' field should map with a list", status=500)
            else:
                urls = data['urls']
                producer.send_message(NEW_URLS_TOPIC, UrlsMessage.serialize(UrlsMessage(urls=urls)))
                return Response(status=200)
        else:
            return Response("Not expected data format.", status=500)

    @app.route("/add_domains", methods=['POST'])
    def add_domain():
        if request.headers['Content-Type'] == 'application/json':
            data = request.json
            if not data.get('domains'):
                return Response("domain list should map with 'domains' field", status=500)
            elif not isinstance(data.get('domains'), list):
                return Response("'domains' field should map with a list", status=500)
            else:
                domains = data['domains']
                # import domain into mysql
                domain_ids = []
                for domain in domains:
                    domain_id = connection.insert_new_domain(domain)
                    if domain_id != 0:
                        domain_ids.append(domain_id)
                # put domain_id into redis queue
                for domain_id in domain_ids:
                    redis.insert_domain('domain_ids', domain_id)
                redis.set_no_domains(redis.get_no_domains() + len(domain_ids))
                return Response(status=200)
        else:
            return Response("Not expected data format.", status=500)

    @app.route("/remove_domains", methods=['DELETE'])
    def remove_domains():
        if request.headers['Content-Type'] == 'application/json':
            data = request.json
            if not data.get('domains'):
                return Response("domain list should map with 'domains' field", status=500)
            elif not isinstance(data.get('domains'), list):
                return Response("'domains' field should map with a list", status=500)
            else:
                domains = data['domains']
                # get domain_ids
                domain_ids = connection.get_domain_id_list_with_domain_names(domains)
                redis.remove_domains('domain_ids', domain_ids)

                return Response(status=200)
        else:
            return Response("Not expected data format.", status=500)

    return app


if __name__ == '__main__':
    producer = Producer(bootstrap_servers=SETTINGS['BOOTSTRAP_SERVERS'])
    redis = RedisServer(REDIS_SERVER['host'], REDIS_SERVER['port'], REDIS_SERVER['db'])
    connection = MysqlConnection(host=MYSQL_DB['host'], user=MYSQL_DB['user'], password=MYSQL_DB['password'],
                                 db=MYSQL_DB['db'])
    run_simple(BIND_ADDRESS, BIND_PORT, get_app(), use_reloader=True, use_debugger=True, use_evalex=True)
