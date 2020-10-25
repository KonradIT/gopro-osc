from goprocam import GoProCamera, constants

goproOSCMap = {
    "camera.setOptions": {"name": "gpControlSet"},
    "camera.takePicture": {"name": "take_photo()"},
    "camera.startCapture": {"name": "shutter(constants.start)"},
    "camera.stopCapture": {"name": "shutter(constants.stop)"}

}

isoLevels = {
    100: "constants.{}.IsoLimit.ISO100",
    200: "constants.{}.IsoLimit.ISO200",
    400: "constants.{}.IsoLimit.ISO400",
    800: "constants.{}.IsoLimit.ISO800",
    1600: "constants.{}.IsoLimit.ISO1600"
}

expCompLevels = {
    -2: "constants.{}.EvComp.M2",
        -1.5: "constants.{}.EvComp.M1_5",
        -1: "constants.{}.EvComp.M1",
        -0.5: "constants.{}.EvComp.M0_5",
    0: "constants.{}.EvComp.Zero",
    2: "constants.{}.EvComp.P2",
    1.5: "constants.{}.EvComp.P1_5",
    1: "constants.{}.EvComp.P1",
    0.5: "constants.{}.EvComp.P0_5",
}

whiteBalanceLevels = {
    "auto": "constants.{}.EvComp.M2",
    "incandescent": "constants.{}.EvComp.M2",
    "fluorescent": "constants.{}.EvComp.M2",
    "daylight": "constants.{}.EvComp.M2",
    "cloudy-daylight": "constants.{}.EvComp.M2",
    "shade": "constants.{}.EvComp.M2"
}
