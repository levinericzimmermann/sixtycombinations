"""Render and mix sound files."""

import functools
import operator
import os
import threading
import time

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


def _convert_groups_to_reaper_marker_file():
    reaper_marker_file_converter = sixtycombinations.converters.frontends.GroupsToReaperMarkerFileConverter(
        "sixtycombinations/builds/reaper_marker.txt"
    )
    reaper_marker_file_converter.convert(sixtycombinations.constants.GROUPS)


def _convert_partials_to_vibrations(
    apply_frequency_response: bool,
) -> basic.SimultaneousEvent[
    basic.SimultaneousEvent[
        basic.SimultaneousEvent[
            basic.SequentialEvent[sixtycombinations.classes.Vibration]
        ]
    ]
]:
    partials_to_vibrations_converter = sixtycombinations.converters.symmetrical.PartialsToVibrationsConverter(
        apply_frequency_response=apply_frequency_response
    )
    return basic.SimultaneousEvent(
        # cycles
        [
            # loudspeakers
            basic.SimultaneousEvent(
                [
                    # a / b
                    basic.SimultaneousEvent(
                        functools.reduce(
                            operator.add,
                            (
                                partials_to_vibrations_converter.convert(partials)
                                for partials in speaker
                            ),
                        )
                    )
                    for speaker in cycle
                ]
            )
            for cycle in sixtycombinations.constants.NESTED_PARTIALS
        ]
    )


def _convert_partials_to_note_likes() -> basic.SimultaneousEvent[
    basic.SimultaneousEvent[
        basic.SimultaneousEvent[
            basic.SequentialEvent[sixtycombinations.classes.Vibration]
        ]
    ]
]:
    partials_to_note_likes_converter = (
        sixtycombinations.converters.symmetrical.PartialsToNoteLikesConverter()
    )
    note_likes = basic.SimultaneousEvent([])
    for cycle in sixtycombinations.constants.NESTED_PARTIALS:
        groupA = basic.SimultaneousEvent([])
        groupB = basic.SimultaneousEvent([])
        for speaker in cycle:
            for nth_num, partials in enumerate(speaker):
                group = (groupA, groupB)[nth_num]
                group.extend(partials_to_note_likes_converter.convert(partials))
        note_likes.append((groupA, groupB))
    return note_likes


def _render_note_likes_to_midi_files(nested_note_likes: basic.SimultaneousEvent):
    for nth_cycle, cycle in enumerate(nested_note_likes):
        for nth_group, group in enumerate(cycle):
            group.duration *= 2  # tempo 120
            midi_file_converter = converters.frontends.midi.MidiFileConverter(
                "instr{}_{}.mid".format(nth_cycle, nth_group),
                available_midi_channels=tuple(range(6)),
                distribute_midi_channels=True,
            )
            midi_file_converter.convert(group)


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
            converters.frontends.csound_constants.FORMAT_64BIT,
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
    _convert_groups_to_reaper_marker_file()

    # raise ValueError

    nested_note_likes = _convert_partials_to_note_likes()
    _render_note_likes_to_midi_files(nested_note_likes)

    print("midi - done")

    # convert partials to vibrations
    nested_vibrations = _convert_partials_to_vibrations(apply_frequency_response=False)
    # logging etc.
    # nested_vibrations.cut_out(0, 122)
    # print(nested_vibrations.duration)
    _print_density_per_speaker(nested_vibrations)

    # render vibrations to sound files
    _render_vibrations_to_sound_files(nested_vibrations)

    # mix sound files together to one single wav file
    _mix_sound_files(2)
