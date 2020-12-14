from sinsound import cos_wave

signal_types = ['cos 18kHz', 'cos 20kHz']


def get_signal_by_type(type):
    t = 60
    if type == 'cos 18kHz':
        return cos_wave(1, 18e3, 48e3, t)
    elif type == 'cos 20kHz':
        return cos_wave(1, 20e3, 48e3, t)
