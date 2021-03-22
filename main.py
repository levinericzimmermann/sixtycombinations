"""Render and mix sound files."""

import functools
import operator
import os
import threading
import time
import typing

import sox

from mutwo import converters
from mutwo.events import basic
from mutwo.parameters import pitches

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
    note_likes_per_group = basic.SimultaneousEvent([])
    for cycle in sixtycombinations.constants.NESTED_PARTIALS:
        groupA = basic.SimultaneousEvent([])
        groupB = basic.SimultaneousEvent([])
        for speaker in cycle:
            for part, partials in zip((groupA, groupB), speaker):
                part.extend(partials_to_note_likes_converter.convert(partials))
        note_likes_per_group.append((groupA, groupB))
    return note_likes_per_group


def _render_rhythmical_grids_to_sound_files(
    rhythmical_grids: typing.Tuple[basic.SequentialEvent[basic.SimpleEvent]],
):
    for nth_cycle, rhythmical_grid in enumerate(rhythmical_grids):
        symmetrical_converter = sixtycombinations.converters.symmetrical.RhythmicalGridToAnnotatedNoteLikesConverter(
            nth_cycle
        )
        frontend_converter = sixtycombinations.converters.frontends.AnnotatedNoteLikesToSoundFileConvert(
            nth_cycle
        )
        frontend_converter.convert(symmetrical_converter.convert(rhythmical_grid))


def _render_vibrations_to_filtered_isis_files(
    nested_vibrations: basic.SimultaneousEvent,
):
    threads = []
    for nth_cycle, cycle in enumerate(nested_vibrations):
        sample_player_event = basic.SimpleEvent(sixtycombinations.constants.DURATION)
        sample_player_event.path = "{}/{}.wav".format(
            sixtycombinations.constants.ISIS_FILES_BUILD_PATH, nth_cycle
        )

        for nth_speaker, speaker_data in enumerate(cycle):
            adapted_speaker_data = basic.SimultaneousEvent(
                [basic.SequentialEvent([sample_player_event])] + speaker_data[:]
            )

            sound_file_converter = sixtycombinations.converters.frontends.VibrationsToFilteredIsisSoundFileConverter(
                nth_cycle, nth_speaker
            )
            thread = threading.Thread(
                target=lambda: sound_file_converter.convert(adapted_speaker_data)
            )
            thread.start()
            threads.append(thread)

    while any([th.isAlive() for th in threads]):
        time.sleep(0.5)


def _render_note_likes_to_midi_files(nested_note_likes: basic.SimultaneousEvent):
    for nth_cycle, cycle in enumerate(nested_note_likes):
        for is_a_or_b, a_or_b in enumerate(cycle):
            a_or_b.duration *= 2  # due to midi tempo 120
            midi_file_converter = converters.frontends.midi.MidiFileConverter(
                "{}/instr{}_{}.mid".format(
                    sixtycombinations.constants.MIDI_FILES_BUILD_PATH,
                    nth_cycle,
                    is_a_or_b,
                ),
                available_midi_channels=tuple(range(12)),
                distribute_midi_channels=False,
                midi_file_type=1,
            )
            midi_file_converter.convert(a_or_b)


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


def _render_singing_phrases_dummies():
    scale = tuple(
        pitches.WesternPitch(pitch, concert_pitch=440)
        for pitch, octave in zip("e f g a b c d e".split(" "), (4, 4, 4, 4, 4, 5, 5, 5))
    )
    for nth_phrase, phrase in enumerate(sixtycombinations.constants.SINGING_PHRASES):
        adjusted_phrase = phrase.copy()
        for event in adjusted_phrase:
            if event.pitch is not None:
                event.pitch = scale[event.pitch]
            else:
                event.pitch = pitches.WesternPitch("c", -1, concert_pitch=440)

        isis_score_converter = converters.frontends.isis.IsisScoreConverter(
            "sixtycombinations/synthesis/isis-score-dummy-phrase-{}.isis".format(
                nth_phrase
            ),
            simple_event_to_pitch=lambda simple_event: simple_event.pitch,
            global_transposition=5,
            tempo=95,
        )

        isis_converter = converters.frontends.isis.IsisConverter(
            "{}/isis/0-dummy-phrase-{}.wav".format(
                sixtycombinations.constants.BUILD_PATH, nth_phrase
            ),
            isis_score_converter,
            "-sv EL",  # singing voice alt
            "-ss eP",  # singing style jG
            converters.frontends.isis_constants.SILENT_FLAG,
            remove_score_file=False,
        )

        isis_converter.convert(adjusted_phrase)


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
    # render dummy files for different singing phrases:
    # _render_singing_phrases_dummies()
    # make reaper marker files for better structure in reaper project:
    # _convert_groups_to_reaper_marker_file()

    # raise ValueError

    nested_note_likes = _convert_partials_to_note_likes()
    _render_note_likes_to_midi_files(nested_note_likes)

    print("midi - done")

    # _render_rhythmical_grids_to_sound_files(
    #     sixtycombinations.constants.ISIS_RHYTHMICAL_GRID_PER_CYCLE
    # )

    # convert partials to vibrations
    nested_vibrations = _convert_partials_to_vibrations(apply_frequency_response=False)
    _render_vibrations_to_filtered_isis_files(nested_vibrations)

    # logging etc.
    # nested_vibrations.cut_out(0, 122)
    # print(nested_vibrations.duration)
    # _print_density_per_speaker(nested_vibrations)

    # render vibrations to sound files
    # _render_vibrations_to_sound_files(nested_vibrations)

    # mix sound files together to one single wav file
    # _mix_sound_files(2)
