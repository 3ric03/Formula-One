import fastf1 
from fastf1 import plotting
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
from matplotlib import cm
from format_time import seconds_to_time_delta
from tyre_data_parser import race_tyre_types
import numpy as np

title_font_b = {'family':'serif','color':'black','size':17}
title_font_w = {'family':'serif','color':'white','size':17}
axis_font_w = {'family':'serif','color':'white','size':13}

# Make plot a bit bigger
plt.rcParams['figure.figsize'] = [10, 10]
    
def practise_pace_plotter(fp1, fp2, drivers: list[int]): #need to loop through drivers and check changes tyres they ran long runs in 
    pass

def race_pace_plotter(race, drivers: list[int]): #use guide, do not consider tyre compounds when displaying 
    
    driver_colours = []
    driver_names = []
    for driver in drivers:
        driver_names.append(race.get_driver(str(driver))["LastName"])
        driver_colours.append(fastf1.plotting.driver_color(race.get_driver(str(driver))["LastName"]))
    compounds = race_tyre_types(race, drivers)
    
    for i, name in enumerate(driver_names):
        name += '\n'
        for j in range (len(compounds[i])):
            if j == 0:
                name += compounds[i][j][0]
            else:
                name += '-' + compounds[i][j][0]
        driver_names[i] = name
        
    laps = race.laps.pick_drivers(drivers)
    # Convert laptimes to seconds
    
    laps['LapTimeSeconds'] = laps['LapTime'].dt.total_seconds()

    # To get accurate laps only, we exclude in- and outlaps
    laps = laps.loc[(laps['PitOutTime'].isnull() & laps['PitInTime'].isnull())]
    
    # using the Inter-Quartile Range (IQR) proximity rule
    percentile_75, percentile_25 = laps['LapTimeSeconds'].quantile(0.75), laps['LapTimeSeconds'].quantile(0.25)
    IRQ_median = percentile_75 - percentile_25
    
    max_lap_time = percentile_75 + (1.5 * IRQ_median)
    min_lap_time = percentile_25 - (1.5 * IRQ_median)
    
    laps.loc[laps['LapTimeSeconds'] < min_lap_time, 'LapTimeSeconds'] = np.nan
    laps.loc[laps['LapTimeSeconds'] > max_lap_time, 'LapTimeSeconds'] = np.nan
    
    # Make plot a bit bigger
    plt.rcParams['figure.figsize'] = [10, 10]
    fig, ax = plt.subplots()
    
    ax.set_facecolor('k') # Set the tick colors to white
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    # Set the axis lines color to white
    ax.spines['left'].set_color('white')
    ax.spines['bottom'].set_color('white')
    
    laptimes = [laps.pick_driver(driver)['LapTimeSeconds'].dropna() for driver in drivers] 
    
    box_plot = ax.boxplot(laptimes, patch_artist = True, widths=0.25)
    ax.set_xticklabels(driver_names, fontdict=axis_font_w)
    ax.set_title('Average racepace comparison')
    ax.set_ylabel('Lap Time (s)', color = "white")
    

    for i, box in enumerate(box_plot['boxes']):
        # Set the outline color to white
        box.set(color='white', linewidth=1.5)
        # Set the fill color of the boxes
        box.set_facecolor(driver_colours[i])
    
    for element in ['whiskers', 'caps', 'medians']:
        for line in box_plot[element]:
            line.set(color='white')
    
    for flier in box_plot['fliers']:
        flier.set(marker='o', color = 'white', alpha = 1)
        
    medians = [np.median(laptimes[i]) for i in range(len(laptimes))]
    
    for i, median in enumerate(medians):
        median_formatted = seconds_to_time_delta(median)
        ax.text(i + 1, median, str(median_formatted), color='white', ha='center', va='bottom')
        
    ax.set_title(f"{race.event.year} {race.event['EventName']} Race Pace Comparison" ,fontdict=title_font_w)
    
    plt.show()

def tyre_deg_plotter(): 
    pass

def input_drivers() -> list[int]:
    drivers = []
    default_drivers = [16, 1, 44, 14]
    user_input = input("Enter up to 4 driver numbers, seperated by space. Blank enter for default drivers: ")
    if not len(user_input):
        return default_drivers
    drivers = user_input.split(' ')
    #drivers = [int(driver) for driver in drivers]
    return drivers
        
def analysis_menu (index, event,  race):
    if index == 1:
        fp1 = event.get_practise(1)
        fp2 = event.get_practise(2)
        drivers = input_drivers()
        race_pace_plotter(fp1, fp2, drivers)
        
    if index == 2:
       drivers = input_drivers()
       race_pace_plotter(race, drivers)
        
    if index == 3:
        pass