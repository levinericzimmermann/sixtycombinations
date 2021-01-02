from mutwo.parameters import pitches

from sixtycombinations.constants import HARMONIES
from sixtycombinations.constants import N_PHASES_OF_FUNDAMENTAL_PER_HARMONY

DURATION_PER_HARMONY = tuple(
    (
        1
        / (
            pitches_per_voice[0][0].normalize(mutate=False).ratio
            * pitches.constants.DEFAULT_CONCERT_PITCH
        )
    )
    * n_phases
    for pitches_per_voice, n_phases in zip(
        HARMONIES.pitches_per_voice_per_bar, N_PHASES_OF_FUNDAMENTAL_PER_HARMONY
    )
)
