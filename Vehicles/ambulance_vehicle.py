SIREN_SCENARIO = 5

# Paste Vehicle code 
# ------------------

# ------------------

basic.show_leds("""
    . . # . .
    . . # . .
    # # # # #
    . . # . .
    . . # . .
    """)

def ambulance_forever_loop(scenario: number):
    if scenario == END_SCENARIO:
        for note_frequency in range(300, 700, 5):
            music.play(music.tone_playable(note_frequency, 50), music.PlaybackMode.UNTIL_DONE)
            
        for note_frequency in range(700, 300, -5):
            music.play(music.tone_playable(note_frequency, 50), music.PlaybackMode.UNTIL_DONE)

def on_forever():
    ambulance_forever_loop(scenario)

basic.forever(on_forever)
