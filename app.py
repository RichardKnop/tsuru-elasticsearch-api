import json
import socket
import fcntl
import struct
from flask import Flask


app = Flask(__name__)


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


@app.route("/resources", methods=["POST"])
def add_instance():
    return '', 201


@app.route("/resources/<name>", methods=["DELETE"])
def remove_instance(name):
    return "", 200


@app.route("/resources/<name>/bind-app", methods=["POST"])
def bind_app(name):
    envs = {
        "ELASTICSEARCH_HOST": get_ip_address('eth0'),
        "ELASTICSEARCH_PORT": '9200',
    }
    return json.dumps(envs), 201


@app.route("/resources/<name>/bind", methods=["POST"])
def bind_app(name):
    return "", 201


@app.route("/resources/<name>/bind-app", methods=["DELETE"])
def unbind_app(name):
    return "", 200


@app.route("/resources/<name>/bind", methods=["DELETE"])
def unbind_app(name):
    return "", 200


@app.route("/resources/<name>/status", methods=["GET"])
def status(name):
    # check the status of the instance named "name"
    return "", 204


if __name__ == "__main__":
    app.run()
