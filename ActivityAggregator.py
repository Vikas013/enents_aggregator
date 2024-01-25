import json
import argparse
from datetime import datetime, timedelta
import os

class ActivityAggregator:
    def __init__(self):
        self.summary_data = {}
        self.timestamp_file = 'last_processed_timestamp.txt'
        self.last_processed_timestamp = self.load_last_processed_timestamp()

    def load_last_processed_timestamp(self):
        if os.path.exists(self.timestamp_file):
            with open(self.timestamp_file, 'r') as f:
                return int(f.read().strip())
        return None

    def save_last_processed_timestamp(self, timestamp):
        with open(self.timestamp_file, 'w') as f:
            f.write(str(timestamp))

    def process_events(self, events):
        for event in events:
            timestamp = event['timestamp']

            # Skip events that were processed in the previous run
            if self.last_processed_timestamp is not None and timestamp <= self.last_processed_timestamp:
                continue

            user_id = event['userId']
            event_date = datetime.utcfromtimestamp(timestamp).date()

            if event_date not in self.summary_data:
                self.summary_data[event_date] = {}

            if user_id not in self.summary_data[event_date]:
                self.summary_data[event_date][user_id] = {'post': 0, 'likeReceived': 0, 'comment': 0}

            event_type = event['eventType']

            # Handle unknown event types gracefully
            if event_type not in self.summary_data[event_date][user_id]:
                print(f"Warning: Unknown event type '{event_type}' for user {user_id} on {event_date}")
                continue  # Skip this event and move to the next one

            self.summary_data[event_date][user_id][event_type] += 1

            # Update the last processed timestamp
            self.last_processed_timestamp = timestamp

    def save_summary_reports(self, output_file):
        output_list = []

        for date, users in self.summary_data.items():
            for user_id, activities in users.items():
                output_dict = {
                    'userId': user_id,
                    'date': date.strftime('%Y-%m-%d'),
                    **activities
                }
                output_list.append(output_dict)

        with open(output_file, 'w') as f:
            json.dump(output_list, f, indent=2)

        # Save the latest timestamp to the timestamp file
        if self.last_processed_timestamp is not None:
            self.save_last_processed_timestamp(self.last_processed_timestamp)

    def load_summary_reports(self, input_file):
        if os.path.exists(input_file):
            with open(input_file, 'r') as f:
                summary_reports = json.load(f)
                for report in summary_reports:
                    user_id = report['userId']
                    event_date = datetime.strptime(report['date'], '%Y-%m-%d').date()
                    self.summary_data.setdefault(event_date, {}).setdefault(user_id, report)

def main():
    parser = argparse.ArgumentParser(description='Aggregate user activity events and generate daily summary reports.')
    parser.add_argument('-i', '--input', required=True, help='Input JSON file path')
    parser.add_argument('-o', '--output', required=True, help='Output JSON file path')
    parser.add_argument('--update', action='store_true', help='Update existing summary reports with new events')
    args = parser.parse_args()

    aggregator = ActivityAggregator()

    # Load existing summary reports if the --update flag is provided
    if args.update:
        aggregator.load_summary_reports(args.output)

    with open(args.input, 'r') as f:
        events = json.load(f)

    aggregator.process_events(events)
    aggregator.save_summary_reports(args.output)

if __name__ == '__main__':
    main()
