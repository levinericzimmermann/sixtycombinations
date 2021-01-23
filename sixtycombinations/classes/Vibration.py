from mutwo.events import basic
from mutwo.parameters import pitches


class Vibration(basic.SimpleEvent):
    def __init__(
        self,
        pitch: pitches.JustIntonationPitch,
        duration: float,
        amplitude: float,
        attack_duration: float = 0.1,
        release_duration: float = 0.1,
    ):
        super().__init__(duration)
        self.pitch = pitch
        self.amplitude = amplitude
        self.attack_duration = attack_duration
        self.release_duration = release_duration

    def __repr__(self):
        return "Vibration({}, {}, {})".format(
            str(self.pitch.ratio), round(self.duration, 2), round(self.amplitude, 1)
        )
