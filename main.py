from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.core.window import Window
from kivy.config import Config
from kivy_garden.graph import Graph, LinePlot
from kivy.clock import Clock
from threading import Thread
import audioop
import pyaudio

from math import sin
Config.set("graphics", "resizable", False)

def get_microphone_level():
    """
    source: http://stackoverflow.com/questions/26478315/getting-volume-levels-from-pyaudio-for-use-in-arduino
    audioop.max alternative to audioop.rms
    """
    chunk = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    p = pyaudio.PyAudio()

    s = p.open(format=FORMAT,
               channels=CHANNELS,
               rate=RATE,
               input=True,
               frames_per_buffer=chunk)
    global levels
    while True:
        data = s.read(chunk)
        mx = audioop.rms(data, 2)
        if len(levels) >= 100:
            levels = []
        levels.append(mx)


class Home(BoxLayout):
    pressure = ObjectProperty(None)
    flow = ObjectProperty(None)
    volumn = ObjectProperty(None)
    
    def __init__(self,):
        super(Home, self).__init__()
        self.pressure_plot = LinePlot(line_width=2, color=[1, 1, 0.3, 1])
        self.flow_plot = LinePlot(line_width=2, color=[1, 1, 0.3, 1])
        self.volumn_plot = LinePlot(line_width=2, color=[1, 1, 0.3, 1])
    
    
    def update_graph(self):
        '''
        pressure_plot.points = [(x, sin(x / 10.)) for x in range(0, 101)]
        flow_plot.points = [(x, sin(x / 10.)-0.1) for x in range(0, 101)]
        volumn_plot.points = [(x, sin(x / 10.)-0.2) for x in range(0, 101)]
        '''
        self.pressure.add_plot(self.pressure_plot)
        self.flow.add_plot(self.flow_plot)
        self.volumn.add_plot(self.volumn_plot)
        Clock.schedule_interval(self.get_value, 0.001)
    
    def get_value(self, dt):
        self.pressure_plot.points = [(i, j/5) for i, j in enumerate(levels)]
        self.flow_plot.points = [(a, b/5) for a, b in enumerate(levels)]
        self.volumn_plot.points = [(x, y/5) for x, y in enumerate(levels)]
        

class Records(GridLayout):
    pass

class Alarms(GridLayout):
    pass

class Header(BoxLayout):
    pass

class MainMenu(BoxLayout):
    pass

class VentilatorApp(App):
    def build(self):
        Window.size = (1024, 600)
        self.manager = ScreenManager(transition=FadeTransition(duration=0.15))
        
        home = Home()
        home.update_graph()
        '''
        pressure = PressurePlot()
        pressure.update_graph()
        flow = FlowPlot()
        flow.update_graph()
        volumn = VolumnPlot()
        volumn.update_graph()
        home.add_widget(pressure)
        home.add_widget(flow)
        home.add_widget(volumn)
        '''
        home_screen = Screen(name="home")
        home_screen.add_widget(home)
        
        self.manager.add_widget(home_screen)
        
        records = Records()
        records_screen = Screen(name="records")
        records_screen.add_widget(records)
        self.manager.add_widget(records_screen)
        
        alarms = Alarms()
        alarms_screen = Screen(name="alarms")
        alarms_screen.add_widget(alarms)
        self.manager.add_widget(alarms_screen)
        
        layout = GridLayout(cols=1)
        layout.add_widget(Header())
        layout.add_widget(self.manager)
        layout.add_widget(MainMenu())
        return layout
        
if __name__ == "__main__":
    levels = []  # store levels of microphone
    get_level_thread = Thread(target = get_microphone_level)
    get_level_thread.daemon = True
    get_level_thread.start()
    VentilatorApp().run()