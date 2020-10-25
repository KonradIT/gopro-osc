from flask import Flask, request
from goprocam import GoProCamera, constants
from dotenv import load_dotenv
import json
import hashlib
from decimal import *
import logging
import signal
import os
import commands

load_dotenv()

logging.info("Loading .env")

app = Flask(__name__)


def gpApiHandler(signum, frame):
    raise Exception("Connection timeout")


signal.signal(signal.SIGALRM, gpApiHandler)
signal.alarm(int(os.getenv("TIMEOUT")))

try:
    gopro = GoProCamera.GoPro(constants.gpcontrol)
except:
    logging.error("Error connecting to GoPro")
    exit()
finally:
    logging.info("GoPro connected")


def getState():
    goproState = dict()

    goproState["batteryLevel"] = Decimal(gopro.getStatus(
        constants.Status.Status, constants.Status.STATUS.BatteryLevel)) / Decimal(100)
    goproState["storageUri"] = gopro.getMedia()
    return goproState


@app.route("/")
def ping():
    return json.dumps({"ok": True})


@app.route("/osc/info")
def oscGetInfo():

    return json.dumps({
        "manufacturer": "GoPro",
        "model": gopro.infoCamera(constants.Camera.Name),
        "serialNumber": gopro.infoCamera(constants.Camera.SerialNumber),
        "firmwareVersion": gopro.infoCamera(constants.Camera.Firmware),
        "supportUrl": "http://github.com/KonradIT/gopro-osc/issues",
        "gps": True if gopro.infoCamera(constants.Camera.Name) == "H19.01" else False,
        "gyro": True if gopro.infoCamera(constants.Camera.Name) == "H19.01" else False,
        "uptime": 1,
        "api": [
            "/osc/info",
            "/osc/state",
            "/osc/commands/execute",
            "/osc/commands/status"
        ],
        "endpoints": {
            "httpPort": 80,
            "httpUpdatesPort": 80
        },
        "apiLevel": [2],
        "_batteryLevel": gopro.parse_value("battery", gopro.getStatus(constants.Status.Status, constants.Status.STATUS.BatteryLevel))
    })


@app.route("/osc/state")
def oscGetState():

    return json.dumps({
        "fingerprint": hashlib.md5(json.dumps(getState(), sort_keys=True)).hexdigest(),
        "state": getState(),
    })


@app.route("/osc/commands/execute", methods=["POST"])
def oscCommand():

    commandName = request.json['name']
    commandParams = request.json['parameters']

    if commandName == "camera.setOptions":
        for k in commandParams.keys():
            logging.debug("Got option name key: ", k)
            if k == "iso":
                isoLevels = commands.isoLevels
                mode = gopro.parse_value("mode", gopro.getStatus(
                    constants.Status.Status, constants.Status.STATUS.Mode)).replace("-", "")
                gopro.gpControlSet(eval("constants.{}.ISO_LIMIT").format(
                    mode), eval(isoLevels[commandParams[k]].format(
                        mode)))
            if k == "exposureCompensation":
                isoLevels = commands.expCompLevels
                mode = gopro.parse_value("mode", gopro.getStatus(
                    constants.Status.Status, constants.Status.STATUS.Mode)).replace("-", "")
                gopro.gpControlSet(eval("constants.{}.EV_COMP").format(
                    mode), eval(isoLevels[commandParams[k]].format(
                        mode)))

    return json.dumps({
        "name": commandName,
        "state": "done",
    })


if __name__ == "__main__":
    app.run("0.0.0.0")
