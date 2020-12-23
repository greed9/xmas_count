from machine import Pin, I2C, RTC
import time
import boot
import config
import ssd1306
import ntptime
import utime
from nixie_driver import NixieDriver
from counter import Counter
import neopixel

def i2c_scan( i2c ):
    print('Scan i2c bus...') 
    devices = i2c.scan()

    if len(devices) == 0:
        print("No i2c device !")
    else:
        print('i2c devices found:',len(devices))

    for device in devices:  
        print("Decimal address: ",device," | Hexa address: ",hex(device))

def days_til_date ( oled, target_year, target_mon, target_day ):
    #rtc = RTC()
    utc_time = utime.time ( )
    utc_time = utc_time - ( 5 * 60 * 60 )
    (year, mon, day, hour, minute, sec, dayno, a) = utime.localtime(utc_time) 
    dtString = str(year) + ' ' + str(mon) + ' ' + str( day ) + ' ' + str( hour) + ' ' + str(minute) 
    oled.text( '                    ', 0, 0)
    oled.text( dtString, 0, 0)
    print( dtString )

    future_time = utime.mktime((target_year, target_mon, target_day, 0, 0, 0, 0, 0))
    today = utime.mktime((year, mon, day, hour, minute, sec, dayno, a))
    return int( ( future_time - today ) / ( 24 * 60 * 60 ) )

def set_date_from_ntp( oled ):
    retval = 0 
    try:
        rtc = RTC()
        ntptime.settime( )
        utc_time = utime.time ( )
        utc_time = utc_time - ( 5 * 60 * 60 )
        (year, mon, day, hour, minute, sec, dayno, a) = utime.localtime(utc_time) 
        dtString = str(year) + ' ' + str(mon) + ' ' + str( day ) + ' ' + str( hour) + ' ' + str(minute) 
        oled.text( dtString, 0, 0)
        print( str(year) + ' ' + str(mon) + ' ' + str( day ) + ' ' + str( hour) + ' ' + str(minute) )

        retval = 1
    except Exception as e:
        oled.text( "Can't get time", 0, 0)
        print( e )

    oled.show()
    return retval

def set_neopixel_colors( red, green, blue):
    neopixel_pin = Pin(14, Pin.OUT)
    np = neopixel.NeoPixel( neopixel_pin, 5 )
    for i in range(np.n):
        np[i] = ( red, green, blue)
    np.write( )

def countdown_display( counters, days ):
    counters[1].count_down_two_digit( counters[0], 99, days, 0.05)
    counters[1].blink_two_digits( counters[0], 5, 0.5 )
    time.sleep(10)
    counters[1].blank( )
    counters[0].blank( )

def calendar_display( counters ):
    utc_time = utime.time ( )
    utc_time = utc_time - ( 5 * 60 * 60 )
    (year, mon, day, hour, minute, sec, dayno, a) = utime.localtime(utc_time)
    print( str(mon) + "-" + str(day))

    counters[1].blank()
    counters[0].blank()
    counters[0].set_count( int( mon % 10 ))
    counters[1].set_count( int( mon / 10 ))
    time.sleep( 5 )
    counters[1].blank()
    counters[0].blank()
    counters[0].set_count( int( day % 10 ))
    counters[1].set_count( int( day / 10 ))
    time.sleep( 5 )
    counters[1].blank()
    counters[0].blank()

def main( ):
    # I got a lot of this stuff from: https://RandomNerdTutorials.com
    
    # ESP32 Pin assignment 
    i2c = I2C(-1, scl=Pin(22), sda=Pin(21))

    #i2c_scan(i2c)

    oled_width = 128
    oled_height = 64
    oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

    result = set_date_from_ntp ( oled )
    while result == 0:
        time.sleep(5)
        result = set_date_from_ntp

    # Light up the neopixels
    set_neopixel_colors( 0, 0, 64 )
   
    nixie_driver = NixieDriver( 25, 26, 27 )
    counters = [Counter( nixie_driver, 0), Counter( nixie_driver, 1)]

    counters[1].set_count( 0 )
    counters[0].set_count( 0 )
    time.sleep( 1 )
    even = True 

    while True:
        print( "Days til Xmas...")
        days = days_til_date( oled, 2020, 12, 25 )

        # Not sure why this is needed, but...
        days = days + 1
        if days == 1 or days == 0:
            # alternate red and green
            if even :
                set_neopixel_colors( 128, 0, 0 )
            else:
                set_neopixel_colors( 0, 128, 0 )
            if even == True:
                even = False
            else:
                even = True
            countdown_display( counters, days )
            time.sleep( 15 )
        elif days > 0 and days <= 99:
            countdown_display( counters, days )
            time.sleep( 15)
        else:
            set_neopixel_colors(0, 0, 64)
            calendar_display( counters )
            time.sleep( 15)

if __name__ == "__main__":
    main ( )
