from format_time import format_laptime
from format_time import format_time_delta
import fastf1
import fastf1.plotting
import seaborn as sns
import matplotlib as mlt
from matplotlib import pyplot as plt
from fastf1.core import Laps
from fastf1.core import Lap
import pandas as pd
from timple.timedelta import strftimedelta
from matplotlib.lines import Line2D
import numpy as np
from matplotlib.collections import LineCollection
import matplotlib.colors as mcolors

title_font_b = {'family':'serif','color':'black','size':17}
title_font_w = {'family':'serif','color':'white','size':17}
mlt.rcParams['figure.facecolor'] = 'black'


def load_race_event (searched_event, race, quali):
    
    winner = race.drivers[:1]
    pole = quali.drivers[:1]
    
    fastest_lap = format_laptime(race.laps.pick_fastest()["LapTime"])
    pole_lap = format_laptime(quali.laps.pick_drivers(pole).pick_fastest()["LapTime"])
    fastest_laps_delta = format_laptime(race.laps.pick_fastest()["LapTime"] - quali.laps.pick_drivers(pole).pick_fastest()["LapTime"])
    
    print()
    print(searched_event["OfficialEventName"])
    template = "Round {0}, {1}\n{2}\nWinner: {3} Car {4}, {5}\n\nFastest racing lap: {6} ({7})\nPole lap: {8} ({9})\nFastest Lap Delta: {10}"
    print(template.format(searched_event["RoundNumber"], searched_event["Location"], searched_event["Session5Date"],
                            race.results["BroadcastName"].iloc[0], winner[0], race.results["TeamName"].iloc[0], 
            fastest_lap, race.get_driver(race.laps.pick_fastest()["DriverNumber"])["LastName"], pole_lap, 
            race.get_driver(pole[0])["LastName"], fastest_laps_delta))

    
def is_wet(race, driver):
    tyre_series = race.laps.pick_driver(driver)["Compound"]
    for tyre in tyre_series:
        if tyre == "Wet" or tyre == "Intermediate":
            return True
    return False

def plot_driver_race_laptime (race, driver):
    wet = False

    fastf1.plotting.setup_mpl(misc_mpl_mods=False)
    wet = is_wet(race, driver)
    
    if not wet:
        laps = race.laps.pick_driver(driver).pick_quicklaps(1.08).reset_index()
    else:
        laps = race.laps.pick_driver(driver).pick_quicklaps(1.40).reset_index()
    fig, ax = plt.subplots(figsize=(8, 8))

    sns.scatterplot(data=laps,
                x="LapNumber",
                y="LapTime",
                ax=ax,
                hue="Compound",
                palette=fastf1.plotting.COMPOUND_COLORS,
                s=80,
                linewidth=0,
                legend='auto')
    ax.set_xlabel("Lap Number")
    ax.set_ylabel("Lap Time")

    # The y-axis increases from bottom to top by default
    # Since we are plotting time, it makes sense to invert the axis
    ax.invert_yaxis()
    sub_title = race.get_driver(driver)["LastName"] + " laptimes, " + race.event["OfficialEventName"]
    plt.suptitle(sub_title)

    # Turn on major grid lines
    plt.grid(color='w', which='major', axis='both')
    sns.despine(left=True, bottom=True)

    plt.tight_layout()
    plt.show()
    
    
def plot_laptimes_comparison (race, driver1, driver2):
    driver_1_name = race.get_driver(driver1)["LastName"]
    driver_2_name = race.get_driver(driver2)["LastName"]
    driver_1_colour = fastf1.plotting.driver_color(driver_1_name)
    driver_2_colour = fastf1.plotting.driver_color(driver_2_name)
    
    wet = False
    wet = is_wet(race, driver1)
    fastf1.plotting.setup_mpl(misc_mpl_mods=False)
    
    if not wet:
        laps1 = race.laps.pick_driver(driver1).pick_quicklaps(1.08).reset_index()
        laps2 = race.laps.pick_driver(driver2).pick_quicklaps(1.08).reset_index()
    else:
        laps1 = race.laps.pick_driver(driver1).pick_quicklaps(1.40).reset_index()
        laps2 = race.laps.pick_driver(driver2).pick_quicklaps(1.40).reset_index()

    lap_list1 = list()
    lap_list2 = list()
    
    for lap in laps1.iterlaps():
        lap_list1.append(lap[1])
    for lap in laps2.iterlaps():
        lap_list2.append(lap[1])
    
    lap_1_df = Laps(lap_list1)
    lap_2_df = Laps(lap_list2)
    
    fig, ax = plt.subplots(figsize=(8, 8))
   
    plt.title(f"{race.event.year} {race.event['EventName']} Lap Time Comparison\n"
             f"{driver_1_name} vs {driver_2_name}", fontdict=title_font_w)
    sns.scatterplot(data=lap_1_df,
                x="LapNumber",
                y="LapTime",
                ax=ax,
                linewidth=0,
                s=80,
                legend='auto',
                color=driver_1_colour,
                label= driver_1_name)
    sns.scatterplot(data=lap_2_df,
                x="LapNumber",
                y="LapTime",
                ax=ax,
                linewidth=0,
                s=80,
                legend='auto',
                color=driver_2_colour,
                label= driver_2_name)

    ax.invert_yaxis()
 
    plt.grid(color='w', which='major', axis='both')
    sns.despine(left=True, bottom=True)

    plt.tight_layout()
    
    plt.show()
    
