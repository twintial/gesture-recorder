from sinsound import *

signal_types = ['cos 18kHz', 'cos 20kHz',
                'cos 2kHz', 'fmcw 20ms 18e3-22e3kHz',
                'fmcw 40ms 10e3-20e3kHz', 'fmcw 20ms 18e3-22e3kHz sep',
                'sinusoid', 'sinusoid2', 'none', 'customized']


def get_all_types():
    return signal_types


def get_signal_by_type(type, customized_signal_file=None):
    t = 30
    if type == signal_types[0]:
        return cos_wave(1, 18e3, 48e3, t)
    elif type == signal_types[1]:
        return cos_wave(1, 20e3, 48e3, t)
    elif type == signal_types[2]:
        return cos_wave(1, 2e3, 48e3, t)
    elif type == signal_types[3]:
        return FMCW_wave(48e3, t, 0.02, 18e3, 22e3)
    elif type == signal_types[4]:
        return FMCW_wave(48e3, t, 0.04, 10e3, 20e3)
    elif type == signal_types[5]:
        # 有问题
        return FMCW_wave_d_with_sep(48e3, np.arange(0, t, 1 / 48e3), 0.02, 18e3, 22e3, 0)
    elif type == signal_types[6]:
        # A = [1/150, 1/70, 1/90, 1/85, 1/68, 1/40, 1/25, 1/14]
        A = [1, 1, 1, 1, 1, 1, 1, 1]
        alpha = 1 / sum(A)
        print(alpha)
        y = A[0] * cos_wave(1, 17350, 48e3, t)
        for i in range(1, 8):
            y = y + A[i] * cos_wave(1, 17350 + i * 700, 48e3, t)
        return alpha * y
    elif type == signal_types[7]:
        # A = [1/7, 1/25, 1/18, 1/6, 1/10, 1/17, 1/5, 1/10]
        A = [1, 1, 1, 1, 1, 1, 1, 1]
        alpha = 1 / sum(A)
        print(alpha)
        y = A[0] * cos_wave(1, 17000, 48e3, t)
        for i in range(1, 8):
            y = y + A[i] * cos_wave(1, 17000 + i * 350, 48e3, t)
        return alpha * y
    elif type == signal_types[8]:
        return np.array([0] * 48000 * 60)
    elif type == 'customized':
        return customized_signal_file
