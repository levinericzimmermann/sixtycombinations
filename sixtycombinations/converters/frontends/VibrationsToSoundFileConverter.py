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

        self.csound_score_converter = converters.frontends.csound.CsoundScoreConverter(
            "sixtycombinations/synthesis/Orchestra{}{}.sco".format(
                nth_cycle, nth_speaker
            ),
            p1=lambda vibration: vibration.instrument,
            p4=lambda vibration: vibration.pitch.frequency,
            p5=lambda vibration: vibration.amplitude,
            p6=lambda vibration: vibration.attack_duration * vibration.duration,
            p7=lambda vibration: vibration.release_duration * vibration.duration,
            p8=lambda vibration: vibration.glissando_pitch_at_start.frequency,
            p9=lambda vibration: vibration.glissando_pitch_at_end.frequency,
            p10=lambda vibration: vibration.glissando_duration_at_start
            * vibration.duration,
            p11=lambda vibration: vibration.glissando_duration_at_end
            * vibration.duration,
            # for instrument 2 (filtered noise) return bandwidth
            p12=lambda vibration: (None, vibration.bandwidth)[
                vibration.instrument in (2,)
            ],
        )

        self.path = "{}/{}_{}.wav".format(
            constants.LOUDSPEAKER_MONO_FILES_BUILD_PATH_ABSOLUTE,
            self.nth_cycle,
            self.nth_speaker,
        )

        self.csound_converter = converters.frontends.csound.CsoundConverter(
            self.path,
            "sixtycombinations/synthesis/Orchestra.orc",
            self.csound_score_converter,
            converters.frontends.csound_constants.SILENT_FLAG,
            converters.frontends.csound_constants.FORMAT_64BIT,
        )

    # ######################################################## #
    #                    public method                         #
    # ######################################################## #

    def convert(self, event_to_convert: ConvertableEvent) -> None:

        # render wav file
        self.csound_converter.convert(event_to_convert)

        # remove score file
        os.remove(self.csound_score_converter.path)
