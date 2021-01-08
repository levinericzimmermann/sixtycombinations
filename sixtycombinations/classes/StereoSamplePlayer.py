from mutwo import events
from mutwo import parameters


class StereoSamplePlayer(events.basic.SimpleEvent):
    def __init__(
        self,
        duration: parameters.durations.abc.DurationType,
        path: str,
        panning: float,
    ):
        super().__init__(duration)
        self.path = path
        self.panning = panning
