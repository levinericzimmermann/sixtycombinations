if __name__ == "__main__":
    import argparse
    import random
    import time

    import expenvelope
    import pyo

    from mutwo.converters.mutwo import LoudnessToAmplitudeConverter

    # levels = (0, 50, 64, 75, 82, 78, 76, 80, 83.3, 79)
    # frequencies = (0, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000)
    # frequencies = tuple(b - a for a, b in zip(frequencies, frequencies[1:]))
    # k50fl_specification = expenvelope.Envelope.from_levels_and_durations(
    #     levels, frequencies
    # )

    PARSER = argparse.ArgumentParser()
    PARSER.add_argument("--static", type=bool, default=False)
    PARSED_ARGS = PARSER.parse_args()
    STATIC = PARSED_ARGS.static

    levels = (
        0,
        53,
        67,
        67,
        76,
        70,
        80,
        76,
        64,
        73,
        75,
        76,
        74,
        80,
        76,
        73,
        76,
        73,
        75,
        73,
        73,
        72,
        75,
        75,
    )
    frequencies = (
        0,
        30,
        40,
        50,
        60,
        70,
        80,
        100,
        120,
        160,
        200,
        250,
        300,
        400,
        500,
        600,
        800,
        1000,
        2000,
        3000,
        4000,
        5000,
        10000,
        20000,
    )
    frequencies = tuple(b - a for a, b in zip(frequencies, frequencies[1:]))
    k50fl_specification = expenvelope.Envelope.from_levels_and_durations(
        levels, frequencies
    )

    converter = LoudnessToAmplitudeConverter(2)

    server = pyo.Server(audio="jack").boot().start()
    dur = 0.4
    sleep = 0.11

    fifths = list(range(8))
    random.seed(100)
    random.shuffle(fifths)

    for fifth in fifths:
        frequency = 100 * ((15 / 8) ** fifth)
        if STATIC:
            amp = 0.03
        else:
            amp = converter.convert(frequency)

        print(frequency, amp)

        f = pyo.Fader(mul=amp, fadeout=0.01, dur=dur)

        sine = pyo.Sine(freq=frequency, mul=f).out(dur=dur)
        f.play()
        time.sleep(dur + sleep)
