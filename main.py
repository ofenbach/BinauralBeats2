from nicegui import ui
import numpy as np
import sounddevice as sd
import cat_design

playing = False

def generate_binaural_beats(base_frequency, delta_frequency, duration, sample_rate=44100):
    t = np.linspace(0, duration, duration * sample_rate, False)
    left_ear = np.sin(2 * np.pi * base_frequency * t)
    right_ear = np.sin(2 * np.pi * (base_frequency + delta_frequency) * t)
    stereo_signal = np.vstack((left_ear, right_ear)).T
    return stereo_signal

def play_binaural_beats(base_frequency, delta_frequency, duration, sample_rate=44100):
    global playing
    if not playing:
        playing = True
        binaural_beats = generate_binaural_beats(base_frequency, delta_frequency, duration, sample_rate)
        sd.play(binaural_beats, sample_rate, blocking=False)

def pause_playback():
    global playing
    if playing:
        playing = False
        sd.stop()

def main():
    cat = cat_design.CatDesign(ui)

    cat.typography("BinauralBeat Generator", "h1")

    cat.divider()  # default cat divider

    with ui.element('div').classes('flex w-full'):

        with cat.box(classes='w-1/3 flex'):  # box is a div with cat styling applied
            cat.typography("Choose your base frequency.", "h3")
            cat.typography("This frequency defines the left ear frequency.", "p1")  # label element with cat styling
            slider_base = ui.slider(min=40, max=200, value=100)
            ui.label().bind_text_from(slider_base, 'value').style('color: white;')

        with cat.box(classes='w-1/3 flex ml-8 mr-8'):  # box is a div with cat styling applied
            cat.typography("Choose your delta frequency.", "h3")
            slider_delta = ui.slider(min=0, max=24, value=10)
            ui.label().bind_text_from(slider_delta, 'value').style('color: white;')

        with ui.element('div'):
            ui.button('Play', on_click=lambda: play_binaural_beats(slider_base.value, slider_delta.value, 500)).classes('mr-8')
            ui.button('Pause', on_click=pause_playback)



    cat.divider()  # default cat divider

    cat.typography("Presets", variant="h1")
    cat.typography("Choose pre defined binaural beats", variant="p1")
    with cat.box():
        ui.button('Alpha 10hz - Alertness, Calmness', on_click=lambda: play_binaural_beats(140, 10, 500)).classes('mr-8')
        ui.button('Beta 16hz - High focus', on_click=lambda: play_binaural_beats(140, 16, 500)).classes('mr-8')
        ui.button('Theta 6hz - meditative state', on_click=lambda: play_binaural_beats(140, 6, 500)).classes('mr-8')
        ui.button('Delta 1hz - Sleepiness', on_click=lambda: play_binaural_beats(140, 1, 500)).classes('mr-8')

    cat.divider()

    ui.run()

main()
