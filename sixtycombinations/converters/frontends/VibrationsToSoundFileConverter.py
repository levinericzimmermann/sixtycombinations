import os

from mutwo import converters
from mutwo.events import basic

from sixtycombinations import classes
from sixtycombinations import constants


ConvertableEvent = basic.SimultaneousEvent[basic.SequentialEvent[classes.Vibration]]


class VibrationsToSoundFileConverter(converters.abc.Converter):
    def __init__(self, nth_cycle: int, nth_speaker: int):
        self.nth_cycle = nth_cycle
        self.nth_speaker = nth_speaker

    # ######################################################## #
    #                    public method                         #
    # ######################################################## #

    def convert(
        self, event_to_convert: ConvertableEvent
    ) -> basic.SequentialEvent[classes.Vibration]:

        csound_score_converter = converters.frontends.csound.CsoundScoreConverter(
            "sixtycombinations/synthesis/SineGenerator.sco",
            p4=lambda vibration: vibration.pitch.frequency,
            p5=lambda vibration: vibration.amplitude,
            p6=lambda vibration: vibration.attack_duration,
            p7=lambda vibration: vibration.release_duration,
        )
        path = "{}/{}_{}.wav".format(
            constants.LOUDSPEAKER_MONO_FILES_BUILD_PATH_RELATIVE,
            self.nth_cycle,
            self.nth_speaker,
        )
        csound_converter = converters.frontends.csound.CsoundConverter(
            path,
            "sixtycombinations/synthesis/SineGenerator.orc",
            csound_score_converter,
            "--format=double",  # 64 bit floating point
        )
        csound_converter.convert(event_to_convert)

        os.remove(csound_score_converter.path)  # remove score file
