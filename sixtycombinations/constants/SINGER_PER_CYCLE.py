from mutwo.parameters import pitches

from sixtycombinations.classes.Ambitus import Ambitus


class IsisVoice(object):
    def __init__(self, ambitus, singing_voice: str, singing_style: str):
        self.ambitus = ambitus
        self.singing_voice = singing_voice
        self.singing_style = singing_style


SINGER_PER_CYCLE = (
    # tenor male pop singer
    IsisVoice(Ambitus(pitches.DirectPitch(110), pitches.DirectPitch(300)), "RT", "jG"),
    # female mezzo-soprano pop singer
    IsisVoice(Ambitus(pitches.DirectPitch(260), pitches.DirectPitch(600)), "MS", "jG"),
    # female soprano lyrical singer
    IsisVoice(Ambitus(pitches.DirectPitch(390), pitches.DirectPitch(1000)), "EL", "jG"),
)
