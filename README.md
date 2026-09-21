# Payment-Service AIOps Assessment

This repository demonstrates a lightweight AIOps workflow for monitoring a synthetic
`payment-service`:

```text
Operational data -> anomaly detection -> event -> producer -> topic -> consumer -> AIOps output
```

The operational problem is identifying slow payment requests, resource saturation, and
service or database timeouts early enough for the operations team to respond. AIOps combines
telemetry analysis with event processing so detected issues can be passed through a repeatable
automated workflow.

## Repository Components

- `data/service_data.json`: timestamped synthetic metrics and log records.
- `src/anomaly_detector.py`: detects threshold breaches and `ERROR` log records.
- `src/event_producer.py`: publishes anomaly events.
- `src/event_topic.py`: stores events in an in-memory topic.
- `src/event_consumer.py`: receives events from the topic.
- `src/aiops_pipeline.py`: runs the complete workflow and prints the final output.
- `tests/`: calculation tests and AIOps pipeline validation.
- `.github/workflows/`: Python test and coverage workflows.

## Operational Data Analysis

Each JSON record contains:

- Metrics: `response_time_ms`, `cpu_percent`, and `memory_percent`.
- Log information: `log_level` and `message`.
- Context: `timestamp` and `service`.

The timestamps are ISO-style values at one-minute intervals from 10:00 through 10:09 on
2026-09-20. Normal observations are the `INFO` records with response times from 120 to 150 ms,
CPU from 42% to 50%, and memory from 51% to 57%.

The unusual observations are:

- `10:05`: response time 610 ms and `ERROR`: `Payment service timeout`.
- `10:06`: response time 640 ms, CPU 94%, memory 91%, and `ERROR`: `Database connection timeout`.

## Anomaly Detection Findings

The detector uses these thresholds:

- Response time greater than 500 ms: `High response time`.
- CPU greater than 80%: `High CPU utilization`.
- Memory greater than 80%: `High memory utilization`.
- Log level equal to `ERROR`: `Error log detected`.

Two anomalies were detected:

1. At 10:05, the payment request timed out and exceeded the response-time threshold.
2. At 10:06, the database connection timed out, response time was high, and CPU and memory
	exceeded their thresholds.

No expected anomaly was missed and no normal record was incorrectly flagged in this dataset.
Each event includes the timestamp, service, source record, and the reasons it was flagged.

## Event Flow

For every detected anomaly, `EventProducer` publishes an event to the shared in-memory
`anomaly-events` `EventTopic`. `EventConsumer` reads that same topic and returns the events as
the downstream AIOps output. The event message contains type, timestamp, service, reasons, and
the original source record.

## Issues Found and Corrected

1. `ERROR` logs were not detected because the detector checked for `WARNING`.
2. The producer and consumer used different topic instances, so the consumer received zero
	events. Both now use the same `anomaly-events` topic.
3. Pipeline imports worked only when `src` was manually added to `PYTHONPATH`. Package-aware
	imports now support both pytest and direct script execution.
4. The disabled Fibonacci test expected `89`, but the correct value for index 10 is `55`.
5. Additional tests cover data loading, direct execution, event flow, empty events, and topic
	clearing.

## Final Execution Result

Running `python3 src/aiops_pipeline.py` produced:

```text
Records processed: 10
Anomalies detected: 2
Events consumed: 2
```

The final output identifies the payment-service timeout at 10:05 and the database connection
timeout with resource saturation at 10:06.

## Validation

The final validation completed with 16 passing tests and 100% total coverage. The coverage
workflow enforces a minimum of 90%.

## Limitation and Improvement

The detector uses fixed thresholds and does not learn the service's normal baseline. Adaptive
thresholds or a time-series model could account for normal variation, sustained trends, and
seasonal behaviour.

## Reproduce the Demonstration

From the repository root:

```bash
python3 -m pip install -r requirements.txt
python3 -m pip install pytest coverage pytest-cov
python3 src/aiops_pipeline.py
python3 -m pytest --cov=src --cov-report=term-missing --verbose
coverage report --fail-under=90
```

The GitHub Skills exercise issue is available at:

https://github.com/Sandhya313/github-skills-challenge/issues/2
# Test with Actions

<img src="https://octodex.github.com/images/Professortocat_v2.png" align="right" height="200px" />

Hey Sandhya313!

Mona here. I'm done preparing your exercise. Hope you enjoy! 💚

Remember, it's self-paced so feel free to take a break! ☕️

[![](https://img.shields.io/badge/Go%20to%20Exercise-%E2%86%92-1f883d?style=for-the-badge&logo=github&labelColor=197935)](https://github.com/Sandhya313/github-skills-challenge/issues/2)

---

&copy; 2025 GitHub &bull; [Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/code_of_conduct.md) &bull; [MIT License](https://gh.io/mit)

