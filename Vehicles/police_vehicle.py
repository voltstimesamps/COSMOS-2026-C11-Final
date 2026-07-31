SIREN_SCENARIO = 5

# Paste Vehicle code 
# ------------------

# ------------------

basic.show_leds("""
    . . # . .
    # # # # #
    . # # # .
    . # . # .
    # . . . #
    """)

def police_forever_loop(scenario):
    if scenario == END_SCENARIO:
        for note_frequency in range(400, 900, 10):
            music.play(music.tone_playable(note_frequency, 30), music.PlaybackMode.UNTIL_DONE)
        
        for note_frequency in range(900, 400, -10):
            music.play(music.tone_playable(note_frequency, 30), music.PlaybackMode.UNTIL_DONE)

def on_forever():
    police_forever_loop(scenario)

basic.forever(on_forever)
