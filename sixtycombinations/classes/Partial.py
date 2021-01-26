import typing

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
        nth_active_partial: int,
        nth_partial: int,
        is_connection_pitch_to_previous_harmony: bool,
        is_connection_pitch_to_next_harmony: bool,
        loudspeaker: Loudspeaker,
        rhythmical_data_per_state: typing.Tuple[typing.Tuple[typing.Any]],
        nth_cycle: int,
    ):
        """info for rhythmical data (see GROUPS.py)

        The rhythmical data contain the following information:
            1. How often the rhythm get repeated (int)
            2. How many periods one beat last (int)
            3. The respective rhythm with duration values in seconds
               (basic.SequentialEvent[basic.SimpleEvent])
            4. Indispensability of each beat (typing.Tuple[int])
        """

        duration = sum((attack, sustain, release)) * (1 / pitch.frequency)

        super().__init__(duration)

        self.pitch = pitch
        self.attack = attack
        self.sustain = sustain
        self.release = release
        self.nth_active_partial = nth_active_partial
        self.nth_partial = nth_partial
        self.is_connection_pitch_to_previous_harmony = (
            is_connection_pitch_to_previous_harmony
        )
        self.is_connection_pitch_to_next_harmony = is_connection_pitch_to_next_harmony
        self.loudspeaker = loudspeaker
        self.rhythmical_data_per_state = rhythmical_data_per_state
        self.nth_cycle = nth_cycle

    def __repr__(self):
        return "Partial({})".format(self.nth_partial)

    @property
    def period_duration(self) -> float:
        return 1 / self.pitch.frequency
