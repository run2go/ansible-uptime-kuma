import enum

import plugins.modules.monitor as module


class FakeMonitorType(enum.Enum):
    HTTP = "http"
    PING = "ping"


class TestMonitorDiff:
    def test_create_diff_has_no_before(self):
        options = {"name": "monitor 1", "type": FakeMonitorType.HTTP, "url": "http://127.0.0.1"}
        diff = module.monitor_diff({}, options)
        assert diff["before"] == ""
        assert "name: monitor 1" in diff["after"]
        assert "type: http" in diff["after"]

    def test_edit_diff_has_before_and_after(self):
        before_monitor = {"id": 1, "name": "monitor 1", "type": FakeMonitorType.HTTP}
        options = {"id": 1, "name": "monitor 1", "type": FakeMonitorType.PING}
        diff = module.monitor_diff(before_monitor, options)
        assert "type: http" in diff["before"]
        assert "type: ping" in diff["after"]
        # id is internal bookkeeping, must not leak into the diff view
        assert "id:" not in diff["before"]
        assert "id:" not in diff["after"]

    def test_enum_values_are_unwrapped(self):
        options = {"type": FakeMonitorType.HTTP}
        diff = module.monitor_diff({}, options)
        assert diff["after"].strip() == "type: http"
