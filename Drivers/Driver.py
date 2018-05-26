class Alarm:
    def __init__(self, timeStr: str, args: dict):
        self.hour = timeStr[0]
        self.minute = timeStr[1]
        self.seconde = timeStr[2]
        self.kwargs = args

    def isValid(self, timeStr: str):
        time = timeStr.split(":")

        if time[0] == self.hour and time[1] == self.minute and time[2] == self.seconde:
            return True

        return False

    def __str__(self):
        return "%s:%s:%s" % (self.hour, self.minute, self.seconde)

class Driver:
    """
    A driver is a component that is composed of an alarm (timer and type
    """
    def __init__(self, name, config: dict):
        self.name = name
        self.config = config
        self.alarms = []

        # hardwarre component
        self.output = []
        self.input = []

        # driver general initialization
        self.__loadGeneralConfig()

    def __call__(self, **kwargs):
        raise NotImplementedError

    def __loadGeneralConfig(self):
        self.output = self.config["output"]
        self.input = self.config["input"]


    def checkEvent(self, timeStr: str):
        for alarm in self.alarms:
            if alarm.isValid(timeStr): return True

        return False

    def _checkConfigIsValid(self):
        areTimersOk = self._checkTimers(self.config["timers"])

        return areTimersOk

    def _checkTimers(self, timers: list):
        """
        Check if the timers describe in the configuration files are well made, A ruler is describe using the following
        syntax: hh:mm:ss (h -> hours, m -> minutes, s -> seconds). The timers must respect the following commands:
        . off command should always been after the on com<mand
        . an off command should always been call after a on command

        :param on the time when the component should be turn on
        :param off the time when the component should be turn off
        :return true if every rules are respected. False otherwise
        """
        for tpl in timers:
            if len(tpl) != 2 and (not "on" in tpl or not "off" in tpl): return False

            on_split = tpl["on"].split(":")
            off_split = tpl["off"].split(":")

            # chech the on / off order
            if (int(off_split[0]) - int(on_split[0]) < 0): return False
            if (int(off_split[1]) - int(on_split[1]) < 0): return False
            if (int(off_split[2]) - int(on_split[2]) < 0): return False

        # chech presence of off command after an on
        return True

    def __setTimer(self):
        raise NotImplementedError
