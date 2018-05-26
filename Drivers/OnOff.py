from Drivers.Driver import Driver
from Drivers.Driver import Alarm

class OnOff(Driver):
    def __init__(self, name, config: dict):
        Driver.__init__(self, name, config)

        if self._checkConfigIsValid():
            self.__setTimer()
        else:
            raise Exception("Config not available for driver: %s" % self.name)

    def __call__(self, args: dict):
        print("Executing OnOff driver with following args: ")
        print(args["action"])

    def __setTimer(self):
        for tpl in self.config["timers"]:
            self.alarms.append(Alarm(tpl["on"].split(":"), {"action": "on"}))
            self.alarms.append(Alarm(tpl["off"].split(":"), {"action": "off"}))

    def checkEvent(self, timeStr: str):
        for alarm in self.alarms:
            if alarm.isValid(timeStr): return alarm.kwargs

        return False

    def __str__(self):
        msg = "\n"
        msg += self.name + "\n"
        msg += "driver: on_off\n"
        for a in self.alarms:
            msg += str(a) + "\n"
        return msg
