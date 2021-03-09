from mutwo.parameters import pitches


class IsisVoice(object):
    def __init__(self, ambitus, singing_voice: str, singing_style: str):
        self.ambitus = ambitus
        self.singing_voice = singing_voice
        self.singing_style = singing_style


SINGER_PER_CYCLE = (
    # tenor male pop singer
    IsisVoice((pitches.DirectPitch(110), pitches.DirectPitch(300)), "RT", "eP"),
    # female mezzo-soprano pop singer
    IsisVoice((pitches.DirectPitch(260), pitches.DirectPitch(600)), "MS", "eP"),
    # female soprano lyrical singer
    IsisVoice((pitches.DirectPitch(390), pitches.DirectPitch(1000)), "EL", "eP"),
)
