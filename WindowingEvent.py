import apache_beam as beam
from apache_beam.transforms.window import FixedWindows
from datetime import datetime

def parse_time(time_str):
    # Convert string to datetime object
    dt = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
    
    # Return Unix timestamp
    return dt.timestamp()

with beam.Pipeline() as p:
    events = p | 'Create Events' >> beam.Create([
        ('event1', '2024-10-06 00:01:00'),
        ('event2', '2024-10-06 00:01:30'),
        ('event3', '2024-10-06 00:02:00'),
        ('event4', '2024-10-06 00:02:30')
    ])
    
    # Assign events to 1-minute fixed windows
    windowed_events = (events
                       | 'Assign Windows' >> beam.Map(lambda x: beam.window.TimestampedValue(x, parse_time(x[1])))
                       | 'Fixed Window' >> beam.WindowInto(FixedWindows(60)))

    # Count events in each window
    event_counts = (windowed_events
                    | 'Extract Event' >> beam.Map(lambda x: ('event', 1))
                    | 'Count Per Window' >> beam.CombinePerKey(sum))
    
    event_counts | 'Print Results' >> beam.Map(print)

#######   outputs   ###########
#('event', 2)
#('event', 2)
