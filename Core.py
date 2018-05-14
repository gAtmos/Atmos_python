from Drivers.OnOff import OnOff
from RepeatedTimer import RepeatedTimer

from threading import Thread
from time import sleep, time
import json
import datetime


class Core():
    def __init__(self, config="config/config.json"):
        self.config = {}
        self.components = []

        # time control
        self.running = False
        self.loopThread = None

        self.loadConfig(config)
        self.buildSystem()

    def loadConfig(self, config="config/config.json"):
        with open(config, "r") as f:
            self.config = json.load(f)

    def buildSystem(self):
        """
        Create the necessary drivers to run the system describe by the configuration file
        :return:
        """
        self.components = []

        for component in self.config:
            if self.config[component]["driver"] == "on_off":
                self.components.append(OnOff(component, self.config[component]))

    def start(self):
        if not self.running:
            self.running = True
            self.loopThread = Thread(target=self._run)
            self.loopThread.start()

    def stop(self):
        if self.running:
            self.running = False
            self.loopThread.cancel()

    def _run(self):
        while self.running:
            self.__checkEvent()

            sleep(1 - (time() % 1))

    def __checkEvent(self):
        currentTime = datetime.datetime.now().strftime('%H:%M:%S')

        cpt = 0
        for comp in self.components:
            if comp.checkEvent(currentTime):
                print("Must execute following component: ", comp.name)
                cpt += 1

        if cpt == 0:
            print("no event")


if __name__ == '__main__':
    core = Core()

    core.start()
