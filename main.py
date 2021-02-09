"""Render sound files."""

import os
import time
import threading

import sox

from mutwo import converters
from mutwo.events import basic

import sixtycombinations


def _is_active(node: basic.SimpleEvent) -> bool:
    return isinstance(node, sixtycombinations.classes.Vibration)


def _print_density_per_speaker(
    nested_vibrations: basic.SimultaneousEvent, n_steps: int = 1000
):
    print("Density per speaker:")
    for nth_cycle, cycle in enumerate(nested_vibrations):
        for nth_speaker, speaker_data in enumerate(cycle):
            duration = speaker_data[0].duration
            n_active_positions = 0
            for nth_step in range(n_steps):
                position = duration * (nth_step / n_steps)
                is_event_active = tuple(
                    _is_active(seq_ev.get_event_at(position)) for seq_ev in speaker_data
                )
                if any(is_event_active):
                    n_active_positions += 1

            message = "{}.{}: {}%".format(
                nth_cycle, nth_speaker, round((n_active_positions / n_steps) * 100, 2)
            )
            print(message)
    print("")


def _convert_partials_to_vibrations() -> basic.SimultaneousEvent:
    partials_to_vibrations_converter = (
        sixtycombinations.converters.symmetrical.PartialsToVibrationsConverter()
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


def _render_vibrations_to_sound_files(nested_vibrations: basic.SimultaneousEvent):
    threads = []
    for nth_cycle, cycle in enumerate(nested_vibrations):
        for nth_speaker, speaker_data in enumerate(cycle):
            sound_file_converter = sixtycombinations.converters.frontends.VibrationsToSoundFileConverter(
                nth_cycle, nth_speaker
            )
            thread = threading.Thread(
                target=lambda: sound_file_converter.convert(speaker_data)
            )
            thread.start()
            threads.append(thread)

    while any([th.isAlive() for th in threads]):
        time.sleep(0.5)


def _cut_sound_file(
    absolute_start_time: float,
    csound_score_converter: converters.frontends.csound.CsoundScoreConverter,
    nth_cycle: int,
    nth_speaker: int,
):
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

    if sixtycombinations.constants.CUT_UP:
        sample0_duration = (
            sixtycombinations.constants.CUT_UP[1]
            - sixtycombinations.constants.CUT_UP[0]
        ) - absolute_start_time
    else:
        sample0_duration = sixtycombinations.constants.DURATION - absolute_start_time

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

    csound_converter = converters.frontends.csound.CsoundConverter(
        absolute_sample_path,
        "sixtycombinations/synthesis/Remix.orc",
        csound_score_converter,
            converters.frontends.csound_constants.SILENT_FLAG,
            converters.frontends.csound_constants.FORMAT_64BIT
    )
    csound_converter.convert(basic.SimultaneousEvent([part0, part1]))
    os.remove(csound_score_converter.path)  # remove score file


def _cut_sound_files(nested_vibrations: basic.SimultaneousEvent):
    threads = []
    for nth_cycle, absolute_start_time in enumerate(
        sixtycombinations.constants.ABSOLUTE_START_TIME_PER_GROUP
    ):
        for nth_speaker, _ in enumerate(nested_vibrations[nth_cycle]):

            csound_score_converter = converters.frontends.csound.CsoundScoreConverter(
                "sixtycombinations/synthesis/Remix{}{}.sco".format(
                    nth_cycle, nth_speaker
                ),
                p4=lambda sample_player: sample_player.start,
                p5=lambda sample_player: sample_player.path,
            )
            thread = threading.Thread(
                target=lambda: _cut_sound_file(
                    absolute_start_time, csound_score_converter, nth_cycle, nth_speaker
                )
            )
            thread.start()
            threads.append(thread)

    while any([th.isAlive() for th in threads]):
        time.sleep(0.5)


def _mix_sound_files(n_channels: int):
    if n_channels == 2:
        csound_score_converter = converters.frontends.csound.CsoundScoreConverter(
            "sixtycombinations/synthesis/StereoMixdown.sco",
            p4=lambda stereo_sample_player: stereo_sample_player.path,
            p5=lambda stereo_sample_player: stereo_sample_player.panning,
        )
        csound_converter = converters.frontends.csound.CsoundConverter(
            "{}/stereo.wav".format(sixtycombinations.constants.MIX_PATH),
            "sixtycombinations/synthesis/StereoMixdown.orc",
            csound_score_converter,
            converters.frontends.csound_constants.SILENT_FLAG,
            converters.frontends.csound_constants.FORMAT_64BIT
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
                duration_in_seconds_of_sample = sox.file_info.duration(sample_path)
                simultaneous_event.append(
                    sixtycombinations.classes.StereoSamplePlayer(
                        duration_in_seconds_of_sample, sample_path, panning
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

    _print_density_per_speaker(nested_vibrations)

    # (2) render partials to sound files
    _render_vibrations_to_sound_files(nested_vibrations)

    # (3) adjust (cut) sound files
    _cut_sound_files(nested_vibrations)

    # (4) mix sound files together to one single wav file
    _mix_sound_files(2)
