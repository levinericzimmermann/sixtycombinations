import functools
import operator

from sixtycombinations.constants import HARMONIES

# set how many phases of the fundamental sine wave are repeated
# per harmony. The calculation makes sure that more simple
# sounds ring longer while more complex sounds (with lower missing
# prime numbers) sound shorter.
N_PHASES_OF_FUNDAMENTAL_PER_HARMONY = tuple(
    functools.reduce(operator.mul, primes)
    for primes in HARMONIES.missing_primes_per_bar
)