def plot_q3_flying_laps(quali):
    fastf1.plotting.setup_mpl(mpl_timedelta_support=True, color_scheme=None, misc_mpl_mods=False)
    
    q1, q2, q3 = quali.laps.split_qualifying_sessions()
    pole = quali.laps.pick_fastest()["LapTime"]
    top_drivers = quali.drivers[:6] #change back to 8
    
    hot_lap_list = list()
    for driver in top_drivers:
        hot_laps = q3.pick_driver(driver).pick_quicklaps()
        index = 1
        
        for lap in hot_laps.iterlaps():
            lap[1]['Flying_Index'] = lap[1]['Driver'] + " Lap " + str(index)
            lap[1]["LapTimeDelta"] = format_time_delta(lap[1]["LapTime"] - pole)
            index+=1
            hot_lap_list.append(lap[1])
            
    sorted_hot_laps = Laps(hot_lap_list).sort_values(by='LapTime').reset_index(drop=True)
    pole_lap = sorted_hot_laps.pick_fastest()
    #sorted_hot_laps['LapTimeDelta'] =  sorted_hot_laps['LapTime'] - pole_lap['LapTime']
    team_colors = list()

    for index, lap in sorted_hot_laps.iterlaps():
        color = fastf1.plotting.team_color(lap['Team'])
        team_colors.append(color)
    
    fig, ax = plt.subplots()
    horizontal_bars = ax.barh(sorted_hot_laps.index, sorted_hot_laps['LapTimeDelta'],
    color=team_colors, edgecolor='grey')
    ax.set_yticks(sorted_hot_laps.index)
    ax.set_yticklabels(sorted_hot_laps['Flying_Index'])

    # show fastest at the top
    ax.invert_yaxis()

    # draw vertical lines behind the bars
    ax.set_axisbelow(True)
    ax.xaxis.grid(True, which='major', linestyle='--', color='black', zorder=-1000)
    
    pole_time = strftimedelta(pole_lap['LapTime'], '%m:%s.%ms')

    plt.title(f"{quali.event['EventName']} {quali.event.year} Qualifying\n"
             f"Pole Lap Time: {pole_time} ({pole_lap['Driver']})", fontdict=title_font_b)
    
    plt.xlabel("Time Delta (Seconds)")
    plt.ylabel("Flying Laps")
    
    for i, value in enumerate(sorted_hot_laps['LapTimeDelta']):
        if i == 0:
            plt.text(value, i, " " + str(pole_time), ha='left', va='center')
            continue
        plt.text(value, i, " +" + str(value), ha='left', va='center')

    plt.show()

