"""This file defines the minimal duration of one static sound."""

import expenvelope

MINIMAL_DURATION_OF_ONE_SOUND = expenvelope.Envelope.from_points((0, 0.9), (1, 0.9),)
