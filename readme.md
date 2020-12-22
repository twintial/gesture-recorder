# Build
pyinstaller -Fw ui.py -p deviceinfoV2.py -p signalgenerator.py -p sinsound.py -p recordtool.py
# notice
1. 发射的sinusoid采样率均为48kHz
2. 保存的wav文件，数据格式为16bit int，采样率为48kHz，声道数量为录音设备的最大channel数量