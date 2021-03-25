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
from .MIDI_FILES_BUILD_PATH import MIDI_FILES_BUILD_PATH
from .ISIS_FILES_BUILD_PATH import ISIS_FILES_BUILD_PATH
from .FILTERED_ISIS_FILES_BUILD_PATH import FILTERED_ISIS_FILES_BUILD_PATH
from .MIX_PATH import MIX_PATH

# ######################################################### #
#           abstract constants                              #
# ######################################################### #
from .PRIMES import PRIMES
from .MINIMAL_DURATION_OF_ONE_BEAT import MINIMAL_DURATION_OF_ONE_BEAT
from .FREQUENCY_RANGE import FREQUENCY_RANGE
from .RANDOM_SEED import RANDOM_SEED
from .N_ITERATIONS_OF_HARMONIC_STRUCTURE import N_ITERATIONS_OF_HARMONIC_STRUCTURE
from .N_ITERATIONS_OF_ISIS_PHRASES import N_ITERATIONS_OF_ISIS_PHRASES
from .CUT_UP import CUT_UP
from .SINGING import SINGING_PHRASES
from .DISTRIBUTED_SINGING_PHRASES import DISTRIBUTED_SINGING_PHRASES
from .SINGER_PER_CYCLE import SINGER_PER_CYCLE

# ######################################################### #
#                      harmony definition                   #
# ######################################################### #
from .HARMONIES import HARMONIES
from .HARMONIES_IN_CORRECT_REGISTER import HARMONIES_IN_CORRECT_REGISTER
from .REAL_FREQUENCY_RANGE import REAL_FREQUENCY_RANGE
from .AVAILABLE_PITCHES import AVAILABLE_PITCHES
from .AVAILABLE_PITCHES_WITH_FUNDAMENTAL_FUNCTION import (
    AVAILABLE_PITCHES_WITH_FUNDAMENTAL_FUNCTION,
)

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
from .LOUDNESS_CONVERTER import (
    LOUDNESS_CONVERTER_WITH_FREQUENCY_RESPONSE,
    LOUDNESS_CONVERTER_WITHOUT_FREQUENCY_RESPONSE,
)

# ######################################################### #
# duration / time per harmony -> transition between harmonies #
# ######################################################### #
from .TRANSITION_PHASES_FACTOR import TRANSITION_PHASES_FACTOR
from .TRANSITION_PHASES_EXPONENT import TRANSITION_PHASES_EXPONENT
from .TRANSITION_PHASES import TRANSITION_PHASES
from .MIN_N_PHASES_FOR_SUSTAIN import MIN_N_PHASES_FOR_SUSTAIN
from .MAX_N_MIN_PHASES_FOR_SUSTAIN import MAX_N_MIN_PHASES_FOR_SUSTAIN
from .GROUPS import Group, GROUPS
from .DURATION import DURATION
from .ABSOLUTE_START_TIME_PER_GROUP import ABSOLUTE_START_TIME_PER_GROUP

# ######################################################### #
#                    composed objects in time               #
# ######################################################### #
from .NESTED_PARTIALS import NESTED_PARTIALS

# ######################################################### #
#                        isis stuff                         #
# ######################################################### #
from .ISIS_PITCH_GENERATOR_PER_CYCLE import ISIS_PITCH_GENERATOR_PER_CYCLE
from .ISIS_RHYTHMICAL_GRID_PER_CYCLE import ISIS_RHYTHMICAL_GRID_PER_CYCLE

# ######################################################### #
#          different tendencies and curves:                 #
# ######################################################### #
from .WEATHER import WEATHER
