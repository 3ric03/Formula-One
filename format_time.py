from datetime import datetime

def format_laptime(laptime):
    minutes = laptime.components.minutes
    seconds = laptime.components.seconds
    milliseconds = laptime.components.milliseconds

    return f"{minutes}:{seconds:02d}.{milliseconds:03d}"