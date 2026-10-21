from streaming_cdc.processor import process

def test_dedupe_and_order():
    result = process([
      {"event_id":"1","key":"x","version":2,"op":"upsert","value":"latest"},
      {"event_id":"2","key":"x","version":1,"op":"upsert","value":"old"},
      {"event_id":"1","key":"x","version":2,"op":"upsert","value":"latest"},
    ])
    assert result["state"]["x"]["value"] == "latest"
    assert result["metrics"]["stale"] == 1
    assert result["metrics"]["duplicates"] == 1

def test_invalid():
    assert process([{"bad": 1}])["metrics"]["invalid"] == 1
