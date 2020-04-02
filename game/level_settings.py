"""waves in form of frequency of enemies (scorpions, wizards, clubs, trolls, swords)"""

# Basic waves
waves = [
    [20, 0, 0, 0, 0],
    [50, 0, 0, 0, 0],
    [100, 0, 0, 0, 0],
    [0, 20, 0, 0, 0, 1],
    [0, 50, 0, 0, 1],
    [0, 100, 0, 0, 0],
    [0, 0, 20, 0, 0],
    [0, 0, 50, 0, 0],
    [0, 0, 100, 0, 0],
    [20, 100, 0, 0, 0],
    [50, 100, 0, 0, 0],
    [100, 100, 0, 0, 0],
    [0, 0, 0, 50, 2],
    [0, 0, 0, 100, 1],
    [20, 0, 0, 150, 1],
    [50, 50, 50, 100, 5],
]

# Bonus and secret wave
bonus_wave = [5, 5, 5, 5, 5, 5]

# Waves for advanced pro players
challenge_waves = [[0, 0, 0, 0, 3, 1],
                   [0, 0, 0, 0, 3, 2],
                   [0, 0, 0, 0, 5, 3]]

