# states

## state-0 (static, quiet, not-rhythmic)

state0 = {
    "spectrality": 0.7,
    "synthesizer_curve": (1, 0.285),
    "bandwidth": 2,
    "attack_duration_tendency": (2.3, 2.9),
    "release_duration_tendency": (1.8, 2.8),
    "loudness_tendency": (0.4, 1),
    "density_tendency": (0.19, 0.95),
    "minimal_phases_per_sound_tendency": (2, 8000),
    "filter_frequency": 0.175,
    "filter_q": -14,
}


## state-1 (calm and quiet windlike)

state1 = {
    "spectrality": 0.7,
    "synthesizer_curve": (1, 0.01),
    "bandwidth": 0.01,
    "attack_duration_tendency": (0.8, 1.9),
    "release_duration_tendency": (0.7, 1.3),
    "loudness_tendency": (0, 1),
    "density_tendency": (0.1, 0.25),
    "minimal_phases_per_sound_tendency": (200, 2400),
    "filter_frequency": 0.875,
    "filter_q": -12,
}


## state-2 (moving and exciting)

state2 = {
    "spectrality": 0.8,
    "synthesizer_curve": (1, 0.8),
    "bandwidth": 0.1,
    "attack_duration_tendency": (0.01, 0.02),
    "release_duration_tendency": (0.01, 0.02),
    "loudness_tendency": (0, 1),
    "density_tendency": (0.05, 0.4),
    "minimal_phases_per_sound_tendency": (2, 7),
    "filter_frequency": 0,
    "filter_q": -15,
}


## state-3 (insect sounds)
### (using activity level algorithm)

state3 = {
    "spectrality": 0.8,
    "synthesizer_curve": (1, 0.8),
    "bandwidth": 0.1,
    "attack_duration_tendency": (0.01, 0.02),
    "release_duration_tendency": (0.01, 0.02),
    "loudness_tendency": (0, 1),
    "density_tendency": (0.05, 0.6),
    "minimal_phases_per_sound_tendency": (20, 300),
    "filter_frequency": 0.9,
    "filter_q": -7,
}
