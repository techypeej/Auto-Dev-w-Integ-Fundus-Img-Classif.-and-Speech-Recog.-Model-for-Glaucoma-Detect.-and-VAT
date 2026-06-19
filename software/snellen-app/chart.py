# Standard Snellen chart using Sloan optotype letters: C D E F L N O P T Z
# Font sizes are starting values — calibrate based on your lens and screen setup

SNELLEN_CHART = [
    {"acuity": "20/200", "letters": ["E"],                               "font_size": 220},
    {"acuity": "20/100", "letters": ["F", "P"],                          "font_size": 160},
    {"acuity": "20/70",  "letters": ["T", "O", "Z"],                     "font_size": 120},
    {"acuity": "20/50",  "letters": ["L", "P", "E", "D"],                "font_size": 90},
    {"acuity": "20/40",  "letters": ["P", "E", "C", "F", "D"],           "font_size": 72},
    {"acuity": "20/30",  "letters": ["E", "D", "F", "C", "Z", "P"],      "font_size": 56},
    {"acuity": "20/25",  "letters": ["F", "E", "L", "O", "P", "Z", "D"],"font_size": 46},
    {"acuity": "20/20",  "letters": ["D", "E", "F", "P", "O", "T", "E", "C"], "font_size": 36},
]
