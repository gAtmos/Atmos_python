from Drivers.Driver import Driver


class OnOff_Alarm:
    def __init__(self, timeStr: str, type: str):
        self.hour = timeStr[0]
        self.minute = timeStr[1]
        self.seconde = timeStr[2]
        self.type = type

    def isValid(self, timeStr: str):
        time = timeStr.split(":")

        if time[0] == self.hour and time[1] == self.minute and time[2] == self.seconde:
            return True

        return False

    def __str__(self):
        return "%s %s:%s:%s" % (self.type, self.hour, self.minute, self.seconde)


class OnOff(Driver):
    def __init__(self, name, config: dict):
        Driver.__init__(self, name)
        self.config = config
        self.alarms = []

        if self._checkConfigIsValid(config):
            self.__setTimer()
        else:
            raise Exception("Config not available for driver: %s" % self.name)

    def __setTimer(self):
        for tpl in self.config["timers"]:
            self.alarms.append(OnOff_Alarm(tpl["on"].split(":"), "on"))
            self.alarms.append(OnOff_Alarm(tpl["off"].split(":"), "off"))

    def checkEvent(self, timeStr: str):
        for alarm in self.alarms:
            if alarm.isValid(timeStr): return True

        return False

    def __str__(self):
        msg = "\n"
        msg += self.name + "\n"
        msg += "driver: on_off\n"
        for a in self.alarms:
            msg += str(a) + "\n"
        return msg
