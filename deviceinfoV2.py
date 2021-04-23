import pyaudio

from sinsound import cos_wave

p = pyaudio.PyAudio()


def get_drivers():
    driver_dicts = []
    for i in range(p.get_host_api_count()):
        driver_dicts.append(p.get_host_api_info_by_index(i))
    return driver_dicts


def get_devices(driver_dicts, kind='Input', driver='ASIO'):
    driver_dict = {}
    devices_name = []
    for d in driver_dicts:
        if d['name'] == driver:
            driver_dict = d
            break
    for i in range(driver_dict['deviceCount']):
        device_dict = p.get_device_info_by_host_api_device_index(driver_dict['index'], i)
        if kind and device_dict[f'max{kind}Channels'] > 0:
            devices_name.append({'name': device_dict['name'],
                                 'id': device_dict['index'],
                                 'channels': device_dict[f'max{kind}Channels']})
    return devices_name


# def play_and_record(input_device_id, output_device_id, signal, rec_file_path, fs=48000, rec_file_channels=1):
#     chunk = 1024
#     format = pyaudio.paInt16
#     stream = p.open(format=format,
#                     channels=rec_file_channels,
#                     rate=fs,
#                     input=True,
#                     output=True,
#                     input_device_index=input_device_id,
#                     output_device_index=output_device_id,
#                     frames_per_buffer=chunk)
#
#
# def record_audio(wave_out_path, record_second):
#     CHUNK = 1024
#     FORMAT = pyaudio.paInt24
#     CHANNELS = 8
#     RATE = 48000
#     p = pyaudio.PyAudio()
#     stream = p.open(format=FORMAT,
#                     channels=CHANNELS,
#                     rate=RATE,
#                     input=True,
#                     input_device_index=12,
#                     frames_per_buffer=CHUNK)
#     wf = wave.open(wave_out_path, 'wb')
#     wf.setnchannels(CHANNELS)
#     wf.setsampwidth(p.get_sample_size(FORMAT))
#     wf.setframerate(RATE)
#     print("* recording")
#     for i in tqdm(range(0, int(RATE / CHUNK * record_second))):
#         data = stream.read(CHUNK)
#         wf.writeframes(data)
#     print("* done recording")
#     stream.stop_stream()
#     stream.close()
#     p.terminate()
#     wf.close()
#
#
# def play():
#     chunk = 1024
#     wf = wave.open(r"output.wav", 'rb')
#     p = pyaudio.PyAudio()
#     stream = p.open(format=p.get_format_from_width(wf.getsampwidth()), channels=2,
#                     rate=wf.getframerate(), output=True)
#     data = wf.readframes(chunk)  # 读取数据
#     print(data)
#     while data != b'':  # 播放
#         stream.write(data)
#         data = wf.readframes(chunk)
#         print('while循环中！')
#         print(data)
#     stream.stop_stream()  # 停止数据流
#     stream.close()
#     p.terminate()  # 关闭 PyAudio


def playsin():
    y = cos_wave(1, 18e3, 48e3, 10)
    stream = p.open(format=pyaudio.paFloat32, channels=1,
                    rate=48000, output=True)
    stream.write(y)
    stream.stop_stream()  # 停止数据流
    stream.close()
    p.terminate()  # 关闭 PyAudio

if __name__ == '__main__':
    # print(get_drivers())
    # print(get_devices(get_drivers(), kind='Output', driver='MME'))
    #
    # record_audio("output.wav", record_second=10)
    import numpy as np
    a = np.array([1,2,3,4,5])
    print(a[10:11])
