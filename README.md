User Activity Aggregator

This Python script aggregates user activity events, generates daily summary reports, and supports real-time updates.

Usage:

1. Ensure you have Python installed on your system.

2. Clone the repository or download the script.

    ```bash
    git clone https://github.com/vikas013/events_aggregator.git
    cd events_aggregator
    ```

3. Make the script executable.

    ```bash
    chmod +x aggregate_events.sh
    ```

4. Run the script with input and output file paths.

    ```bash
    ./aggregate_events.sh -i input.json -o output.json
    ```

    - `-i` or `--input`: Specify the input JSON file path containing user activity events.
    - `-o` or `--output`: Specify the output JSON file path for storing the daily summary reports.

5. To update existing summary reports with new events, use the `--update` flag.

    ```bash
    ./aggregate_events.sh -i input.json -o output.json --update
    ```

    This will process only the events added after the last run without the `--update` flag.

Example:

```bash
./aggregate_events.sh -i input.json -o output.json
