import nixie_driver.py
import counter.py

nixie_driver = NixieDriver( 25, 26, 27 )
#nixie_driver.nixie_display( 0, 1 )
#nixie_driver.nixie_display( 1, 1 )
#nixie_driver.nixie_display( 0, 2 )
#nixie_driver.nixie_display( 1, 3 )
#nixie_driver.nixie_display( 0, -1)
#nixie_driver.nixie_display( 1, -1 )

# count nixies up and down
counters = [Counter( nixie_driver, 0), Counter( nixie_driver, 1)]
#counters[0].count_up( 100, 0.1)
#counters[0].blink( 5, 0.25)
#counters[0].blank()
#counters[1].count_down( 100, 0.1)
#counters[1].blink( 5, 0.25)
#counters[1].blank()