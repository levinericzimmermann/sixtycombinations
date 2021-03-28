import functools
import operator

from mutwo.events import basic
from mutwo.parameters import volumes

from sixtycombinations.constants import N_ITERATIONS_OF_ISIS_PHRASES

# VAR:   duration, pitch, volume, consonants, vowel
# TYPES: beats, cent distance to previous pitch, loudness, tuple(str), str
RAW_PHRASES = (
    # Mors omnia solvit.
    (
        # Mors
        (4, 0, 1, ("m",), "o"),
        (2, None, 1, ("R", "s"), "_"),
        # omnia
        (2, 0, 1, tuple([]), "o"),
        (4, 100, 1, ("m", "n"), "i"),
        (2, 0, 1, tuple([]), "a"),
        (1, None, 1, tuple([]), "_"),
        # solvit
        (2, 300, 1, ("s",), "o"),
        (2, 100, 1, tuple([]), "o"),
        (1, 0, 0.5, ("l", "v",), "i"),
        (1, None, 0, ("t",), "_"),
    ),
    # Nascentes morimur,
    (
        # Nascentes
        (2, 0, 1, ("n",), "a"),
        (2, 0, 1, ("s", "k",), "e"),
        (1, 0, 1, ("n", "t",), "e"),
        (1, None, 0, ("s",), "_"),
        # morimur
        (2, 100, 1, ("m",), "o"),
        (2, 0, 1, ("R",), "i"),
        (2, -100, 1, tuple([]), "i"),
        (2, 0, 1, ("m",), "u"),
        (1, None, 0, ("R",), "_"),
    ),
    # Mors ultima linea rerum.
    (
        # Mors
        (4, 0, 1, ("m",), "o"),
        (2, None, 0, ("R", "s"), "_"),
        # ultima
        (2, 0, 1, tuple([]), "u"),
        (3, 120, 1, ("l", "t",), "i"),
        (2, 0, 1, ("m",), "a"),
        (1, None, 0, tuple([]), "_"),
        # linea
        (2, 300, 1, ("l",), "i"),
        (2, 100, 1, ("n",), "e"),
        (2, 0, 1, tuple([]), "a"),
        (1, None, 0, tuple([]), "_"),
        # rerum
        (3, 500, 1, ("R",), "e"),
        (2, 0, 1, ("R",), "u"),
        (2, None, 0, ("m",), "_"),
    ),
    # Ortus cuncta suos repetunt matremque requirunt,
    # (
    #     # Ortus
    #     (1, 0, 1, tuple([]), "o"),
    #     (1, 0, 0, ("R", "t"), "u"),
    #     (1, None, 0, ("s",), "_"),
    #     # cuncta
    #     (1, 0, 0, ("k",), "u"),
    #     (1, 0, 1, ("n", "k", "t",), "a"),
    #     # suos
    #     (1, 0, 1, ("s",), "u"),
    #     (1, 0, 1, tuple([]), "o"),
    #     (1, None, 0, ("s",), "_"),
    #     # repetunt
    #     (1, 0, 1, ("R",), "e"),
    #     (1, 0, 1, ("p",), "e"),
    #     (1, 0, 1, ("t",), "u"),
    #     (1, None, 0, ("n", "t"), "_"),
    #     # matremque
    #     (1, 0, 1, ("m",), "a"),
    #     (1, 0, 1, ("t", "R"), "e"),
    #     (1, 0, 1, ("m", "k"), "u"),
    #     (2, 0, 1, tuple([]), "e"),
    #     # requirunt
    #     (1, 0, 1, ("R",), "e"),
    #     (1, 0, 1, ("k",), "u"),
    #     (1, 0, 1, tuple([]), "i"),
    #     (3, 0, 1, ("R",), "u"),
    #     (1, None, 0, ("n", "t"), "_"),
    # ),
    # Et redit ad nihilum quod fuit ante nihil.
    (
        # Et
        (1, 0, 1, tuple([]), "e"),
        (1, None, 0, ("t",), "_"),
        # redit
        (1, 0, 0, ("R",), "e"),
        (1, 0, 0, ("d",), "i"),
        (1, None, 0, ("t",), "_"),
        # ad
        (1, 0, 1, tuple([]), "a"),
        (1, None, 0, ("d",), "_"),
        # nihilum
        (1, 0, 1, ("n",), "i"),
        (1, 0, 1, ("H",), "i"),
        (1, 0, 1, ("l",), "u"),
        (1, None, 0, ("m",), "_"),
        # quod
        (1, 0, 1, ("k",), "u"),
        (1, 0, 1, tuple([]), "o"),
        (1, None, 0, ("d",), "_"),
        # fuit
        (1, 0, 1, ("f",), "u"),
        (1, 0, 1, tuple([]), "i"),
        (1, None, 0, ("t",), "_"),
        # ante
        (1, 0, 1, tuple([]), "a"),
        (1, 0, 0, ("n", "t",), "e"),
        # nihil
        (1, 0, 1, ("n",), "i"),
        (1, 0, 1, ("H",), "i"),
        (1, None, 0, ("l",), "_"),
    ),
)


SINGING_PHRASES = []

for raw_phrase in RAW_PHRASES:
    converted_phrase = basic.SequentialEvent([])

    for duration, pitch, volume, consonants, vowel in raw_phrase:
        event = basic.SimpleEvent(duration)
        event.pitch = pitch
        event.volume = volumes.DirectVolume(volume)
        event.consonants = consonants
        event.vowel = vowel
        converted_phrase.append(event)

    for event_index, event in enumerate(converted_phrase):
        previous_pitch = None
        if event.pitch:
            for previous_event in reversed(converted_phrase[:event_index]):
                if previous_event.pitch:
                    previous_pitch = previous_event.pitch
                    break
        if previous_pitch:
            event.pitch_distance = event.pitch - previous_pitch
        else:
            event.pitch_distance = 0

    SINGING_PHRASES.append(converted_phrase)


SINGING_PHRASES = functools.reduce(
    operator.add,
    tuple(
        tuple(phrase.copy() for phrase in SINGING_PHRASES)
        for _ in range(N_ITERATIONS_OF_ISIS_PHRASES)
    ),
)
