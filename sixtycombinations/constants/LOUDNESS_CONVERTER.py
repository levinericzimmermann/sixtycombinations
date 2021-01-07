from mutwo import converters

from sixtycombinations.constants import LOUDNESS_LEVELS
from sixtycombinations.constants import LOUDSPEAKERS

LOUDNESS_CONVERTER = {
    loudspeaker.name: tuple(
        converters.mutwo.LoudnessToAmplitudeConverter(perceived_loudness_in_sone)
        for perceived_loudness_in_sone in LOUDNESS_LEVELS
    )
    for loudspeaker in LOUDSPEAKERS.values()
}
