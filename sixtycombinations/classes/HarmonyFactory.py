import functools
import itertools
import operator

from mutwo import parameters


class HarmonyFactory(object):
    def __init__(
        self, harmonic_primes: tuple = (3, 5, 7, 11, 13), tonality: bool = False,
    ) -> None:

        assert len(harmonic_primes) == 5

        self.harmonic_primes = harmonic_primes
        self.tonality = tonality

        self.pitches_per_voice_per_bar, self.missing_primes_per_bar = self.make_pitches(
            self.harmonic_primes, self.tonality
        )
        self.harmonic_primes_per_bar = self.make_harmonic_primes_per_bar(
            self.missing_primes_per_bar
        )

    def make_harmonic_primes_per_bar(self, missing_primes_per_bar: tuple) -> tuple:
        hp_per_bar = []

        for missing_primes in missing_primes_per_bar:
            primes = tuple(p for p in self.harmonic_primes if p not in missing_primes)
            primes += tuple(reversed(missing_primes))
            hp_per_bar.append(primes)

        return tuple(hp_per_bar)

    def make_pitches(self, harmonic_primes: tuple, tonality: bool) -> tuple:
        def make_primary_pitches(missing_prime: int) -> tuple:
            available_primes = tuple(p for p in harmonic_primes if p != missing_prime)
            pitches = [
                parameters.pitches.JustIntonationPitch(
                    "{}/{}".format(
                        functools.reduce(operator.mul, available_primes), missing_prime
                    )
                )
            ]
            for n in (3, 4):
                for combination in itertools.combinations(available_primes, n):
                    pitches.append(
                        parameters.pitches.JustIntonationPitch(
                            "{}/{}".format(
                                functools.reduce(operator.mul, combination), 1
                            )
                        )
                    )
            return tuple(pitches)

        def make_secondary_pitches(missing_prime0: int, missing_prime1: int) -> tuple:
            available_primes = tuple(
                p for p in harmonic_primes if p not in (missing_prime0, missing_prime1)
            )
            pitches = [
                parameters.pitches.JustIntonationPitch(
                    "{}/{}".format(
                        functools.reduce(operator.mul, available_primes), missing_prime1
                    )
                )
            ]
            for n in (2, 3):
                for combination in itertools.combinations(available_primes, n):
                    pitches.append(
                        parameters.pitches.JustIntonationPitch(
                            "{}/{}".format(
                                functools.reduce(operator.mul, combination), 1
                            )
                        )
                    )
            return tuple(pitches)

        def make_tertiary_pitches(missing_primes0: tuple, missing_prime1) -> tuple:
            available_primes = tuple(
                p
                for p in harmonic_primes
                if p not in missing_primes0 + (missing_prime1,)
            )
            pitches = [
                parameters.pitches.JustIntonationPitch(
                    "{}/{}".format(
                        functools.reduce(operator.mul, available_primes), missing_prime1
                    )
                )
            ]
            for n in (1, 2):
                for combination in itertools.combinations(available_primes, n):
                    pitches.append(
                        parameters.pitches.JustIntonationPitch(
                            "{}/{}".format(
                                functools.reduce(operator.mul, combination), 1
                            )
                        )
                    )
            return tuple(pitches)

        symmetric_structure = self.make_symmetric_structure(harmonic_primes)

        primary_pitches = {p: make_primary_pitches(p) for p in harmonic_primes}
        primary_pitches_transposition_model = (
            parameters.pitches.JustIntonationPitch("1/1"),
        ) + tuple(
            parameters.pitches.JustIntonationPitch("{}/{}".format(1, prime))
            for prime in harmonic_primes
        )
        for prime in harmonic_primes:
            primary_pitches[prime] = self.sort_transposition(
                primary_pitches_transposition_model, primary_pitches[prime]
            )[1]

        secondary_pitches = {
            per: make_secondary_pitches(*per)
            for per in functools.reduce(
                operator.add,
                tuple(
                    tuple(itertools.permutations(com))
                    for com in itertools.combinations(harmonic_primes, 2)
                ),
            )
        }
        for prime in harmonic_primes:
            secondary_pitches_transposition_model = (
                parameters.pitches.JustIntonationPitch("1/1"),
            ) + tuple(
                parameters.pitches.JustIntonationPitch("{}/{}".format(1, p))
                for p in harmonic_primes
                if p != prime
            )
            for prime1 in harmonic_primes:
                if prime1 != prime:
                    key = (prime, prime1)
                    secondary_pitches[key] = self.sort_transposition(
                        secondary_pitches_transposition_model, secondary_pitches[key]
                    )[1]

        tertiary_pitches = {}
        for combination in itertools.combinations(harmonic_primes, 2):
            for prime in harmonic_primes:
                if prime not in combination:
                    key = tuple(sorted(combination)) + (prime,)
                    tertiary_pitches.update(
                        {key: make_tertiary_pitches(key[:2], key[2])}
                    )
        for combination in itertools.combinations(harmonic_primes, 2):
            tertiary_pitches_transposition_model = (
                parameters.pitches.JustIntonationPitch("1/1"),
            ) + tuple(
                parameters.pitches.JustIntonationPitch("1/{}".format(p))
                for p in harmonic_primes
                if p not in combination
            )
            for prime in harmonic_primes:
                if prime not in combination:
                    key = tuple(sorted(combination)) + (prime,)
                    tertiary_pitches[key] = self.sort_transposition(
                        tertiary_pitches_transposition_model, tertiary_pitches[key]
                    )[1]

        if not tonality:
            for collection in (primary_pitches, secondary_pitches, tertiary_pitches):
                for key in collection:
                    tuple(p.inverse() for p in collection[key])

        pitches_per_voice_per_part = []
        for bar in symmetric_structure:
            pitches_per_voice_per_part.append(
                (
                    primary_pitches[bar[0]],
                    secondary_pitches[bar[:2]],
                    tertiary_pitches[tuple(sorted(bar[:2])) + (bar[2],)],
                )
            )
        return tuple(pitches_per_voice_per_part), symmetric_structure

    @staticmethod
    def fix_inner_positions_of_symmetrical_sets(sets: tuple) -> tuple:
        available_elements = set.union(*sets)
        element_counter = {element: 0 for element in available_elements}
        last_elements = []
        n_sets = len(sets)
        for counter, s0, s1 in zip(range(n_sets), sets, sets[1:] + (sets[0],)):
            possible_elements = s0.intersection(s1)
            if last_elements:
                prohibited_items = [last_elements[-1]]
                if counter + 1 == n_sets:
                    prohibited_items.append(last_elements[0])

                possible_elements = tuple(
                    item for item in possible_elements if item not in prohibited_items
                )

            choosen_element = sorted(
                possible_elements, key=lambda x: element_counter[x]
            )[0]
            element_counter[choosen_element] += 1
            last_elements.append(choosen_element)

        fixed_sets = []
        for s, first_element, last_element in zip(
            sets, [last_elements[-1]] + last_elements, last_elements
        ):
            in_between = tuple(
                element for element in s if element not in (first_element, last_element)
            )
            fixed_sets.append((first_element,) + in_between + (last_element,))

        return tuple(fixed_sets)

    @staticmethod
    def fix_inner_positions_of_nested_structures(structures: tuple) -> tuple:
        structure1 = HarmonyFactory.fix_inner_positions_of_symmetrical_sets(
            tuple(set(group) for group in structures[1])
        )
        new_order_of_structure1 = tuple(
            tuple(old_group.index(item) for item in group)
            for old_group, group in zip(structures[1], structure1)
        )
        structure2 = tuple(
            tuple(groups[idx] for idx in indices_per_group)
            for groups, indices_per_group in zip(structures[2], new_order_of_structure1)
        )
        structure2 = tuple(
            set(item) for item in functools.reduce(operator.add, structure2)
        )
        structure2 = HarmonyFactory.fix_inner_positions_of_symmetrical_sets(structure2)
        return structures[0], structure1, structure2

    @staticmethod
    def combine_structures_to_progressing_list(structures: tuple) -> tuple:
        complete_length = len(structures[-1])
        progressing_list = [[] for i in structures[-1]]
        for structure in structures:
            length = len(structure)
            ratio = complete_length // length
            for item, valid_range in zip(
                structure,
                tuple(
                    zip(
                        range(0, complete_length, ratio),
                        range(ratio, complete_length + ratio, ratio),
                    )
                ),
            ):
                for n in range(*valid_range):
                    progressing_list[n].append(item)
        return tuple(tuple(bar) for bar in progressing_list)

    @staticmethod
    def make_symmetric_structure(elements: tuple) -> tuple:
        assert len(elements) == 5
        structure0 = tuple(elements)
        structure1 = tuple(
            tuple(element for element in elements if element not in (el0,))
            for el0 in structure0
        )
        structure2 = tuple(
            tuple(
                tuple(element for element in elements if element not in (el0, el1))
                for el1 in group1
            )
            for el0, group1 in zip(structure0, structure1)
        )
        fixed_positions = HarmonyFactory.fix_inner_positions_of_nested_structures(
            (structure0, structure1, structure2)
        )
        fixed_positions = tuple(
            functools.reduce(operator.add, structure) if idx > 0 else structure
            for idx, structure in enumerate(fixed_positions)
        )
        return HarmonyFactory.combine_structures_to_progressing_list(fixed_positions)

    @staticmethod
    def sort_transposition(original: tuple, *transposition: tuple) -> tuple:
        # TODO(add a description)
        """This method."""
        matrix = tuple(tuple(b - a for b in original) for a in original)
        sets = tuple(tuple(sorted(m)) for m in matrix)
        r = []
        for group in transposition:
            intervals0 = tuple(p - group[0] for p in group)
            try:
                idx = sets.index(tuple(sorted(intervals0)))
            except ValueError:
                msg = "Group {0} isn't a transposition of {1}.".format(group, original)
                raise ValueError(msg)

            compare = matrix[idx]
            new_group = [None for i in original]
            for idxi, interval in enumerate(intervals0):
                new_group[compare.index(interval)] = group[idxi]

            r.append(tuple(new_group))

        return (tuple(original),) + tuple(r)
