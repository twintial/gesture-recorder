from sinsound import cos_wave

signal_types = ['cos 18kHz', 'cos 20kHz', 'cos 2kHz', 'customized']


def get_all_types():
    return signal_types


def get_signal_by_type(type, customized_signal_file=None):
    t = 60
    if type == 'cos 18kHz':
        return cos_wave(1, 18e3, 48e3, t)
    elif type == 'cos 20kHz':
        return cos_wave(1, 20e3, 48e3, t)
    elif type == 'cos 2kHz':
        return cos_wave(1, 2e3, 48e3, t)
    elif type == 'customized':
        return customized_signal_file
