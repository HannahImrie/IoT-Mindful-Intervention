import os
import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D22)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0
chan0 = AnalogIn(mcp, MCP.P0)
chan1 = AnalogIn(mcp, MCP.P1)
chan2 = AnalogIn(mcp, MCP.P2)
chan3 = AnalogIn(mcp, MCP.P3)
chan4 = AnalogIn(mcp, MCP.P4)


while True:
    start = time.time()
    fR = chan0.value
    bR = chan1.value
    b = chan2.value
    bL = chan3.value
    fL = chan4.value

    print(
        f'Front Right: {fR}, Back Right: {bR}, Back: {b}, Back Left: {bL}, Front Left: {fL}')
    end = time.time()
    timer = end-start
    #print(f'This operation takes {timer} seconds.')
    time.sleep(1-timer)
