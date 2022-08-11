import sys
import wave
import numpy as np
import pyaudio
from PyQt5.QtWidgets import QLCDNumber
import matplotlib.pyplot as plt


class Record:
    def __init__(self, time: QLCDNumber):
        self.wav_file = None
        self.wf = None

        self.signal = None
        self.cursor = 0

        self.time = time
        # seconds
        self.t = 0
        self.n_file_split = 1
        self.file_split_time = 0
        self.file_split_time_flag = 60 * 60 # 60min

        self.frames = []
        self.chunk = 7200
        self.fs = 48000
        self.input_channels = 1
        self.format = pyaudio.paInt16  # int24在数据处理上不方便,改为int16
        self._recording = False
        self._playing = False

        self.base_save_path = None
        self.save_path = None
        self.input_device_index = None
        self.output_device_index = None

        self.p = pyaudio.PyAudio()
        self.record_stream = None
        self.play_stream = None

    def set_param(self, input_id, output_id, input_channels, save_path):
        self.input_device_index = input_id
        self.output_device_index = output_id
        self.input_channels = input_channels
        self.save_path = save_path
        self.base_save_path = save_path

    def update_save_file_name(self):
        self.save_path = self.base_save_path.replace('.wav', f'_{self.n_file_split}.wav')
        self.n_file_split += 1

    def input_callback(self, in_data, frame_count, time_info, status_flags):
        # self.frames.append(in_data)
        if self.file_split_time > self.file_split_time_flag:
            self.update_save_file_name()
            self.prepare_wav_file()
            self.file_split_time = 0
        self.wf.writeframes(in_data)
        # input_channel必须是1
        self.t = self.t + frame_count / self.fs
        # 文件分割信号
        self.file_split_time = self.file_split_time + frame_count / self.fs
        self.time.display(self.t)
        return in_data, pyaudio.paContinue

    def output_callback(self, in_data, frame_count, time_info, status_flags):
        out_data = self.signal[self.cursor:self.cursor + frame_count]
        self.cursor = self.cursor + frame_count
        # 存在最后一小段放不出的问题
        if self.cursor + frame_count > len(self.signal):
            self.cursor = 0
        return out_data, pyaudio.paContinue

    def wav_file_output_callback(self, in_data, frame_count, time_info, status_flags):
        # 如果要连续播放，chunk的大小必须能被音频样本点整除
        out_data = self.wav_file.readframes(frame_count)
        if len(out_data) == 0:
            # print("l:", frame_count * self.wav_file.getnchannels() * self.wav_file.getsampwidth())
            self.wav_file.rewind()
            out_data = self.wav_file.readframes(frame_count)
        return out_data, pyaudio.paContinue

    def prepare_wav_file(self):
        if self.wf is not None:
            self.wf.close()
        # open save wav file
        self.wf = wave.open(self.save_path, 'wb')
        self.wf.setnchannels(self.input_channels)
        self.wf.setsampwidth(self.p.get_sample_size(self.format))
        self.wf.setframerate(self.fs)

    def play_signal(self, signal):
        # signal可能是一个wav文件名称或者是一串信号
        self._playing = True
        self.signal = signal
        if type(signal) == str:
            self.wav_file = wave.open(signal, "rb")
            self.play_stream = self.p.open(format=self.p.get_format_from_width(self.wav_file.getsampwidth()),
                                           channels=self.wav_file.getnchannels(),
                                           rate=self.wav_file.getframerate(),
                                           output=True,
                                           output_device_index=self.output_device_index,
                                           frames_per_buffer=self.chunk,
                                           stream_callback=self.wav_file_output_callback
                                           )
        else:
            # p = pyaudio.PyAudio()
            self.play_stream = self.p.open(format=pyaudio.paFloat32,
                                           channels=1,
                                           rate=self.fs,
                                           output=True,
                                           output_device_index=self.output_device_index,
                                           frames_per_buffer=self.chunk,
                                           stream_callback=self.output_callback)
        self.play_stream.start_stream()

    def record(self):
        self.record_stream = self.p.open(format=self.format,
                                         channels=self.input_channels,
                                         rate=self.fs,
                                         input=True,
                                         input_device_index=self.input_device_index,
                                         frames_per_buffer=self.chunk,
                                         stream_callback=self.input_callback)
        self.record_stream.start_stream()

    def play_and_record(self, signal):
        self.prepare_wav_file()
        self.play_signal(signal)
        self.record()

    def stop(self):
        self.record_stream.stop_stream()
        self.record_stream.close()
        self.play_stream.stop_stream()
        self.play_stream.close()
        if type(self.signal) == str:
            self.wav_file.close()
        # self.p.terminate()

        # self.save()
        self.wf.close()
        self.frames.clear()
        self.t = 0

    # def save(self):
    #     wf = wave.open(self.save_path, 'wb')
    #     wf.setnchannels(self.channels)
    #     wf.setsampwidth(self.p.get_sample_size(self.format))
    #     wf.setframerate(self.fs)
    #     wf.writeframes(b''.join(self.frames))
    #     wf.close()
