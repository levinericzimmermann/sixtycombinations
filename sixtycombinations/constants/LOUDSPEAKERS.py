"""Definition of all loudspeakers that are used for the installation."""

import expenvelope

from sixtycombinations.classes import Loudspeaker

LOUDSPEAKERS = {
    loudspeaker.name: loudspeaker
    for loudspeaker in (
        # VISATON SPEAKER
        Loudspeaker(
            "WS25E",
            expenvelope.Envelope.from_points(
                (20, 71),
                (30, 78.5),
                (40, 80.75),
                (50, 80.1),
                (60, 80),
                (70, 80),
                (80, 79.8),
                (90, 80.25),
                (100, 80.95),
                (150, 81.95),
                (200, 81.95),
                (267, 81.98),
                (300, 83.75),
                (360, 85.95),
                (420, 85.95),
                (500, 85),
                (600, 84.3),
                (700, 83),
                (710, 82),
                (800, 86),
                (900, 85.85),
                (1000, 86),
                (1250, 87.5),
                (1500, 86.9),
                (1750, 85),
                (2000, 89),
                (2500, 94),
                (3000, 94),
                (3400, 90),
                (4000, 90),
                (5000, 88),
                (6000, 76.85),
                (7000, 70),
                (8000, 54),
                (9000, 64),
                (10000, 69),
                (13000, 54),
                (15000, 58),
                (17000, 59),
                (20000, 52),
            ),
        ),
        Loudspeaker(
            "FRS7S",
            expenvelope.Envelope.from_points(
                (20, 50),
                (30, 52),
                (50, 63),
                (100, 74),
                (150, 83.8),
                (170, 85.2),
                (200, 84),
                (300, 82),
                (325, 82),
                (350, 80),
                (375, 82),
                (400, 80.85),
                (500, 80.85),
                (700, 82),
                (800, 80),
                (900, 80),
                (1000, 81),
                (1250, 81.9),
                (1500, 80.2),
                (1750, 79),
                (2000, 80),
                (2550, 80),
                (2800, 84),
                (3000, 82),
                (3250, 84),
                (3500, 82),
                (3750, 84),
                (4000, 83),
                (5000, 80.89),
                (6000, 83.5),
                (8000, 82),
                (9000, 90),
                (10000, 90),
                (12200, 84),
                (15000, 84.2),
                (20000, 82.9),
            ),
        ),
        Loudspeaker(
            "K50FL",
            expenvelope.Envelope.from_points(
                (50, 50),
                (100, 64),
                (180, 76),
                (200, 75),
                (340, 87),
                (500, 81),
                (700, 80),
                (900, 77),
                (1000, 78),
                (1700, 77),
                (2000, 76),
                (4000, 76),
                (4200, 73.9),
                (5000, 80),
                (5600, 78),
                (6000, 88),
                (7000, 83),
                (8000, 82),
                (9000, 82.5),
                (10000, 83.3),
                (12900, 85.8),
                (13950, 83),
                (15000, 84.8),
                (17500, 80),
                (20000, 79),
            ),
        ),
        Loudspeaker(
            "K50FLS",
            expenvelope.Envelope.from_points(
                (49.999, 0),
                (50, 50),
                (100, 50),
                (200, 64),
                (300, 73),
                (400, 79.33),
                (500, 89),
                (600, 90),
                (700, 89),
                (800, 85.85),
                (900, 83),
                (950, 84),
                (1000, 83.5),
                (1250, 82.25),
                (1500, 82.9),
                (1740, 82.9),
                (1750, 81.9),
                (2000, 81.9),
                (2500, 83.5),
                (2620, 84.7),
                (2780, 84),
                (3000, 86),
                (3100, 86),
                (3500, 91),
                (3700, 88),
                (4000, 91),
                (4320, 84),
                (4500, 83.9),
                (5000, 83.8),
                (6000, 81),
                (6400, 80),
                (6900, 82),
                (7100, 80),
                (7500, 81.9),
                (8000, 79),
                (8200, 78.9),
                (9000, 81),
                (9400, 76.9),
                (10000, 76),
                (10850, 75),
                (11250, 76.5),
                (12500, 77),
                (13200, 78),
                (15000, 76),
                (16500, 76),
                (20000, 82.4),
            ),
        ),
        # KENFORD SPEAKER
        Loudspeaker(
            "HW806",
            expenvelope.Envelope.from_points(
                (10, 50),
                (15, 56.8),
                (20, 66),
                (25, 70.9),
                (30, 75),
                (40, 81.7),
                (45, 84),
                (50, 84.89),
                (55, 84.89),
                (60, 86),
                (70, 87.125),
                (75, 85),
                (80, 85),
                (85, 85),
                (90, 86),
                (100, 87.55),
                (125, 88.1),
                (140, 90),
                (150, 89.75),
                (190, 88.1),
                (200, 86.135),
                (225, 86),
                (250, 86.135),
                (260, 86),
                (300, 87),
                (400, 87.2),
                (450, 87.32),
                (500, 89.9),
                (600, 92),
                (700, 90.95),
                (800, 88.3),
                (900, 90),
                (950, 91),
                (1000, 90),
                (1500, 87.8),
                (1750, 86.2),
                (2000, 87),
                (3000, 92),
                (3250, 92.8),
                (3500, 92),
                (4000, 91),
                (5000, 88),
                (6000, 85.3),
                (7000, 86.9),
                (8000, 83.75),
                (10000, 72.5),
            ),
        ),
    )
}
