import numbers
import typing


class State(object):
    def __init__(
        self,
        name: str,
        attributes: typing.Dict[str, typing.Any],
        duration_maker: typing.Callable[[], numbers.Number],
        transition_duration_maker: typing.Callable[[], numbers.Number],
        attack_curve_shape: float,
        release_curve_shape: float,
    ):
        self.name = name

        for attribute_name, attribute_content in attributes.items():
            setattr(self, attribute_name, attribute_content)

        self.attributes = attributes.keys()
        self.duration_maker = duration_maker
        self.transition_duration_maker = transition_duration_maker

        self.attack_curve_shape = attack_curve_shape
        self.release_curve_shape = release_curve_shape

    def __repr__(self) -> str:
        return "State({})".format(self.name)
