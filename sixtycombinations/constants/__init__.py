# ######################################################### #
#                           path                            #
# ######################################################### #
from .BUILD_PATH import BUILD_PATH
from .LOUDSPEAKER_MONO_FILES_BUILD_PATH import LOUDSPEAKER_MONO_FILES_BUILD_PATH
from .LOUDSPEAKER_MONO_FILES_BUILD_PATH_RELATIVE import (
    LOUDSPEAKER_MONO_FILES_BUILD_PATH_RELATIVE,
)
from .LOUDSPEAKER_MONO_FILES_BUILD_PATH_ABSOLUTE import (
    LOUDSPEAKER_MONO_FILES_BUILD_PATH_ABSOLUTE,
)
from .MIX_PATH import MIX_PATH

# ######################################################### #
#           abstract constants                              #
# ######################################################### #
from .PRIMES import PRIMES
from .MINIMAL_DURATION_OF_ONE_BEAT import MINIMAL_DURATION_OF_ONE_BEAT
from .FREQUENCY_RANGE import FREQUENCY_RANGE
from .RANDOM_SEED import RANDOM_SEED
from .N_ITERATIONS_OF_HARMONIC_STRUCTURE import N_ITERATIONS_OF_HARMONIC_STRUCTURE
from .CUT_UP import CUT_UP

# ######################################################### #
#                      harmony definition                   #
# ######################################################### #
from .HARMONIES import HARMONIES
from .HARMONIES_IN_CORRECT_REGISTER import HARMONIES_IN_CORRECT_REGISTER
from .REAL_FREQUENCY_RANGE import REAL_FREQUENCY_RANGE

# ######################################################### #
#                loudspeaker & loudspeaker positions        #
# ######################################################### #
from .LOUDSPEAKERS import LOUDSPEAKERS
from .RING_POSITION_TO_LOUDSPEAKER import RING_POSITION_TO_LOUDSPEAKER
from .OUTPUT_CHANNEL_TO_SPEAKER import OUTPUT_CHANNEL_TO_SPEAKER
from .PITCH_TO_LOUDSPEAKER_MAPPING import PITCH_TO_LOUDSPEAKER_MAPPING

# ######################################################### #
#               initialising Loudness converters            #
# ######################################################### #
from .LOUDNESS_LEVEL_RANGE import LOUDNESS_LEVEL_RANGE
from .N_LOUDNESS_LEVELS import N_LOUDNESS_LEVELS
from .LOUDNESS_LEVELS import LOUDNESS_LEVELS
from .LOUDNESS_CONVERTER import LOUDNESS_CONVERTER

# ######################################################### #
# duration / time per harmony -> transition between harmonies #
# ######################################################### #
from .TRANSITION_PHASES_FACTOR import TRANSITION_PHASES_FACTOR
from .TRANSITION_PHASES_EXPONENT import TRANSITION_PHASES_EXPONENT
from .TRANSITION_PHASES import TRANSITION_PHASES
from .MIN_N_PHASES_FOR_SUSTAIN import MIN_N_PHASES_FOR_SUSTAIN
from .MAX_N_MIN_PHASES_FOR_SUSTAIN import MAX_N_MIN_PHASES_FOR_SUSTAIN
from .GROUPS import GROUPS
from .DURATION import DURATION
from .ABSOLUTE_START_TIME_PER_GROUP import ABSOLUTE_START_TIME_PER_GROUP

# ######################################################### #
#                    composed objects in time               #
# ######################################################### #
from .NESTED_PARTIALS import NESTED_PARTIALS

# ######################################################### #
#          different tendencies and curves:                 #
# ######################################################### #

# The following constants / tendencies keep mostly the same throughout the
# complete composition (only soft modulations for variety are applied, but
# generally a satisfying range has been found for the complete composition)
from .ATTACK_DURATION_TENDENCY import ATTACK_DURATION_TENDENCY
from .RELEASE_DURATION_TENDENCY import RELEASE_DURATION_TENDENCY
from .MINIMAL_PHASES_PER_SOUND_TENDENCY import MINIMAL_PHASES_PER_SOUND_TENDENCY
from .GLISSANDO_START_PITCH_CURVE import GLISSANDO_START_PITCH_CURVE
from .GLISSANDO_END_PITCH_CURVE import GLISSANDO_END_PITCH_CURVE
from .GLISSANDO_START_DURATION_TENDENCY import GLISSANDO_START_DURATION_TENDENCY
from .GLISSANDO_END_DURATION_TENDENCY import GLISSANDO_END_DURATION_TENDENCY

# ###############################################################################
# TENDENCIES FOR A HIGH LEVEL STATE
# Here I can differentiate between a more full or rich sound versus a more
# nuanced, differentiated, quiet sound.
# For building the rich sound:
#   - low spectrality
#   - narrow and high density and loudness tendency
# For building the nuanced sound:
#   - high spectrality
#   - wide density and loudness tendency
#
# The most interesting results happen when the sound is generally nuanced,
# but the spectrality is constantly moving, so that the listener can experience
# both: the richness of all available frequencies and the actual harmonic
# situation of three main pitches (with their more quiet overtones).
#
# I can think of 3 different situations:
#   (1) short & sudden rich "sonic explosions"
#   (2) longer periods with a moving spectrality and wide ranges of tendencies
#       (most interesting listening experience, tendencies may vary in a
#        controlled range)
#   (3) a damped, quiet, low-frequency-emphasising, dark sound situation with a
#       constant, rather high, spectrality
from .SPECTRALITY import SPECTRALITY
from .LOUDNESS_TENDENCY import LOUDNESS_TENDENCY
from .DENSITY_TENDENCY import DENSITY_TENDENCY

# There are two effects for the filter that I wanna use:
#   (1) damping higher frequencies (making longer parts with an emphasis
#       on bass)
#   (2) short filter sweeps where only high frequencies are dominant
from .FILTER_FREQUENCY import FILTER_FREQUENCY
from .FILTER_Q import FILTER_Q

from .SYNTHESIZER_CURVE import SYNTHESIZER_CURVE
from .BANDWIDTH import BANDWIDTH
# ###############################################################################
