from pathlib import Path
import runpy

from src.anomaly_detector import AnomalyDetector
from src.aiops_pipeline import load_data, run_pipeline
from src.event_consumer import EventConsumer
from src.event_producer import EventProducer
from src.event_topic import EventTopic


def test_normal_record_is_not_anomaly():
    detector = AnomalyDetector()

    record = {
        "timestamp": "2026-09-20T10:00:00",
        "service": "payment-service",
        "response_time_ms": 120,
        "cpu_percent": 42,
        "memory_percent": 51,
        "log_level": "INFO",
        "message": "Payment request processed successfully"
    }

    assert detector.detect(record) is None


def test_anomalous_record_is_detected():
    detector = AnomalyDetector()

    record = {
        "timestamp": "2026-09-20T10:05:00",
        "service": "payment-service",
        "response_time_ms": 610,
        "cpu_percent": 75,
        "memory_percent": 70,
        "log_level": "ERROR",
        "message": "Payment service timeout"
    }

    event = detector.detect(record)

    assert event is not None
    assert event["type"] == "ANOMALY"
    assert "Error log detected" in event["reasons"]


def test_pipeline_consumes_detected_events():
    data_path = Path(__file__).parents[1] / "data" / "service_data.json"
    result = run_pipeline(str(data_path))

    assert result["records_processed"] == 10
    assert len(result["anomalies_detected"]) == 2
    assert len(result["events_consumed"]) == 2
    assert result["events_consumed"] == result["anomalies_detected"]


def test_load_data_reads_service_records():
    data_path = Path(__file__).parents[1] / "data" / "service_data.json"

    data = load_data(str(data_path))

    assert len(data) == 10
    assert data[0]["service"] == "payment-service"


def test_pipeline_script_prints_results(capsys, monkeypatch):
    monkeypatch.chdir(Path(__file__).parents[1])

    runpy.run_path("src/aiops_pipeline.py", run_name="__main__")

    output = capsys.readouterr().out
    assert "Records processed: 10" in output
    assert "Anomalies detected: 2" in output
    assert "Events consumed: 2" in output


def test_producer_publishes_event():
    topic = EventTopic("anomaly-events")
    producer = EventProducer(topic)

    event = {
        "type": "ANOMALY",
        "service": "payment-service"
    }

    assert producer.publish(event)
    assert len(topic.get_messages()) == 1


def test_consumer_receives_event():
    topic = EventTopic("anomaly-events")
    producer = EventProducer(topic)
    consumer = EventConsumer(topic)

    event = {
        "type": "ANOMALY",
        "service": "payment-service"
    }

    producer.publish(event)

    messages = consumer.consume()

    assert len(messages) == 1


def test_producer_rejects_empty_event():
    topic = EventTopic("anomaly-events")
    producer = EventProducer(topic)

    assert not producer.publish(None)
    assert topic.get_messages() == []


def test_topic_clear_removes_messages():
    topic = EventTopic("anomaly-events")
    topic.publish({"type": "ANOMALY"})

    topic.clear()

    assert topic.get_messages() == []