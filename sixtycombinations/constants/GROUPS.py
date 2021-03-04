"""This file implements the class Group and furthermore define all relevant Groups.

One Group is a set of pitches with just relationships.
"""

import copy
import functools
import itertools
import operator
import typing

from ortools.linear_solver import pywraplp
import quicktions as fractions

from mu.rhy import indispensability

from mutwo.events import basic
from mutwo.parameters import pitches
from mutwo.utilities import prime_factors

from sixtycombinations.constants import HARMONIES_IN_CORRECT_REGISTER
from sixtycombinations.constants import MAX_N_MIN_PHASES_FOR_SUSTAIN
from sixtycombinations.constants import MIN_N_PHASES_FOR_SUSTAIN
from sixtycombinations.constants import TRANSITION_PHASES

from sixtycombinations.constants import MINIMAL_DURATION_OF_ONE_BEAT

from sixtycombinations.constants import N_ITERATIONS_OF_HARMONIC_STRUCTURE


class Group(object):
    def __init__(
        self,
        cycle_index: int,
        harmony_index: int,
        harmony: typing.Tuple[pitches.JustIntonationPitch],
        attack: int,
        release: int,
        sustain: int = None,
        relative_start_time: float = None,
    ):
        self.cycle_index = cycle_index
        self.harmony_index = harmony_index
        self.fundamental = harmony[0]
        self.harmony = harmony
        self.attack = int(attack)
        self.release = int(release)
        self.sustain = sustain
        self.relative_start_time = relative_start_time

    # ################################################### #
    #                    magic methods                    #
    # ################################################### #

    def __repr__(self) -> str:
        return "Group({}, {})".format(self.cycle_index, self.harmony_index)

    # ################################################### #
    #                    static methods                   #
    # ################################################### #

    @staticmethod
    def find_common_pitch_between_two_harmonies_and_its_ratio_to_the_particular_harmony(
        pitches0: typing.Tuple[pitches.JustIntonationPitch],
        pitches1: typing.Tuple[pitches.JustIntonationPitch],
    ) -> tuple:
        common_pitch = None
        for pitch0 in pitches0:
            for pitch1 in pitches1:
                if pitch0.exponents[1:] == pitch1.exponents[1:]:
                    common_pitch = (pitch0, pitch1)
                    break

        prime0, prime1 = (
            int((pitch - pitches[0]).ratio)
            for pitch, pitches in zip(common_pitch, (pitches0, pitches1))
        )
        return common_pitch, prime0, prime1

    @staticmethod
    def _get_variable_name(nth_cycle: int, nth_index: int) -> str:
        return "sustain_factor_{}_{}".format(nth_cycle, nth_index)

    @staticmethod
    def _calculate_duration_of_n_phases(
        group: "Group", n_phases: int
    ) -> fractions.Fraction:
        return (
            fractions.Fraction(1, group.get_relationship_to_deepest_fundamental())
            * n_phases
        )

    @staticmethod
    def _sum_active_transitions_of_group(
        group: "Group", higher_groups: typing.Tuple["Group"]
    ) -> int:
        return sum(
            (
                (
                    (Group._calculate_duration_of_n_phases(group, n_transition_phases))
                    - overlapping_group_size
                )
                / 2
            )
            + overlapping_group_size
            for n_transition_phases, overlapping_group_size in zip(
                (group.attack, group.release),
                (
                    Group._calculate_duration_of_n_phases(higher_group, n_phases)
                    for higher_group, n_phases in zip(
                        (higher_groups[0], higher_groups[-1]),
                        (higher_groups[0].attack, higher_groups[-1].release),
                    )
                ),
            )
        )

    @staticmethod
    def _declare_constraint(
        solver: pywraplp.Solver,
        group: "Group",
        variables: typing.Tuple[typing.Tuple[pywraplp.Variable]],
    ) -> None:
        higher_groups = group.get_simultaneous_groups_of_higher_cycle()
        if higher_groups:
            # fixed duration of group
            summed_active_transitions_of_group = Group._sum_active_transitions_of_group(
                group, higher_groups
            )

            # fixed duration of higher groups
            summed_transitions_of_higher_groups = sum(
                Group._calculate_duration_of_n_phases(higher_group, higher_group.attack)
                for higher_group in higher_groups
            )
            summed_transitions_of_higher_groups += Group._calculate_duration_of_n_phases(
                higher_groups[-1], higher_groups[-1].release
            )
            difference_of_duration = (
                summed_active_transitions_of_group - summed_transitions_of_higher_groups
            )
            constraint = sum(
                Group._calculate_duration_of_n_phases(higher_group, var)
                for var, higher_group in zip(variables[1], higher_groups)
            )
            constraint = constraint - (
                Group._calculate_duration_of_n_phases(group, variables[0][0])
            )
            solver.Add(constraint == difference_of_duration)

    @staticmethod
    def _get_n_periods_of_fundamental_per_beat(
        fundamental: pitches.JustIntonationPitch,
        n_phases: int,
        partials: typing.Tuple[int],
        minimal_duration_of_one_beat: float,
    ) -> int:
        # heuristic check to make sure partials are sorted
        assert max(partials) == partials[-1]

        n_periods_of_fundamental_per_beat = 1
        duration_of_one_period_per_partial = tuple(
            1 / (fundamental.frequency * partial) for partial in partials
        )
        valid_solutions = [1]
        while (
            duration_of_one_period_per_partial[-1] * n_periods_of_fundamental_per_beat
            < minimal_duration_of_one_beat
        ):
            n_periods_of_fundamental_per_beat += 1
            while n_phases % n_periods_of_fundamental_per_beat != 0:
                n_periods_of_fundamental_per_beat += 1

                if n_periods_of_fundamental_per_beat > n_phases:
                    return valid_solutions[-1]

            valid_solutions.append(int(n_periods_of_fundamental_per_beat))

        return valid_solutions[-1]

    @staticmethod
    def _generate_rhythmical_data(
        fundamental: pitches.JustIntonationPitch,
        n_periods_of_fundamental_per_beat: int,
        n_repetitions_of_rhythm: int,
        partial: int,
    ) -> typing.Tuple[typing.Any]:
        """Generate rhythmical data for the respective partial.

        The rhythmical data contain the following information:
            1. How often the rhythm get repeated (int)
            2. How many periods one beat last (int)
            3. The respective rhythm with duration values in seconds
               (basic.SequentialEvent[basic.SimpleEvent])
            4. Indispensability of each beat (typing.Tuple[int])
        """

        duration_of_one_period = 1 / (fundamental.frequency * partial)
        duration_of_one_beat = (
            duration_of_one_period * n_periods_of_fundamental_per_beat
        )
        rhythm = basic.SequentialEvent(
            [basic.SimpleEvent(duration_of_one_beat) for _ in range(partial)]
        )
        if partial == 1:
            indispensability_for_bar = (0,)
        else:
            indispensability_for_bar = indispensability.indispensability_for_bar(
                (partial,)
            )

        return (
            n_repetitions_of_rhythm,
            n_periods_of_fundamental_per_beat,
            rhythm,
            indispensability_for_bar,
        )

    @staticmethod
    def _get_rhythmical_data_per_partial(
        fundamental: pitches.JustIntonationPitch,
        n_phases: int,
        partials: typing.Tuple[int],
        minimal_duration_of_one_beat: float,
    ) -> typing.Tuple[typing.Tuple[typing.Any]]:
        n_periods_of_fundamental_per_beat = Group._get_n_periods_of_fundamental_per_beat(
            fundamental, n_phases, partials, minimal_duration_of_one_beat
        )
        n_repetitions_of_rhythm = n_phases // n_periods_of_fundamental_per_beat
        rhythmical_data_per_partial = tuple(
            Group._generate_rhythmical_data(
                fundamental,
                n_periods_of_fundamental_per_beat,
                n_repetitions_of_rhythm,
                partial,
            )
            for partial in partials
        )
        return rhythmical_data_per_partial

    @staticmethod
    def _round_sustain(n_phases: float) -> int:
        """Round sustain phases.

        Makes sure that the resulting number can be decomposed
        in more than 4 prime numbers.
        """
        n_phases = int(n_phases)

        for n in range(5):
            if len(prime_factors.factorise(n_phases)) < 5:
                n_phases -= 1

        return n_phases

    # ################################################### #
    #                    getter methods                   #
    # ################################################### #

    def get_simultaneous_groups_of_higher_cycle(
        self,
    ) -> typing.Union[typing.Tuple["Group"], None]:
        if self.cycle_index < 2:
            ratio_to_higher_cycle = len(GROUPS[self.cycle_index + 1]) // len(
                GROUPS[self.cycle_index]
            )
            simultaneous_groups_in_higher_cycle_index0 = (
                self.harmony_index * ratio_to_higher_cycle
            )
            simultaneous_groups_in_higher_cycle_index1 = (
                simultaneous_groups_in_higher_cycle_index0 + ratio_to_higher_cycle
            )
            return GROUPS[self.cycle_index + 1][
                simultaneous_groups_in_higher_cycle_index0:simultaneous_groups_in_higher_cycle_index1
            ]
        else:
            return None

    def get_previous_group(self) -> "Group":
        return GROUPS[self.cycle_index][self.harmony_index - 1]

    def get_next_group(self) -> "Group":
        return GROUPS[self.cycle_index][
            (self.harmony_index + 1) % len(GROUPS[self.cycle_index])
        ]

    def get_relationship_to_deepest_fundamental(self) -> int:
        if self.cycle_index == 0:
            return 1
        else:
            ratio_to_lowest_cycle = len(GROUPS[self.cycle_index]) // len(GROUPS[0])
            responsible_group = GROUPS[0][self.harmony_index // ratio_to_lowest_cycle]
            ratio_to_deepest_fundamental = pitches.JustIntonationPitch(
                (self.fundamental - responsible_group.fundamental).exponents
            ).ratio
            return ratio_to_deepest_fundamental

    # ################################################### #
    #                     properties                      #
    # ################################################### #

    @property
    def duration(self) -> float:
        return (self.attack + self.sustain + self.release) * (
            1 / self.fundamental.frequency
        )

    @property
    def common_pitch_data_with_previous_harmony(self) -> pitches.JustIntonationPitch:
        previous_harmony = self.get_previous_group().harmony
        return self.find_common_pitch_between_two_harmonies_and_its_ratio_to_the_particular_harmony(
            previous_harmony, self.harmony
        )

    @property
    def common_pitch_data_with_next_harmony(self) -> pitches.JustIntonationPitch:
        next_harmony = self.get_next_group().harmony
        return self.find_common_pitch_between_two_harmonies_and_its_ratio_to_the_particular_harmony(
            next_harmony, self.harmony
        )

    # ################################################### #
    #                     private methods                 #
    #       (mostly for solving constraint problem)       #
    # ################################################### #

    def _declare_variable(
        self, solver: pywraplp.Solver, nth_cycle: int, nth_index: int
    ) -> None:
        return solver.NumVar(
            MIN_N_PHASES_FOR_SUSTAIN,
            MIN_N_PHASES_FOR_SUSTAIN * MAX_N_MIN_PHASES_FOR_SUSTAIN,
            self._get_variable_name(nth_cycle, nth_index),
        )

    def _declare_variables(
        self, solver: pywraplp.Solver
    ) -> typing.Tuple[typing.Tuple[pywraplp.Variable]]:
        # Declare variables. Set a number for each sustain factor
        # of simultaneous groups.
        variables = [[], [], []]
        for nth_central_group, simultaneous_central_group in enumerate(
            self.get_simultaneous_groups_of_higher_cycle()
        ):
            inner_variables = []
            inner_groups = (
                simultaneous_central_group.get_simultaneous_groups_of_higher_cycle()
            )
            for nth_inner_group, simultaneous_inner_group in enumerate(inner_groups):
                inner_variables.append(
                    self._declare_variable(
                        solver,
                        2,
                        nth_inner_group + (nth_central_group * len(inner_groups)),
                    )
                )

            variables[2].append(tuple(inner_variables))
            variables[1].append(self._declare_variable(solver, 1, nth_central_group))

        variables[0].append(self._declare_variable(solver, 0, 0))
        return tuple(tuple(v) for v in variables)

    def _declare_constraints(
        self,
        solver: pywraplp.Solver,
        variables: typing.Tuple[typing.Tuple[pywraplp.Variable]],
    ) -> None:
        groups = [[self, variables[:2]]]
        for nth_higher_group, higher_groups in enumerate(
            self.get_simultaneous_groups_of_higher_cycle()
        ):
            responsible_variables = (
                [variables[1][nth_higher_group]],
                variables[2][nth_higher_group],
            )
            groups.append((higher_groups, responsible_variables))
        [
            self._declare_constraint(solver, group, responsible_variables)
            for group, responsible_variables in groups
        ]

    # ################################################### #
    #          methods for assigning attributes           #
    # ################################################### #

    def _assign_rhythmical_data(self) -> None:
        partials = tuple(
            (pitch - self.fundamental).ratio.numerator for pitch in self.harmony
        )
        minimal_duration_of_one_beat = MINIMAL_DURATION_OF_ONE_BEAT
        self.rhythmical_data_per_state = tuple(
            self._get_rhythmical_data_per_partial(
                self.fundamental,
                n_periods_in_state,
                partials,
                minimal_duration_of_one_beat,
            )
            for n_periods_in_state in (
                self.attack,
                Group._round_sustain(self.sustain),
                self.release,
            )
        )

        # print duration of one bar etc.
        print("Group:", self.cycle_index)
        for rhythmical_data in self.rhythmical_data_per_state:
            print(
                rhythmical_data[0][1],
                rhythmical_data[0][2].duration * rhythmical_data[0][0],
                rhythmical_data[-1][2][0].duration,
            )
        print("")

    def _assign_sustain_for_itself_and_higher_groups(self) -> None:
        # only valid for lowest cycle
        assert self.cycle_index == 0

        # definition of the problem
        solver = pywraplp.Solver.CreateSolver("GLOP")
        variables = self._declare_variables(solver)
        self._declare_constraints(solver, variables)

        # solving the problem and assigning the results
        status = solver.Solve()
        if status == pywraplp.Solver.OPTIMAL:
            higher_groups = self.get_simultaneous_groups_of_higher_cycle()
            highest_groups = functools.reduce(
                operator.add,
                (
                    higher_group.get_simultaneous_groups_of_higher_cycle()
                    for higher_group in higher_groups
                ),
            )
            for variable, group in zip(
                (
                    variables[0]
                    + variables[1]
                    + functools.reduce(operator.add, variables[2])
                ),
                (self,) + higher_groups + highest_groups,
            ):
                n_phases = variable.solution_value()
                group.sustain = n_phases
                # print("{} = {}".format(variable.name(), n_phases))

        else:
            msg = (
                "Couldn't find any valid solution. Try to increase the value of"
                " MAX_N_MIN_PHASES_FOR_SUSTAIN."
            )
            raise ValueError(msg)


# basic initialisation of group
GROUPS = tuple(
    tuple(
        Group(cycle_index, harmony_index, harmony, transitions[0], transitions[1])
        for harmony_index, harmony, transitions in zip(
            range(len(harmonies)), harmonies, transitions_per_group
        )
    )
    for cycle_index, harmonies, transitions_per_group in zip(
        range(3), HARMONIES_IN_CORRECT_REGISTER, TRANSITION_PHASES
    )
)


# figure out sustain value of Groups via constraint programming
[group._assign_sustain_for_itself_and_higher_groups() for group in GROUPS[0]]


# find rhythmical data per group
[[group._assign_rhythmical_data() for group in groups] for groups in GROUPS]


# multiply groups according to N_ITERATIONS_OF_HARMONIC_STRUCTURE variable
GROUPS = tuple(
    functools.reduce(
        operator.add,
        (copy.deepcopy(group) for _ in range(N_ITERATIONS_OF_HARMONIC_STRUCTURE)),
    )
    for group in GROUPS
)


# declare relative start time of each harmony in each group in seconds
# (relative insofar as the numbers assume that each start time
# of each cycle is 0, while it actually differs, see ABSOLUTE_START_TIME_PER_GROUP)
for cycle in GROUPS:
    relative_start_time = 0
    for group in cycle:
        group.relative_start_time = relative_start_time
        relative_start_time += (group.attack + group.sustain) * (
            1 / group.fundamental.frequency
        )


# print average difference of duration between different groups

for nth_cycle, cycle in enumerate(GROUPS):
    for state in (0, 1, 2):
        duration_per_group = tuple(
            group.rhythmical_data_per_state[state][0][0]
            * group.rhythmical_data_per_state[state][0][2].duration
            for group in cycle
        )
        duration_difference_pairs = tuple(
            abs(a - b) for a, b in itertools.combinations(duration_per_group, 2)
        )
        avg_dur = sum(duration_per_group) / len(duration_per_group)
        avg_diff = sum(duration_difference_pairs) / len(duration_difference_pairs)
        print(
            "Group {}, state {} AVG dur: {}, AVG diff: {}".format(
                nth_cycle, state, avg_dur, avg_diff
            )
        )
    print("")
