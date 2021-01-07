from mutwo.events import basic
from mutwo.parameters import pitches

from sixtycombinations.classes import Loudspeaker


class Vibration(basic.SimpleEvent):
    def __init__(
        self,
        pitch: pitches.JustIntonationPitch,
        duration: float,
        loudness_level: int,
        loudspeaker: Loudspeaker,
    ):
        super().__init__(duration)
        self.pitch = pitch
        self.loudness_level = loudness_level
        self.loudspeaker = loudspeaker
