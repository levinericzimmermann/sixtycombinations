from mutwo import events
from mutwo import parameters


class SamplePlayer(events.basic.SimpleEvent):
    def __init__(
        self,
        duration: parameters.durations.abc.DurationType,
        start: float,
        path: str,
    ):
        super().__init__(duration)
        self.start = start
        self.path = path
