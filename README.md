# AIOps Service Monitoring Simulation

## Scenario

This project monitors a synthetic `payment-service`. The operational problem is detecting
slow payment requests, resource saturation, and service or database timeouts before they
become broader production incidents.

The assessment demonstrates a lightweight AIOps workflow:

```text
Operational data -> anomaly detection -> event -> producer -> topic -> consumer -> AIOps output
```

AIOps combines telemetry analysis and event processing so that an operational issue can be
identified and passed to a downstream component in a repeatable way.

## Repository Components

- `data/service_data.json`: synthetic timestamped payment-service metrics and log records.
- `src/anomaly_detector.py`: applies response-time, CPU, memory, and log-level thresholds.
- `src/event_producer.py`: publishes detected anomaly events.
- `src/event_topic.py`: in-memory topic that stores messages.
- `src/event_consumer.py`: receives messages from the topic.
- `src/aiops_pipeline.py`: loads data, detects anomalies, publishes events, and prints the
  final AIOps result.
- `tests/`: unit and end-to-end validation for calculations and the AIOps pipeline.

## Operational Data Analysis

Each record contains:

- Metrics: `response_time_ms`, `cpu_percent`, and `memory_percent`.
- Log information: `log_level` and `message`.
- Context: `timestamp` and `service`.

Timestamps use ISO-style date-time strings at one-minute intervals from 10:00 through 10:09
on 2026-09-20. The normal observations are the INFO records with response times from 120 to
150 ms, CPU from 42% to 50%, and memory from 51% to 57%.

The unusual observations are:

- 10:05: response time 610 ms and an ERROR stating `Payment service timeout`.
- 10:06: response time 640 ms, CPU 94%, memory 91%, and an ERROR stating
  `Database connection timeout`.

## Anomaly Detection Findings

The detector flags values above these thresholds:

- Response time: greater than 500 ms.
- CPU: greater than 80%.
- Memory: greater than 80%.
- Log level: `ERROR`.

Two anomalies are detected, at 10:05 and 10:06. The event contains the timestamp, service,
source record, and reasons such as `High response time`, `High CPU utilization`,
`High memory utilization`, and `Error log detected`. No expected anomaly was missed and no
normal record was incorrectly flagged in this dataset.

One limitation is that the detector uses fixed thresholds and does not learn the service's
normal baseline. A possible improvement would be adaptive thresholds or a time-series model
that accounts for seasonal behaviour and sustained trends.

## Event Flow and Corrections

For each detected anomaly, the producer publishes an event to the shared in-memory
`anomaly-events` topic. The consumer reads the same topic and returns the processed events as
the downstream AIOps output.

The investigation found and corrected these issues:

1. `ERROR` log records were not detected because the detector checked for `WARNING` instead.
2. The producer and consumer were connected to different topic instances, so consumers saw
	zero events.
3. The pipeline used imports that worked only when `src` was manually added to `PYTHONPATH`.
	Package-compatible imports now support both pytest and direct script execution.
4. The disabled Fibonacci test had an incorrect expected value (`89`); the implementation
	correctly returns `55` for index 10.

## Final Execution

Running `python3 src/aiops_pipeline.py` produces this result:

```text
Records processed: 10
Anomalies detected: 2
Events consumed: 2
```

The final output identifies the payment-service timeout at 10:05 and the database connection
timeout with resource saturation at 10:06.

## Reproduce the Demonstration

From the repository root:

```bash
python3 -m pip install -r requirements.txt
python3 -m pip install pytest coverage pytest-cov
python3 src/aiops_pipeline.py
python3 -m pytest --cov=src --cov-report=term-missing --verbose
coverage report --fail-under=90
```

The final validation passes with 16 tests and 100% total coverage.
# GitHub Challenge

<img src="https://octodex.github.com/images/Professortocat_v2.png" align="right" height="200px" />

Hey there!

Your challenge is ready.
Follow the instructions provided for this challenge and complete the required tasks in this repository.

Make sure your work is committed and pushed to your repository before submission.

Good luck!


---

&copy; 2025 GitHub &bull; [Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/code_of_conduct.md) &bull; [MIT License](https://gh.io/mit)

