from sinsound import cos_wave, FMCW_wave
import scipy.signal as signal
import numpy as np

signal_types = ['cos 18kHz', 'cos 20kHz', 'cos 2kHz', 'chirp 40ms 18e3-20e3kHz', 'customized']


def get_all_types():
    return signal_types


def get_signal_by_type(type, customized_signal_file=None):
    t = 30
    if type == 'cos 18kHz':
        return cos_wave(1, 18e3, 48e3, t)
    elif type == 'cos 20kHz':
        return cos_wave(1, 20e3, 48e3, t)
    elif type == 'cos 2kHz':
        return cos_wave(1, 2e3, 48e3, t)
    elif type == 'chirp 40ms 18e3-20e3kHz':
        return FMCW_wave(48e3, t, 0.04, 18e3, 20e3)
    elif type == 'customized':
        return customized_signal_file
