# -*- coding: utf-8 -*-

import time
from datetime import datetime
from math import sin
from threading import Thread

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.core.window import Window
from kivy.config import Config
from kivy_garden.graph import Graph, LinePlot
from kivy.clock import Clock
from kivy.core.audio import SoundLoader

import board
import busio
import pigpio
import RPi.GPIO as GPIO
import adafruit_bmp280
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import Adafruit_DHT


def data_collection():
    global pressure
    global flow
    global volume
    global acc
    i2c = busio.I2C(board.SCL, board.SDA)
    bmp = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, 0x76)
    ads = ADS.ADS1015(i2c)
    chan = AnalogIn(ads, ADS.P0)
    acc = 0
    while True:
        if len(pressure) >= 100:
            pressure = []
            flow = []
            volume = []
            acc = 0
        pressure.append(bmp.pressure)
        f = chan.voltage/0.297-0.45
        flow.append(f)
        acc += f
        volume.append(acc)
    
    
class Home(BoxLayout):
    pressure = ObjectProperty(None)
    flow = ObjectProperty(None)
    volumn = ObjectProperty(None)
    ie = StringProperty('1:4')
    resp = NumericProperty(10)
    temperature = NumericProperty(None)
    humidity = NumericProperty(None)
    
    def __init__(self):
        super(Home, self).__init__()
        self.pressure_plot = LinePlot(line_width=2, color=[1, 1, 0.3, 1])
        self.flow_plot = LinePlot(line_width=2, color=[1, 1, 0.3, 1])
        self.volumn_plot = LinePlot(line_width=2, color=[1, 1, 0.3, 1])
        self.init_resp()
        self.ie_list = ['2:1', '1:1', '1:2', '1:3', '1:4']
        self.ie_index = 0
    
    def update_graph(self):
        self.pressure.add_plot(self.pressure_plot)
        self.flow.add_plot(self.flow_plot)
        self.volumn.add_plot(self.volumn_plot)
        Clock.schedule_interval(self.get_value, 0.001)
    
    def get_value(self, dt):
        self.pressure_plot.points = [(i, j/5) for i, j in enumerate(pressure)]
        self.flow_plot.points = [(i, j/5) for i, j in enumerate(flow)]
        self.volumn_plot.points = [(i, j/5) for i, j in enumerate(flow)]
    
    def dht11_old(self):
        dht = Adafruit_DHT.DHT11
        gpio_pin = 17
        while True:
            humid, temp_c = Adafruit_DHT.read_retry(dht, gpio_pin)
            if temp_c is not None and humid is not None:
                self.temperature = int(temp_c * (9 / 5) + 32)
                self.humidity = int(humid)
            time.sleep(30)

    def update_temp_humid(self):
        temp_humid_thread = Thread(target = self.dht11_old)
        temp_humid_thread.daemon = True
        temp_humid_thread.start()
    
    def plus_one(self):
        if self.resp < 30:
            self.resp += 1
        
    def minus_one(self):
        if self.resp > 10:
            self.resp -= 1
    
    def left_one(self):
        if self.ie_index > 0:
            self.ie_index -= 1
            self.ie = self.ie_list[self.ie_index]
    
    def right_one(self):
        if self.ie_index < (len(self.ie_list) - 1):
            self.ie_index += 1
            self.ie = self.ie_list[self.ie_index]
        
    def init_resp(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(27, GPIO.OUT)
        self.ESC = 4  #Connect the ESC in this GPIO pin
        self.pi = pigpio.pi()
        self.pi.set_servo_pulsewidth(self.ESC, 0)
        time.sleep(1)
        resp_thread = Thread(target = self.resp_control)
        resp_thread.daemon = True
        resp_thread.start()
        
    def resp_control(self):
        speed = 1200
        while True:
            self.i = int(self.ie[0])
            self.e = int(self.ie[2])
            # Inspiratory
            self.pi.set_servo_pulsewidth(self.ESC, speed)
            GPIO.output(27, False)
            time.sleep(60/self.resp*self.i/(self.i+self.e))
            # Expiratory
            self.pi.set_servo_pulsewidth(self.ESC, 0)
            GPIO.output(27, True)
            time.sleep(60/self.resp*self.e/(self.i+self.e))


class Records(GridLayout):
    pass


class Alarms(GridLayout):
    pass


class Header(BoxLayout):
    now = StringProperty('')
    def __init__(self):
        super(Header, self).__init__()
        self.update_time()
        
    def update_time(self):
        self.now = datetime.now().strftime("%I:%M %p\n%m/%d/%Y")
        Clock.schedule_interval(self.get_time, 1)
    
    def get_time(self, dt):
        self.now = datetime.now().strftime("%I:%M %p\n%m/%d/%Y")

class MainMenu(BoxLayout):
    pass

class VentilatorApp(App):
    def build(self):
        Window.fullscreen = True
        Window.size = (1024, 600)
        self.audio = SoundLoader.load('beep-21.wav')
        self.manager = ScreenManager(transition=FadeTransition(duration=0.15))
        # Initialize Home object
        home = Home()
        home.update_graph()
        home.update_temp_humid()
        # Add Home object to screen
        home_screen = Screen(name="home")
        home_screen.add_widget(home)
        self.manager.add_widget(home_screen)
        # Create Records object and add it to screen
        records = Records()
        records_screen = Screen(name="records")
        records_screen.add_widget(records)
        self.manager.add_widget(records_screen)
        # Create Alarms object and add it to screen
        alarms = Alarms()
        alarms_screen = Screen(name="alarms")
        alarms_screen.add_widget(alarms)
        self.manager.add_widget(alarms_screen)
        
        layout = GridLayout(cols=1)
        header = Header()
        layout.add_widget(header)
        layout.add_widget(self.manager)
        layout.add_widget(MainMenu())
        return layout
    
    def beep(self):
        if self.audio:
            self.audio.play()
        
if __name__ == "__main__":
    pressure = []
    flow = []
    volume = []
    data_thread = Thread(target = data_collection)
    data_thread.daemon = True
    data_thread.start()
    VentilatorApp().run()