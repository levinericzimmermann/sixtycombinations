import typing

import expenvelope


class Loudspeaker(object):
    """Loudspeaker model abstraction.

    Loudspeakers are only defined by their product name, their
        frequency response and their resonance frequency range.
    """

    def __init__(
        self,
        name: str,
        frequency_response: expenvelope.Envelope = expenvelope.Envelope.from_points(
            (0, 80), (20000, 80)
        ),
        resonance_frequency_range: typing.Tuple[float] = (270, 430),
    ):
        self.name = name
        self.frequency_response = frequency_response
        self.resonance_frequency_range = resonance_frequency_range
