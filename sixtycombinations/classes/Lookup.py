import typing

from mu.utils import infit


class Lookup(typing.Dict[str, infit.InfIt]):
    def __call__(self, key: str) -> str:
        return next(self[key])
