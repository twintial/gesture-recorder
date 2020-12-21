import wave

import pyaudio
from PyQt5.QtWidgets import QLCDNumber


class Record:
    def __init__(self, time: QLCDNumber):
        self.wav_file = None

        self.signal = None
        self.cursor = 0

        self.time = time
        self.t = 0

        self.frames = []
        self.chunk = 2048
        self.fs = 48000
        self.channels = 1
        self.format = pyaudio.paInt16 # int24在数据处理上不方便
        self._recording = False
        self._playing = False
        self.save_path = None
        self.input_device_index = None
        self.output_device_index = None

        self.p = pyaudio.PyAudio()
        self.record_stream = None
        self.play_stream = None

    def set_param(self, input_id, output_id, channels, save_path):
        self.input_device_index = input_id
        self.output_device_index = output_id
        self.channels = channels
        self.save_path = save_path

    def input_callback(self, in_data, frame_count, time_info, status_flags):
        self.frames.append(in_data)
        self.t = self.t + frame_count / self.fs
        self.time.display(self.t)
        return in_data, pyaudio.paContinue

    def output_callback(self, in_data, frame_count, time_info, status_flags):
        out_data = self.signal[self.cursor:self.cursor + frame_count]
        self.cursor = self.cursor + frame_count
        if self.cursor + frame_count > len(self.signal):
            self.cursor = 0
        return out_data, pyaudio.paContinue

    def wavfile_output_callback(self, in_data, frame_count, time_info, status_flags):
        out_data = self.wav_file.readframes(frame_count)
        return out_data, pyaudio.paContinue

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
                                           stream_callback=self.wavfile_output_callback
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
                                         channels=self.channels,
                                         rate=self.fs,
                                         input=True,
                                         input_device_index=self.input_device_index,
                                         frames_per_buffer=self.chunk,
                                         stream_callback=self.input_callback)
        self.record_stream.start_stream()

    def play_and_record(self, signal):
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

        self.save()
        self.frames.clear()
        self.t = 0

    def save(self):
        wf = wave.open(self.save_path, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.format))
        wf.setframerate(self.fs)
        wf.writeframes(b''.join(self.frames))
        wf.close()
