from mutwo.events import basic
from mutwo.parameters import volumes

# duration, pitch, volume, consonants, vowel
RAW_PHRASES = (
    # Mors omnia solvit.
    (
        # Mors
        (1.5, 0, 1, ("m",), "o"),
        (0.5, None, 1, ("R", "s"), "_"),
        # omnia
        (1, 0, 1, tuple([]), "o"),
        (2, 1, 1, ("m", "n"), "i"),
        (1, 0, 1, tuple([]), "a"),
        (0.5, None, 1, tuple([]), "_"),
        # solvit
        (1, 2, 1, ("s",), "o"),
        (1, 1, 1, tuple([]), "o"),
        (1.5, 0, 0.5, ("l", "v",), "i"),
        (0.5, None, 0, ("t",), "_"),
    ),
    # Nascentes morimur,
    (
        # Nascentes
        (1, 0, 1, ("n",), "a"),
        (2, 0, 1, ("s", "k",), "e"),
        (1, 0, 1, ("n", "t",), "e"),
        (1, None, 0, ("s",), "_"),
        # morimur
        (1, 1, 1, ("m",), "o"),
        (2, 1, 1, ("R",), "i"),
        (1, 0, 1, tuple([]), "i"),
        (1, 0, 1, ("m",), "u"),
        (1, None, 0, ("R",), "_"),
    ),
    # Mors ultima linea rerum.
    (
        # Mors
        (1.5, 0, 1, ("m",), "o"),
        (0.5, None, 0, ("R", "s"), "_"),
        # ultima
        (1, 0, 1, tuple([]), "u"),
        (1.5, 1, 1, ("l", "t",), "i"),
        (1, 0, 1, ("m",), "a"),
        (0.5, None, 0, tuple([]), "_"),
        # linea
        (1, 2, 1, ("l",), "i"),
        (2, 1, 1, ("n",), "e"),
        (1, 0, 1, tuple([]), "a"),
        (0.5, None, 0, tuple([]), "_"),
        # rerum
        (2, 1, 1, ("R",), "e"),
        (1, 0, 1, ("R",), "u"),
        (1, None, 0, ("m",), "_"),
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
