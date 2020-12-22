from time import sleep
from nixie_driver import NixieDriver

class Counter:
    def __init__(self, nixie_driver, tube_no, start_val = 0 ):
        self.tube_no = tube_no
        self.count = start_val
        self.nixie_driver = nixie_driver

    def set_count( self, count):
        self.count = count - 1
        if self.count < 0:
            self.count = 9
        self.nixie_driver.nixie_display( self.tube_no, int(self.count))

    def reset( self ):
        self.count = 0 ;
        self.nixie_driver.nixie_display( self.tube_no, count )

    def blank( self ):
        self.nixie_driver.nixie_display( self.tube_no, -1 )

    def inc( self ):
        self.count = self.count + 1
        if( self.count > 9 ):
            self.count = 0 
        self.nixie_driver.nixie_display( self.tube_no, self.count)

    def dec( self ):
        self.count = self.count - 1
        if( self.count < 0):
            self.count = 9
        self.nixie_driver.nixie_display( self.tube_no, self.count )

    def get_count( self):
        return self.count

    def count_up( self, n_reps, delay=0):
        for i in range( n_reps ):
            self.inc()
            sleep( delay )

    def count_down( self, n_reps, delay=0):
        for i in range( n_reps ):
            self.dec()
            sleep( delay )

    # self is ms digit, other is ls digit
    def count_down_two_digit( self, other_counter, start_val, stop_val, delay=0):
        if start_val >= 0 and start_val <= 99:
            digit1 = int(start_val / 10 )
            digit2 = int(start_val % 10)
            #print( str( digit1 ) + "," + str(digit2))
            self.set_count( digit1 )
            other_counter.set_count( digit2 )
            sleep(delay)
            for i in range(start_val - stop_val):
                prev = other_counter.get_count( )
                other_counter.dec( )
                if prev == 9:
                    self.dec( )
                sleep( delay )

    def blink( self, n_reps, delay=0):
        current_count = self.get_count() + 1
        for i in range( n_reps ):
            self.blank()
            sleep( delay )
            self.set_count( current_count )
            sleep( delay )
    
    def blink_alternate( self, other_counter, n_reps, delay=0):
        for i in range( n_reps ):
            self.blink( 1, delay )
            other_counter.blink( 1, delay )

    def blink_two_digits( self, other_counter, n_reps, delay=0):
        my_count = self.get_count( ) + 1
        other_count = other_counter.get_count() + 1
        for i in range( n_reps ):
            sleep ( delay )
            self.blank( )
            other_counter.blank( )
            sleep( delay )
            self.set_count( my_count )
            other_counter.set_count( other_count )
            