# Streaming CDC Reference

A runnable Python reference for change-data-capture handling: event validation, replay-safe deduplication, version ordering, deletes and dead-letter handling. Uses synthetic JSONL events. Demonstrates transferable patterns for Kafka and Spark streaming systems without claiming a deployed cluster.

## Quick start
```bash
python -m pip install -e '.[dev]'
python -m streaming_cdc --input data/events.jsonl
pytest -q
```

This local implementation does **not** guarantee exactly-once distributed processing or Kafka deployment. A production solution would add durable checkpoints, retries, schema registry integration and transactional sinks.
