import numpy as np
import scipy.signal as signal


def cos_wave(A, f, fs, t, phi=0):
    '''
    :params A:    振幅
    :params f:    信号频率
    :params fs:   采样频率
    :params phi:  相位
    :params t:    时间长度
    '''
    # 若时间序列长度为 t=1s,
    # 采样频率 fs=1000 Hz, 则采样时间间隔 Ts=1/fs=0.001s
    # 对于时间序列采样点个数为 n=t/Ts=1/0.001=1000, 即有1000个点,每个点间隔为 Ts
    Ts = 1 / fs
    n = t / Ts
    n = np.arange(n)
    # 默认类型为float32
    y = A * np.cos(2 * np.pi * f * n * Ts + phi * (np.pi / 180)).astype(np.float32)
    return y


def FMCW_wave(fs, t, T, f0, f1):
    ts = np.arange(0, T, 1.0 / fs)
    sweep = signal.chirp(ts, f0, T, f1, method='linear').astype(np.float32)
    c = int(t/T)  # 这里取整
    y = sweep
    for i in range(c-1):
        y = np.hstack((y, sweep))
    return y