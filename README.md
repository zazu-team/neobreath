# iAI Open Source Ventilator Sensor Inforamtion

## Sensor list

| Sensor Name | Sensor Model | Links | Pin Address |
| ----------- | ------------ | ----- | ----------- |
| Pressure sensor A | Adafruit MPRLS | [Adafruit](https://learn.adafruit.com/adafruit-mprls-ported-pressure-sensor-breakout/overview) | I2C 18 |
| Pressure sensor B | HiLetgo BMP280 | [Adafruit](https://learn.adafruit.com/adafruit-bmp280-barometric-pressure-plus-temperature-sensor-breakout/overview) | I2C 76 |
| Temperature and humidity sensor | HiLetgo DHT11(Digital) | [Adafruit](https://learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging/overview) | GPIO 17 |
| Differential pressure sensor| NXP MPX5010DP (+ADS1115 ADC) | [NXP](https://www.nxp.com/docs/en/data-sheet/MPX5010.pdf) | I2C 48|

## Rasberry pi GPIO resources

- [GPIO pins information](https://www.raspberrypi.org/documentation/usage/gpio/README.md)
- [Gpiozero](https://gpiozero.readthedocs.io/en/stable/)
- [RPi.GPIO](https://pypi.org/project/RPi.GPIO/)
- [CircuitPython on Raspberry Pi](https://learn.adafruit.com/circuitpython-on-raspberrypi-linux)

## Tutorials

- [DHT11 on Raspberry Pi Tutorial](https://www.circuitbasics.com/how-to-set-up-the-dht11-humidity-sensor-on-the-raspberry-pi/)
- [BMP280 on Raspberry Pi Tutorial](http://www.pibits.net/code/raspberry-pi-and-bmp280-sensor-example.php)
- [MPX5010DP on Raspberry Pi Tutorial](https://github.com/Pi4IoT/Node-RED/tree/master/waterLevel_moisture_Node-RED)

## Voltage to differential pressure

![mpx5010](mpx5010.PNG)

- Vs = 3.3Vdc
- ignore noise
- P = (Vout/Vs-0.04)/0.09 = Vout/0.297-0.45

## DC motor

![l293d](l293d.jpg)

Use motor driver L293D

IN1 to GPIO 23 (pin16)

IN2 to GPIO 24 (pin18)

EN1 to GPIO 25 (pin22)

Connect GND to GND

Connect OUT1 and OUT2 to the motor

Connect Vcc for the chip (no.16) to 5V in Rpi

Connect Vcc for the DC motor (no. 8) to a power supply between 4.5V and 36V.

## Resp rate control

The normal respiration rate for an adult at rest is 12 to 20 breaths per minute.

We set the range of the adjustable respiration rate as from 10 to 30 times per minute. It means each respiration takes 2 seconds to 6 seconds. We set the default resp rate as 20. We set the default I:E ratio as 2:1.

I:E ratio refers to the ratio of inspiratory time:expiratory time. In normal spontaneous breathing, the expiratory time is about twice as long as the inspiratory time. This gives an I:E ratio of 1:2.

The ratio is typically changed in asthmatics due to the prolonged time of expiration. They might have an I:E ratio of 1:3 or 1:4. Even longer expiratory times are required sometimes.

An inverse ratio refers to when the I:E ratio is 2:1 or higher and is typically used to ventilate non-compliant lungs. Pressure control modes of ventilation should be used when employing inverse ratios as the use of volume control modes might lead to breath stacking and an increase in airway pressure.