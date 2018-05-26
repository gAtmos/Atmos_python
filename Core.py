from Drivers.OnOff import OnOff

from threading import Thread
from time import sleep, time
import json
import datetime
import queue

class Core():
    """
    The core of the system. It role is to load the configuration file, check for potential errors, "compile" it in order
    to build all the necessary drivers that are required to run the entire atmosphere control system describe.
    Each task that must be executed are stored into a task queue of the core, and a timer, running on a separated thread,
    will check every second for action to execute.
    """
    def __init__(self, config="config/config.json"):
        self.config = {}
        self.components = []
        self.toExecute = queue.Queue()

        # time control
        self.timerRunning = False
        self.timerThread = None

        # execution control
        self.execRunning = False
        self.execThread = None

        self.loadConfig(config)
        self.buildSystem()

    def loadConfig(self, config="config/config.json"):
        with open(config, "r") as f:
            self.config = json.load(f)

    def buildSystem(self):
        """
        Create the necessary drivers to run the system describe by the configuration file
        """
        self.components = []

        for component in self.config:
            if self.config[component]["driver"] == "on_off":
                self.components.append(OnOff(component, self.config[component]))

    def startTimer(self):
        """
        Start the time into a separate thread
        """
        if not self.timerRunning:
            self.timerRunning = True
            self.timerThread = Thread(target=self._runTimer)
            self.timerThread.start()

    def stopTimer(self):
        """If running, kill the timer and stop the system"""
        if self.timerRunning:
            self.timerRunning = False
            self.timerThread.cancel()

    def _runTimer(self):
        """Infinite loop that check through all the driver for action event"""
        while self.timerRunning:
            self.__checkEvent()

            sleep(1 - (time() % 1))

    def startExec(self):
        """
        Start the thread in charge of executing the driver __call__
        """
        if not self.execRunning:
            self.execRunning = True
            self.execThread = Thread(target=self._runExecutionThread())
            self.execThread.start()

    def stopExec(self):
        if self.execRunning:
            self.execRunning = False
            self.execThread.cancel()

    def _runExecutionThread(self):
        while self.execRunning:
            try:
                comp, kwargs = self.toExecute.get(timeout=500)
                print(comp)
                print(kwargs)
                comp(kwargs)

            except TimeoutError:
                pass

    def __checkEvent(self):
        currentTime = datetime.datetime.now().strftime('%H:%M:%S')

        cpt = 0
        for comp in self.components:
            test = comp.checkEvent(currentTime)
            if type(test) is not bool:
                print("Must execute following component: ", comp.name)
                self.toExecute.put((comp, test))
                cpt += 1

        if cpt == 0:
            print("no event")


if __name__ == '__main__':
    core = Core()

    core.startTimer()
    core.startExec()
