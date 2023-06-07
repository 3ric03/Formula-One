"""Qualifying results overview
==============================

Plot the qualifying result with visualization the fastest times.
"""


import matplotlib.pyplot as plt
import pandas as pd
from timple.timedelta import strftimedelta

import fastf1
import fastf1.plotting
from fastf1.core import Laps


# we only want support for timedelta plotting in this example
fastf1.plotting.setup_mpl(mpl_timedelta_support=True, color_scheme=None, misc_mpl_mods=False)

session = fastf1.get_session(2021, 'Spanish Grand Prix', 'Q')
session.load()


##############################################################################
# First, we need to get an array of all drivers.

drivers = pd.unique(session.laps['Driver'])
print(drivers)


##############################################################################
# After that we'll get each drivers fastest lap, create a new laps object
# from these laps, sort them by lap time and have pandas reindex them to
# number them nicely by starting position.

list_fastest_laps = list()
for drv in drivers:
    drvs_fastest_lap = session.laps.pick_driver(drv).pick_fastest()
    list_fastest_laps.append(drvs_fastest_lap)
    
print(list_fastest_laps[0]["LapTime"])
fastest_laps = Laps(list_fastest_laps).sort_values(by='LapTime').reset_index(drop=True)
