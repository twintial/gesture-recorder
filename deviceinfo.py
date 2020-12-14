import sounddevice as sd
from scipy.io import wavfile
from sinsound import cos_wave


def get_drivers():
    driver_device_dict = {}
    host_api_tuple = sd.query_hostapis()
    for temp_dict in host_api_tuple:
        driver_device_dict[temp_dict["name"]] = temp_dict["devices"]
    return driver_device_dict


def get_devices(driver_device_dict, kind='input', driver='ASIO'):
    devices_name = []
    devices_num = driver_device_dict[driver]
    for n in devices_num:
        device_dict = sd.query_devices(n)
        if kind and device_dict[f'max_{kind}_channels'] > 0:
            devices_name.append({'name': device_dict['name'],
                                 'id': n,
                                 'channels': device_dict[f'max_{kind}_channels']})
    return devices_name


def play_and_record(input_device_id, output_device_id, signal, rec_file_path, fs=48000, rec_file_channels=1):
    # 首先设置默认输出和输入声道
    sd.default.device[0] = input_device_id
    sd.default.device[1] = output_device_id

    # 开始边录边播
    rec_data = sd.playrec(data=signal, samplerate=fs, channels=rec_file_channels, blocking=True)
    # 存储录音文件
    wavfile.write(rec_file_path, fs, rec_data)


def stop():
    sd.stop()


if __name__ == '__main__':
    print(get_drivers())
    output = get_devices(get_drivers(), kind='output', driver='MME')
    print(output)
    input = get_devices(get_drivers(), kind='input', driver='ASIO')
    print(input)
    y = cos_wave(1, 18e3, 48e3, 10)
    # play_and_record(input[0]['id'], output[0]['id'], y, 't.wav', rec_file_channels=2)
