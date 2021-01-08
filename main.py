"""Render sound files."""

import os

import sox

from mutwo import converters
from mutwo.events import basic

import sixtycombinations


def _convert_partials_to_vibrations() -> basic.SimultaneousEvent:
    partials_to_vibrations_converter = (
        sixtycombinations.converters.mutwo.PartialsToVibrationsConverter()
    )
    return basic.SimultaneousEvent(
        # cycles
        [
            # loudspeakers
            basic.SimultaneousEvent(
                [
                    # a / b
                    basic.SimultaneousEvent(
                        [
                            partials_to_vibrations_converter.convert(partials)
                            for partials in speaker
                        ]
                    )
                    for speaker in cycle
                ]
            )
            for cycle in sixtycombinations.constants.NESTED_PARTIALS
        ]
    )


def _render_partials_to_sound_files(nested_vibrations: basic.SimultaneousEvent):
    csound_score_converter = converters.csound.CsoundScoreConverter(
        "sixtycombinations/synthesis/SineGenerator.sco",
        p4=lambda vibration: vibration.pitch.frequency,
        p5=lambda vibration: vibration.amplitude,
    )
    for nth_cycle, cycle in enumerate(nested_vibrations):
        for nth_speaker, speaker_data in enumerate(cycle):
            path = "{}/{}_{}.wav".format(
                sixtycombinations.constants.LOUDSPEAKER_MONO_FILES_BUILD_PATH_RELATIVE,
                nth_cycle,
                nth_speaker,
            )
            csound_converter = converters.csound.CsoundConverter(
                path,
                "sixtycombinations/synthesis/SineGenerator.orc",
                csound_score_converter,
                "--format=double",  # 64 bit floating point
            )
            csound_converter.convert(speaker_data)

    os.remove(csound_score_converter.path)  # remove score file


def _cut_sound_files(nested_vibrations: basic.SimultaneousEvent):
    csound_score_converter = converters.csound.CsoundScoreConverter(
        "sixtycombinations/synthesis/Remix.sco",
        p4=lambda sample_player: sample_player.start,
        p5=lambda sample_player: '"{}"'.format(sample_player.path),
    )
    for nth_cycle, absolute_start_time in enumerate(
        sixtycombinations.constants.ABSOLUTE_START_TIME_PER_GROUP
    ):
        for nth_speaker, _ in enumerate(nested_vibrations[nth_cycle]):
            relative_sample_path = "{}/{}_{}.wav".format(
                sixtycombinations.constants.LOUDSPEAKER_MONO_FILES_BUILD_PATH_RELATIVE,
                nth_cycle,
                nth_speaker,
            )
            absolute_sample_path = "{}/{}_{}.wav".format(
                sixtycombinations.constants.LOUDSPEAKER_MONO_FILES_BUILD_PATH_ABSOLUTE,
                nth_cycle,
                nth_speaker,
            )
            duration_in_seconds_of_relative_sample = sox.file_info.duration(
                relative_sample_path
            )

            sample0_duration = (
                sixtycombinations.constants.DURATION - absolute_start_time
            )

            part0 = basic.SequentialEvent(
                [
                    sixtycombinations.classes.SamplePlayer(
                        sample0_duration, 0, relative_sample_path,
                    )
                ]
            )
            if absolute_start_time > 0:
                part0.insert(0, basic.SimpleEvent(absolute_start_time))

            part1 = basic.SequentialEvent(
                [
                    sixtycombinations.classes.SamplePlayer(
                        duration_in_seconds_of_relative_sample - sample0_duration,
                        sample0_duration,
                        relative_sample_path,
                    )
                ]
            )

            csound_converter = converters.csound.CsoundConverter(
                absolute_sample_path,
                "sixtycombinations/synthesis/Remix.orc",
                csound_score_converter,
                "--format=double",  # 64 bit floating point
            )
            csound_converter.convert(basic.SimultaneousEvent([part0, part1]))

    os.remove(csound_score_converter.path)  # remove score file


def _mix_sound_files(n_channels: int):
    if n_channels == 2:
        csound_score_converter = converters.csound.CsoundScoreConverter(
            "sixtycombinations/synthesis/StereoMixdown.sco",
            p4=lambda stereo_sample_player: '"{}"'.format(stereo_sample_player.path),
            p5=lambda stereo_sample_player: stereo_sample_player.panning,
        )
        csound_converter = converters.csound.CsoundConverter(
            "{}/stereo.wav".format(sixtycombinations.constants.MIX_PATH),
            "sixtycombinations/synthesis/StereoMixdown.orc",
            csound_score_converter,
            "--format=double",  # 64 bit floating point
        )
        simultaneous_event = basic.SimultaneousEvent([])
        for nth_cycle, loudspeakers in enumerate(
            sixtycombinations.constants.RING_POSITION_TO_LOUDSPEAKER
        ):
            n_loudspeakers = len(loudspeakers)
            for nth_loudspeaker, _ in enumerate(loudspeakers):
                panning = nth_loudspeaker / (n_loudspeakers - 1)
                sample_path = "{}/{}_{}.wav".format(
                    sixtycombinations.constants.LOUDSPEAKER_MONO_FILES_BUILD_PATH_ABSOLUTE,
                    nth_cycle,
                    nth_loudspeaker,
                )
                simultaneous_event.append(
                    sixtycombinations.classes.StereoSamplePlayer(
                        sixtycombinations.constants.DURATION, sample_path, panning
                    )
                )

        csound_converter.convert(simultaneous_event)
        os.remove(csound_score_converter.path)  # remove score file

    elif n_channels == 15:
        pass

    else:
        raise NotImplementedError()


if __name__ == "__main__":
    # (1) convert partials to vibrations
    nested_vibrations = _convert_partials_to_vibrations()

    # (2) render partials to sound files
    _render_partials_to_sound_files(nested_vibrations)

    # (3) adjust (cut) sound files
    _cut_sound_files(nested_vibrations)

    # (4) mix sound files together to one single wav file
    _mix_sound_files(2)