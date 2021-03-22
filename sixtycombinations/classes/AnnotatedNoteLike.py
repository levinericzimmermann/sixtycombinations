import numbers
import typing


from mutwo.events import music
from mutwo import parameters

PitchOrPitches = typing.Union[
    parameters.abc.Pitch, typing.Iterable, numbers.Number, None
]

Volume = typing.Union[parameters.abc.Volume, numbers.Number]


class AnnotatedNoteLike(music.NoteLike):
    """NoteLike for ISiS."""

    def __init__(
        self,
        pitch_or_pitches: PitchOrPitches,
        duration: parameters.abc.DurationType,
        volume: numbers.Number,
        consonants: typing.Tuple[str],
        vowel: str,
    ):
        super().__init__(pitch_or_pitches, duration, volume)
        self.consonants = consonants
        self.vowel = vowel
