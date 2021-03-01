from mutwo import converters

from sixtycombinations.constants import LOUDNESS_LEVELS
from sixtycombinations.constants import LOUDSPEAKERS

LOUDNESS_CONVERTER_WITH_FREQUENCY_RESPONSE = {
    loudspeaker.name: tuple(
        converters.symmetrical.LoudnessToAmplitudeConverter(
            perceived_loudness_in_sone, loudspeaker.frequency_response
        )
        for perceived_loudness_in_sone in LOUDNESS_LEVELS
    )
    for loudspeaker in LOUDSPEAKERS.values()
}

LOUDNESS_CONVERTER_WITHOUT_FREQUENCY_RESPONSE = {
    loudspeaker.name: tuple(
        converters.symmetrical.LoudnessToAmplitudeConverter(perceived_loudness_in_sone)
        for perceived_loudness_in_sone in LOUDNESS_LEVELS
    )
    for loudspeaker in LOUDSPEAKERS.values()
}
