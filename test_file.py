import fastf1
import fastf1.plotting
from matplotlib import pyplot as plt


session = fastf1.get_session(2023, "Bahrain", 'FP2')
session.load()


laps = session.laps
print((laps.pick_driver("1").pick_tyre("SOFT")))
print(laps.pick_driver("16").pick_tyre("SOFT"))
print(laps.pick_driver("44").pick_tyre("SOFT"))