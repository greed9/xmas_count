from machine import Pin
from time import sleep

# Port of Marcin Saj's arduino code for the NixieTester V2 driver board
# https://nixietester.com/project/nixie-tube-driver-v2/

class NixieDriver:
    def __init__ (self, clk_pin_no, en_pin_no, din_pin_no):

        # This code is equivalent to setup ( ) in Marcin's Arduino sketch
        self.en_pin = Pin(en_pin_no, Pin.OUT)
        self.clk_pin = Pin(clk_pin_no, Pin.OUT)
        self.din_pin = Pin(din_pin_no, Pin.OUT)
        self.en_pin.value( 0 )
        self.din_pin.value( 0 )
        self.clk_pin.value( 0 )

        # remember the state of each digit
        self.selected_digit = [0, 0]
        self.cathodes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # This code models the NixieDisplay method in the Arduino sketch
    def nixie_display( self, tube_no, value ):

        # turn off previous digit for self tube
        offset = tube_no * 10
        self.cathodes[int(offset + self.selected_digit[tube_no])] = 0

        # turn on selected digit for self tube
        # -1 is special case of all digits off
        if value > -1:
            self.cathodes[int(offset + value)] = 1
            self.selected_digit[tube_no] = value

        # Hold enable low for entire transmission
        self.en_pin.value( 0 )

        # clear the shift registers
        self.clk_pin.value( 0 )
        self.din_pin.value( 0 )

        # Shift out the values - msb first
        for digit in reversed(self.cathodes):
            self.din_pin.value( digit )
            self.clk_pin.value( 1 )
            self.clk_pin.value( 0 )
            #print( str(digit) + ",", end="")

        #print( )

        # Finish transmission
        self.en_pin.value( 1 )
        self.clk_pin.value( 0 )

    def main ( ):
        pass

    if __name__ == "__main__":
        main( )
