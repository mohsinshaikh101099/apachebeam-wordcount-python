import apache_beam as beam
from apache_beam.transforms.window import FixedWindows
from apache_beam.transforms.trigger import AfterWatermark, AfterProcessingTime, AccumulationMode
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
        ('late_event', '2024-10-06 00:01:15')
    ])

    # Assign timestamps and apply windowing
    windowed_events = (events
                       | 'Assign Timestamps' >> beam.Map(lambda x: beam.window.TimestampedValue(x, parse_time(x[1])))
                       
                       # Apply a Fixed Window of 1 minute with Triggers
                       | 'Apply Fixed Window' >> beam.WindowInto(
                            FixedWindows(60),
                            trigger=AfterWatermark(early=AfterProcessingTime(10)),  # Fire after watermark or 10s of processing time
                            accumulation_mode=AccumulationMode.DISCARDING  # Discard old data once results are emitted
                        ))

    # Count events in each window, including late data
    event_counts = (windowed_events
                    | 'Extract Event' >> beam.Map(lambda x: ('event', 1))
                    | 'Count Per Window' >> beam.CombinePerKey(sum))
    
    event_counts | 'Print Results' >> beam.Map(print)
