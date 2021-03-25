import typing

from mutwo.events import basic
from mutwo.parameters import pitches


class Vibration(basic.SimpleEvent):
    def __init__(
        self,
        pitch: pitches.JustIntonationPitch,
        duration: float,
        amplitude: float,
        attack_duration: float,
        release_duration: float,
        instrument: int,
        bandwidth: float,
        glissando_pitch_at_start: pitches.JustIntonationPitch,
        glissando_pitch_at_end: pitches.JustIntonationPitch,
        glissando_duration_at_start: float,
        glissando_duration_at_end: float,
        bandwidth_for_singer: float,
    ):
        super().__init__(duration)
        self.pitch = pitch
        self.amplitude = amplitude

        (
            self.attack_duration,
            self.release_duration,
        ) = Vibration._adjust_envelope_durations(
            attack_duration, release_duration, duration
        )

        self.instrument = instrument
        self.bandwidth = bandwidth

        self.glissando_pitch_at_start = glissando_pitch_at_start
        self.glissando_pitch_at_end = glissando_pitch_at_end
        (
            self.glissando_duration_at_start,
            self.glissando_duration_at_end,
        ) = self._adjust_envelope_durations(
            glissando_duration_at_start, glissando_duration_at_end, duration
        )
        self.bandwidth_for_singer = bandwidth_for_singer

    @staticmethod
    def _adjust_envelope_durations(
        attack_duration: float, release_duration: float, duration: float
    ) -> typing.Tuple[float]:
        # make sure summed envelope values aren't longer than complete duration
        while attack_duration + release_duration > duration:
            if attack_duration > release_duration:
                attack_duration = release_duration
            elif release_duration > attack_duration:
                release_duration = attack_duration
            if attack_duration > 0:
                attack_duration *= 0.99
            if release_duration > 0:
                release_duration *= 0.99

        return attack_duration / duration, release_duration / duration

    def __repr__(self):
        return "Vibration({}, {}, {})".format(
            str(self.pitch.ratio), round(self.duration, 2), round(self.amplitude, 1)
        )
