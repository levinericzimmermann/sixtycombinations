from mutwo import converters
from mutwo.events import basic

from sixtycombinations import classes

ConvertableEvent = basic.SequentialEvent[classes.Partial]


class PartialsToVibrationsConverter(converters.abc.MutwoEventConverter):
    def convert(
        self, event_to_convert: ConvertableEvent
    ) -> basic.SequentialEvent[classes.Vibration]:
        pass