def plot_telemetry_data(session, driver1, driver2, command):
    
    driver_1_name = session.get_driver(driver1)["LastName"]
    driver_2_name = session.get_driver(driver2)["LastName"]
    
    driver_1_colour = fastf1.plotting.driver_color(driver_1_name)
    driver_2_colour = fastf1.plotting.driver_color(driver_2_name)
    
    driver_1_laps = session.laps.pick_driver(driver1).pick_fastest()
    driver_2_laps = session.laps.pick_driver(driver2).pick_fastest() 
    
    driver_1_tele = driver_1_laps.get_car_data().add_distance()
    driver_2_tele = driver_2_laps.get_car_data().add_distance()
    
    if command == 4:
        fig, ax = plt.subplots(nrows=3, sharex=True)

        for axis in ax:
            axis.set_facecolor('k')
                # Set the tick colors to white
            axis.tick_params(axis='x', colors='white')
            axis.tick_params(axis='y', colors='white')

            # Set the axis lines color to white
            axis.spines['left'].set_color('white')
            axis.spines['bottom'].set_color('white')

        legend_handles = [Line2D([0], [0], color=driver_1_colour, label=driver_1_name + " " + str(format_laptime(driver_1_laps["LapTime"]))),
                        Line2D([0], [0], color=driver_2_colour, label=driver_2_name + " " + str(format_laptime(driver_2_laps["LapTime"])))]
        ax[2].legend(handles=legend_handles)


        ax[0].plot(driver_1_tele['Distance'], driver_1_tele['Speed'], color = driver_1_colour, label = driver_1_name)
        ax[0].plot(driver_2_tele['Distance'], driver_2_tele['Speed'], color = driver_2_colour, label = driver_2_name)

        ax[0].set_ylabel('Speed in km/h', color = "white")
        ax[0].set_title(f"{session.event.year} {session.event['EventName']} Q3 Fast Lap Comparison\n"
                    f"{driver_1_name} vs {driver_2_name}", fontdict=title_font_w)

        ax[1].plot(driver_1_tele['Distance'], driver_1_tele['Throttle'], color = driver_1_colour)
        ax[1].plot(driver_2_tele['Distance'], driver_2_tele['Throttle'], color = driver_2_colour)

        ax[1].set_ylabel('Throttle Pressure %', color = "white")

        ax[2].plot(driver_1_tele['Distance'], driver_1_tele['RPM'], color = driver_1_colour)
        ax[2].plot(driver_2_tele['Distance'], driver_2_tele['RPM'], color = driver_2_colour)

        ax[2].set_ylabel('RPM', color = "white")
        ax[2].set_xlabel('Distance in m', color = "white")

        plt.show()
        
    if command == 5:
        cmap_binary = mcolors.ListedColormap([driver_1_colour, driver_2_colour])
         
        track_coord_x = driver_1_laps.telemetry['X']
        track_coord_y = driver_1_laps.telemetry['Y']
        track_speed_1 = driver_1_laps.telemetry['Speed']
        track_speed_2 = driver_2_laps.telemetry['Speed']
        
        max_length = max(len(track_speed_1), len(track_speed_2))
        
        #make sure arrays are of the same size
        if len(track_speed_1) == max_length:
            track_speed_2 =  track_speed_2._append(pd.Series([0] * (max_length - len(track_speed_2)))).reset_index(drop=True)
        
        else:
            track_speed_1 =  track_speed_1._append(pd.Series([0] * (max_length - len(track_speed_1))))
            
        track_speed_1 = track_speed_1.reset_index(drop=True)
        track_speed_2 = track_speed_2.reset_index(drop=True)
       
        points = np.array([track_coord_x, track_coord_y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        
        # Determine which driver is faster at each point
        faster_array = track_speed_1 > track_speed_2
        
        driver_1_fast_count = 0
        driver_2_fast_count = 0

        for data in faster_array:
            if data == True:
                driver_1_fast_count+=1
            else:
                driver_2_fast_count+=1
        
        driver_1_fast_percentage = (float(driver_1_fast_count) / (driver_1_fast_count + driver_2_fast_count)) * 100
        driver_2_fast_percentage = 100 - driver_1_fast_percentage
        
        # Create an array to hold the color values
        color_combined = np.where(faster_array, 0, 1)

        # Create the boundaries for color mapping
        boundaries = [-0.5, 0.5, 1.5]

        # Create BoundaryNorm for discrete color mapping
        norm = mcolors.BoundaryNorm(boundaries, cmap_binary.N)
        
        fig, ax = plt.subplots(sharex=True, sharey=True, figsize=(12, 6.75))
        # Adjust margins and turn of axis
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.12)
        ax.axis('off')
        
        ax.plot(track_coord_x, track_coord_y, color='white', linestyle='-', linewidth=8, zorder=0)
        
        
        color_combined = np.where(faster_array, 0, 1)
        
        lc = LineCollection(segments, cmap=cmap_binary, norm=norm, linestyle='-', linewidth=5)

        lc.set_array(color_combined)
        
        line = ax.add_collection(lc)
        
        ax.set_title(f"{session.event.year} {session.event['EventName']} Qualifying Track Dominance\n"
                    f"{driver_1_name} vs {driver_2_name}", fontdict=title_font_w)

        driver_1_label = driver_1_name + " " + str(format_laptime(driver_1_laps["LapTime"])) + " - Fastest in " \
        + str("{:.1f}".format(driver_1_fast_percentage)) + "% of Lap"
        driver_2_label = driver_2_name + " " + str(format_laptime(driver_2_laps["LapTime"])) + " - Fastest in " \
        + str("{:.1f}".format(driver_2_fast_percentage)) + "% of Lap"

        
        legend_handles = [Line2D([0], [0], color=driver_1_colour, label=driver_1_label),
                        Line2D([0], [0], color=driver_2_colour, label=driver_2_label)]
        ax.legend(handles=legend_handles)
        
        plt.show()
       
        
    
def plotting_menu(index, race, quali):
    if index == 1:
        driver = input("Enter driver number: ")
        plot_driver_race_laptime(race, driver)
        
    if index == 2:
        driver1 = input("Enter driver 1 number: ")
        driver2 = input("Enter driver 2 number: ")
        plot_laptimes_comparison(race, driver1, driver2)
        
    if index == 3:
        plot_q3_flying_laps(quali)
        
    if index == 4 or index == 5:
        driver1 = input("Enter driver 1 number: ")
        driver2 = input("Enter driver 2 number: ")
        plot_telemetry_data(quali, driver1, driver2, index)
    
        
        
    