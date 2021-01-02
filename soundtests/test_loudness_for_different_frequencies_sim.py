if __name__ == "__main__":
    import argparse
    import time

    import pyo

    from mutwo.converters.mutwo import LoudnessToAmplitudeConverter

    PARSER = argparse.ArgumentParser()
    PARSER.add_argument("--static", type=bool, default=False)
    PARSED_ARGS = PARSER.parse_args()
    STATIC = PARSED_ARGS.static

    converter = LoudnessToAmplitudeConverter(1)

    server = pyo.Server(audio="jack").boot().start()
    dur = 4
    sleep = 0.2

    fifths = list(range(8))

    frequencies = []
    amps = []

    for fifth in fifths:
        frequency = 100 * ((15 / 8) ** fifth)
        amp = converter.convert(frequency)

        frequencies.append(frequency)
        amps.append(amp)

    if STATIC:
        amps = 0.0095
    sine = pyo.Sine(freq=frequencies, mul=amps).out(0, 0, dur=dur)
    time.sleep(dur + sleep)
