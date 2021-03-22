from mutwo.events import basic
from mutwo.parameters import volumes

# TODO(write pitch in absolute cent values and let
# program calculate the difference. For manual composing
# is easier to think in absolute values)

# VAR:   duration, pitch, volume, consonants, vowel
# TYPES: beats, cent distance to previous pitch, loudness, tuple(str), str
RAW_PHRASES = (
    # Mors omnia solvit.
    (
        # Mors
        (3, 0, 1, ("m",), "o"),
        (1, None, 1, ("R", "s"), "_"),
        # omnia
        (2, 0, 1, tuple([]), "o"),
        (4, 200, 1, ("m", "n"), "i"),
        (2, -200, 1, tuple([]), "a"),
        (1, None, 1, tuple([]), "_"),
        # solvit
        (2, 300, 1, ("s",), "o"),
        (2, -200, 1, tuple([]), "o"),
        (3, -100, 0.5, ("l", "v",), "i"),
        (1, None, 0, ("t",), "_"),
    ),
    # Nascentes morimur,
    (
        # Nascentes
        (2, 0, 1, ("n",), "a"),
        (4, 0, 1, ("s", "k",), "e"),
        (2, 0, 1, ("n", "t",), "e"),
        (2, None, 0, ("s",), "_"),
        # morimur
        (2, 100, 1, ("m",), "o"),
        (4, 0, 1, ("R",), "i"),
        (2, -100, 1, tuple([]), "i"),
        (2, 0, 1, ("m",), "u"),
        (2, None, 0, ("R",), "_"),
    ),
    # Mors ultima linea rerum.
    (
        # Mors
        (3, 0, 1, ("m",), "o"),
        (1, None, 0, ("R", "s"), "_"),
        # ultima
        (2, 0, 1, tuple([]), "u"),
        (3, 200, 1, ("l", "t",), "i"),
        (2, -200, 1, ("m",), "a"),
        (1, None, 0, tuple([]), "_"),
        # linea
        (2, 300, 1, ("l",), "i"),
        (4, -100, 1, ("n",), "e"),
        (2, -200, 1, tuple([]), "a"),
        (1, None, 0, tuple([]), "_"),
        # rerum
        (4, 0, 1, ("R",), "e"),
        (2, -100, 1, ("R",), "u"),
        (2, None, 0, ("m",), "_"),
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

    SINGING_PHRASES.append(converted_phrase)
