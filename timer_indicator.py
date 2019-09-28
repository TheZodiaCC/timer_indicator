import signal
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk
from gi.repository import AppIndicator3
from gi.repository import GObject
from threading import Thread
import time

class TimeIndicator():
    def __init__(self):
        self.app = "timer_indicator"
        iconpath = ""
        self.indicator = AppIndicator3.Indicator.new(
            self.app, iconpath, AppIndicator3.IndicatorCategory.OTHER)
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.create_menu())
        self.indicator.set_label("00-00-00", self.app)

        self.sec = 0
        self.mins = 0
        self.hours = 0

    def create_menu(self):
        menu = Gtk.Menu()
        name = Gtk.MenuItem("PyTimer")
        name.set_sensitive(False)
        menu.append(name)
        sep = Gtk.SeparatorMenuItem()
        menu.append(sep)
        start = Gtk.MenuItem('Start')
        start.connect('activate', self.start)
        menu.append(start)
        stop = Gtk.MenuItem('Stop')
        stop.connect('activate', self.stop)
        menu.append(stop)
        reset = Gtk.MenuItem('Reset')
        reset.connect('activate', self.reset)
        menu.append(reset)
        sep1 = Gtk.SeparatorMenuItem()
        menu.append(sep1)
        item_quit = Gtk.MenuItem('Quit')
        item_quit.connect('activate', self.quit)
        menu.append(item_quit)

        menu.show_all()
        return menu

    def start(self, source):
        self.update = Thread(target=self.time)
        self.update.setDaemon(True)
        self.update.start()

    def stop(self, source):
        self.dead = True

    def reset(self, source):
        if self.dead == True:
            self.sec = 0
            self.mins = 0
            self.hours = 0
            data = (f"{self.hours}-{self.mins}-{self.sec}")
            GObject.idle_add(self.indicator.set_label, data, self.app, priority=GObject.PRIORITY_DEFAULT)
        else:
            pass

    def time(self):
        self.dead = False

        while (self.dead == False):

            self.sec += 1
            time.sleep(1)

            if self.sec >= 59:
                self.sec = 0
                self.mins += 1
                time.sleep(1)
            else:
                pass

            if self.mins == 60:
                self.mins = 0
                self.hours += 1
            data = (f"{self.hours}-{self.mins}-{self.sec}")
            GObject.idle_add(self.indicator.set_label, data, self.app, priority=GObject.PRIORITY_DEFAULT)

    def quit(self, source):
        Gtk.main_quit()


if __name__ == "__main__":

    TimeIndicator()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    Gtk.main()