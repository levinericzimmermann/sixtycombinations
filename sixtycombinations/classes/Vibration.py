from mutwo.events import basic
from mutwo.parameters import pitches


class Vibration(basic.SimpleEvent):
    def __init__(
        self, pitch: pitches.JustIntonationPitch, duration: float, amplitude: float,
    ):
        super().__init__(duration)
        self.pitch = pitch
        self.amplitude = amplitude

    def __repr__(self):
        return "Vibration({}, {}, {})".format(
            str(self.pitch.ratio), round(self.duration, 2), round(self.amplitude, 1)
        )
