import operator
import os
import typing

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


class GroupsToReaperMarkerFileConverter(converters.abc.Converter):
    cycle_index_to_color = ("0 0 1", "0 21274726 1", "0 29274726 1")

    def __init__(self, path: str):
        self._path = path
        self._reaper_marker_converter = (
            converters.frontends.reaper.ReaperMarkerConverter()
        )

    def convert(
        self,
        groups_per_cycle: typing.Tuple[typing.Tuple[type(constants.GROUPS[0][0])]],
    ):
        reaper_marker_events = basic.SimultaneousEvent([])
        for nth_cycle, groups in enumerate(groups_per_cycle):
            absolute_start_time_for_cycle = constants.ABSOLUTE_START_TIME_PER_GROUP[
                nth_cycle
            ]

            for nth_group, group in enumerate(groups):
                reaper_marker_events_for_group = basic.SequentialEvent([])
                absolute_start_time_for_group = (
                    absolute_start_time_for_cycle + group.relative_start_time
                )
                absolute_start_time_for_group %= constants.DURATION
                reaper_marker_events_for_group.append(
                    basic.SimpleEvent(absolute_start_time_for_group)
                )

                for state_name in "attack sustain release".split(" "):
                    n_phases = getattr(group, state_name)
                    duration_of_state = (1 / group.fundamental.frequency) * n_phases
                    state_marker = basic.SimpleEvent(duration_of_state)
                    state_marker.name = "Group({},{})-{}".format(
                        nth_cycle, nth_group, state_name.upper()
                    )
                    state_marker.color = self.cycle_index_to_color[nth_cycle]
                    reaper_marker_events_for_group.append(state_marker)

                absolute_start_time_and_reaper_marker_events_pairs = []
                for absolute_time, state_marker in zip(
                    reaper_marker_events_for_group.absolute_times[1:],
                    reaper_marker_events_for_group[1:],
                ):
                    absolute_time %= constants.DURATION
                    absolute_start_time_and_reaper_marker_events_pairs.append(
                        (absolute_time, state_marker)
                    )

                sorted_absolute_start_time_and_reaper_marker_events_pairs = sorted(
                    absolute_start_time_and_reaper_marker_events_pairs,
                    key=operator.itemgetter(0),
                )
                if sorted_absolute_start_time_and_reaper_marker_events_pairs[0][0] != 0:
                    sorted_absolute_start_time_and_reaper_marker_events_pairs.insert(
                        0, (0, basic.SimpleEvent(1))
                    )

                sorted_absolute_start_times = tuple(
                    map(
                        lambda pair: pair[0],
                        sorted_absolute_start_time_and_reaper_marker_events_pairs,
                    )
                )

                adjusted_reaper_marker_events_for_group = basic.SequentialEvent([])
                for absolute_start_time0, absolute_start_time1, event in zip(
                    sorted_absolute_start_times,
                    sorted_absolute_start_times[1:] + (1,),
                    map(
                        lambda pair: pair[1],
                        sorted_absolute_start_time_and_reaper_marker_events_pairs,
                    ),
                ):
                    event.duration = absolute_start_time1 - absolute_start_time0
                    adjusted_reaper_marker_events_for_group.append(event)

                reaper_marker_events.append(adjusted_reaper_marker_events_for_group)

        with open(self._path, "w") as f:
            f.write(self._reaper_marker_converter.convert(reaper_marker_events))
