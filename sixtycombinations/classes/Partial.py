from mutwo.events import basic
from mutwo.parameters import pitches

from sixtycombinations.classes import Loudspeaker


class Partial(basic.SimpleEvent):
    def __init__(
        self,
        pitch: pitches.JustIntonationPitch,
        attack: int,
        sustain: float,
        release: int,
        nth_partial: int,
        is_connection_pitch_to_previous_harmony: bool,
        is_connection_pitch_to_next_harmony: bool,
        loudspeaker: Loudspeaker,
    ):
        duration = sum((attack, sustain, release)) * (1 / pitch.frequency)
        super().__init__(duration)
        self.pitch = pitch
        self.attack = attack
        self.sustain = sustain
        self.release = release
        self.nth_partial = nth_partial
        self.is_connection_pitch_to_previous_harmony = (
            is_connection_pitch_to_previous_harmony
        )
        self.is_connection_pitch_to_next_harmony = is_connection_pitch_to_next_harmony
        self.loudspeaker = loudspeaker

    def __repr__(self):
        return "Partial({})".format(self.nth_partial)
