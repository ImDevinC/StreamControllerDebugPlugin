import tracemalloc

from loguru import logger as log
from src.backend.PluginManager.ActionCore import ActionCore
from src.backend.DeckManagement.InputIdentifier import InputEvent, Input
from src.backend.PluginManager.EventAssigner import EventAssigner


class DebugAction(ActionCore):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._tracing = False
        self.event_manager.add_event_assigner(
            EventAssigner(
                id="profile",
                ui_label="Start Profiler/Take Snapshot",
                default_event=Input.Key.Events.DOWN,
                callback=self._on_snapshot,
            )
        )
        self.event_manager.add_event_assigner(
            EventAssigner(
                id="profiler",
                ui_label="Stop Profiling",
                default_event=Input.Key.Events.HOLD_STOP,
                callback=self._on_profiler_stop,
            )
        )

    def on_ready(self):
        super().on_ready()
        self.set_center_label("Press to start profiling")

    def _on_snapshot(self, _):
        if not self._tracing:
            log.debug("Starting memory profiling")
            tracemalloc.start()
            self._snapshot = tracemalloc.take_snapshot()
            self._first_snapshot = self._snapshot
            self.set_center_label("Press to take snapshot")
            self._tracing = True
            return
        self._take_snapshot()

    def _on_profiler_stop(self, _):
        if self._tracing:
            log.debug("Stopping memory profiling and taking snapshot")
            self._take_snapshot()
            tracemalloc.stop()
            self.set_center_label("Profiling stopped. Check logs for details.")
            self._tracing = False
            return
        log.warning("Profiler is not running. Cannot stop profiling.")

    def _take_snapshot(self):
        snapshot2 = tracemalloc.take_snapshot()
        top_stats = snapshot2.compare_to(self._first_snapshot, 'lineno')
        log.debug("First snapshot memory usage differences:")
        log.debug("\n".join(str(stat) for stat in top_stats[:10]))
        top_stats = snapshot2.compare_to(self._snapshot, 'lineno')
        log.debug("Latest snapshot memory usage differences:")
        log.debug("\n".join(str(stat) for stat in top_stats[:10]))
        self._snapshot = snapshot2
