import setuptools

setuptools.setup(
    name="sixtycombinations",
    version="0.0.01",
    license="GPL",
    description="sound installation for 15 miniature speaker",
    author="Levin Zimmermann <levin-eric.zimmermann@folkwang-uni.de>",
    url="https://github.com/levinericzimmermann/sixtycombinations",
    packages=setuptools.find_packages(),
    setup_requires=[],
    tests_require=["nose"],
    install_requires=[
        "pyo>=1.0.3",
        "mutwo>=0.0.01",
        "ortools>=8.1.8487",
        "quicktions",
        "sox",
    ],
    python_requires=">=3.7",
)
