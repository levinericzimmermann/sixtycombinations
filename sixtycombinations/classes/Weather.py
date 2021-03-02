import numbers
import operator
import typing

import expenvelope
import yamm

from sixtycombinations.classes import DynamicChoice
from sixtycombinations.classes import State
from sixtycombinations.classes import Tendency


class Weather(object):
    def __init__(
        self,
        start_state: State,
        states: typing.Iterable[State],
        markov_chain: yamm.Chain,
        duration: numbers.Number,
        seed: int = 100,
    ):
        import random

        random.seed(seed)
        self.random = random

        self._states = states
        self._state_weight_envelopes = Weather._make_weight_envelope_per_state(
            start_state, states, markov_chain, duration
        )

    # ######################################### #
    #       distribute weights of states        #
    #       over complete duration              #
    # ######################################### #

    @staticmethod
    def _append_points(
        states: typing.Iterable[State],
        state_names: typing.Tuple[str],
        points_per_state: typing.List[typing.List],
        state_name: str,
        *points
    ) -> typing.List[typing.List]:
        nth_state = state_names.index(state_name)
        state = states[nth_state]

        for point, value, curve_shape in zip(
            points,
            (0, 1, 1, 0),
            (state.attack_curve_shape, 0, state.release_curve_shape, 0),
        ):
            points_per_state[nth_state].append((point, value, curve_shape))

        return points_per_state

    @staticmethod
    def _postprocess_collected_points_per_state(
        points_per_state: typing.List[typing.List], duration: numbers.Number,
    ) -> typing.Tuple[typing.Tuple]:
        postprocessed_points_per_state = []
        for points in points_per_state:
            sorted_points = sorted(points, key=operator.itemgetter(0))
            last_point = (duration, points[0][1], 0)
            if last_point not in sorted_points:
                sorted_points.append(last_point)
            sorted_points = tuple(
                (absolute_duration / duration, value, curve_shape)
                for absolute_duration, value, curve_shape in sorted_points
            )
            postprocessed_points_per_state.append(tuple(sorted_points))

        return tuple(postprocessed_points_per_state)

    @staticmethod
    def _convert_distributed_states_to_envelopes(
        states: typing.Iterable[State],
        distributed_states_data: typing.Tuple[typing.Tuple[float]],
        duration: numbers.Number,
    ) -> typing.Tuple[expenvelope.Envelope]:
        state_names = tuple(state.name for state in states)
        points_per_state = [[] for _ in states]
        is_first = True
        for state_data in distributed_states_data:
            state_name, attack, sustain, release = state_data

            if is_first:
                for state_index, state in enumerate(states):
                    if state.name != state_name:
                        points_per_state[state_index].append((0, 0, 0))

                is_first = False

            points_per_state = Weather._append_points(
                states,
                state_names,
                points_per_state,
                state_name,
                attack,
                sustain[0],
                sustain[1],
                release,
            )

        postprocessed_points_per_state = Weather._postprocess_collected_points_per_state(
            points_per_state, duration
        )

        envelope_per_state = tuple(
            expenvelope.Envelope.from_points(*points)
            for points in postprocessed_points_per_state
        )

        return envelope_per_state

    @staticmethod
    def _distribute_states_on_duration(
        start_state: State,
        states: typing.Iterable[State],
        markov_chain: yamm.Chain,
        duration: numbers.Number,
    ) -> typing.Tuple[typing.Tuple[float]]:
        generator = markov_chain.walk_deterministic((start_state,))

        state_names = tuple(state.name for state in states)

        summed_duration = 0
        last_state = None

        active_states = []
        while summed_duration < duration:
            current_state = states[state_names.index(next(generator))]
            sustain = current_state.duration_maker()
            if last_state is None:
                attack = None
            else:
                attack = (
                    last_state.transition_duration_maker()
                    + current_state.transition_duration_maker()
                ) * 0.5

            sustain_start = summed_duration + attack if attack else summed_duration
            sustain = (sustain_start, sustain_start + sustain)
            attack = summed_duration if attack else None

            new_summed_duration = sustain[-1]
            if new_summed_duration > duration:
                active_states[0][1] = summed_duration
                active_states[-1][3] = duration
                break

            if last_state is not None:
                active_states[-1][3] = sustain_start
            active_states.append([current_state.name, attack, sustain, None])
            summed_duration = new_summed_duration
            last_state = current_state

        return tuple(tuple(state) for state in active_states)

    @staticmethod
    def _make_weight_envelope_per_state(
        start_state: State,
        states: typing.Iterable[State],
        markov_chain: yamm.Chain,
        duration: numbers.Number,
    ) -> typing.Tuple[expenvelope.Envelope]:
        distributed_states_data = Weather._distribute_states_on_duration(
            start_state, states, markov_chain, duration
        )
        return Weather._convert_distributed_states_to_envelopes(
            states, distributed_states_data, duration
        )

    # ######################################### #
    #           interpolation methods           #
    # ######################################### #

    def _interpolate_dynamic_choices(
        self,
        absolute_time: numbers.Number,
        dynamic_choices_and_weights: typing.Tuple[typing.Tuple[DynamicChoice, float]],
    ):
        dynamic_choices, weights = (
            map(lambda n: n[i], dynamic_choices_and_weights) for i in range(2)
        )
        summed_weights = sum(weights)
        collected_items = []
        collected_weights = []
        for dynamic_choice, weight in dynamic_choices_and_weights:
            for item, item_weight_envelope in dynamic_choice.items():
                if item not in collected_items:
                    collected_items.append(item)
                    collected_weights.append(0)

                value = item_weight_envelope.value_at(absolute_time) * (
                    weight / summed_weights
                )
                collected_weights[collected_items.index(item)] += value

        return self.random.choices(collected_items, collected_weights, k=1)[0]

    @staticmethod
    def _get_range_of_tendencies(
        absolute_time: numbers.Number,
        tendencies_and_weights: typing.Tuple[typing.Tuple[Tendency, float]],
    ) -> typing.Tuple[float]:
        value0, value1 = (
            Weather._interpolate_envelopes(
                absolute_time,
                tuple(
                    (getattr(tendency, attr), weight)
                    for tendency, weight in tendencies_and_weights
                ),
            )
            for attr in ("minima_curve", "maxima_curve")
        )
        return value0, value1

    def _interpolate_tendencies(
        self,
        absolute_time: numbers.Number,
        tendencies_and_weights: typing.Tuple[typing.Tuple[Tendency, float]],
    ):
        value0, value1 = Weather._get_range_of_tendencies(
            absolute_time, tendencies_and_weights
        )
        return self.random.uniform(value0, value1)

    @staticmethod
    def _interpolate_envelopes(
        absolute_time: numbers.Number,
        envelopes_and_weights: typing.Tuple[typing.Tuple[Tendency, float]],
    ):
        envelopes, weights = (
            map(lambda n: n[i], envelopes_and_weights) for i in range(2)
        )
        summed_weights = sum(weights)
        value = sum(
            envelope.value_at(absolute_time) * (weight / summed_weights)
            for envelope, weight in envelopes_and_weights
        )
        return value

    # ######################################### #
    #               public api                  #
    # ######################################### #

    def get_value_of_at(
        self, attribute_name: str, absolute_time: numbers.Number,
    ) -> typing.Any:
        attribute_weight_pairs = tuple(
            filter(
                lambda state_weight_pair: state_weight_pair[1] > 0,
                (
                    (
                        getattr(state, attribute_name),
                        weight_envelope.value_at(absolute_time),
                    )
                    for state, weight_envelope in zip(
                        self._states, self._state_weight_envelopes
                    )
                ),
            )
        )

        attribute_example = attribute_weight_pairs[0][0]

        if isinstance(attribute_example, DynamicChoice):
            value = self._interpolate_dynamic_choices(
                absolute_time, attribute_weight_pairs
            )

        elif isinstance(attribute_example, Tendency):
            value = self._interpolate_tendencies(absolute_time, attribute_weight_pairs)

        elif isinstance(attribute_example, expenvelope.Envelope):
            value = Weather._interpolate_envelopes(
                absolute_time, attribute_weight_pairs
            )

        else:
            raise NotImplementedError(type(attribute_example))

        return value

    def get_range_of_at(
        self, attribute_name: str, absolute_time: numbers.Number,
    ) -> typing.Any:
        attribute_weight_pairs = tuple(
            filter(
                lambda state_weight_pair: state_weight_pair[1] > 0,
                (
                    (
                        getattr(state, attribute_name),
                        weight_envelope.value_at(absolute_time),
                    )
                    for state, weight_envelope in zip(
                        self._states, self._state_weight_envelopes
                    )
                ),
            )
        )

        attribute_example = attribute_weight_pairs[0][0]

        if isinstance(attribute_example, Tendency):
            range_ = Weather._get_range_of_tendencies(
                absolute_time, attribute_weight_pairs
            )

        else:
            raise NotImplementedError(type(attribute_example))

        return range_

    # ######################################### #
    #               magic methods               #
    # ######################################### #

    def __repr__(self) -> str:
        return "Weather({})".format(self._states)
