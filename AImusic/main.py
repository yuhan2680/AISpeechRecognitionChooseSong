import pygame, easygui,sys,win32com.client
from pygame.locals import *
import wave
from aip import AipSpeech
import numpy as np
from pyaudio import PyAudio, paInt16
import os
x = 450
y = 200
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)
pygame.init()
screen_size = width, height = 500, 354
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('点歌机(长按Enter或者空格录音选歌,松开即为录音结束)')

# 设置字体样式和大小  SysFont不是Font
my_font = pygame.font.SysFont("SimHei",50)
# 渲染文字
text1 = my_font.render('Hop', True, (0, 0, 0))
text2 = my_font.render('多心经', True, (0, 0, 0))
text3 = my_font.render('蓝莲花', True, (0, 0, 0))
text4 = my_font.render('送别', True, (0, 0, 0))
text5 = my_font.render('因为刚好遇见你', True, (0, 0, 0))
text6 = my_font.render('只因你太美', True, (0, 0, 0))
text7 = my_font.render('Bad Guy', True, (0, 0, 0))

NUM_SAMPLES = 2000  # py audio内置缓冲大小
SAMPLING_RATE = 16000  # 取样频率
LEVEL = 500  # 声音保存的阈值
COUNT_NUM = 20  # NUM_SAMPLES个取样之内出现COUNT_NUM个大于LEVEL的取样则记录声音
SAVE_LENGTH = 1  # 声音记录的最小长度：SAVE_LENGTH * NUM_SAMPLES 个取样
#TIME_COUNT = 30  # 录音时间，单位s

Voice_String = []


# 录音保存的路径
def savewav():
    wf = wave.open(r".\voices\say_voice.wav", 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(SAMPLING_RATE)
    wf.writeframes(np.array(Voice_String).tostring())
    wf.close()


# 录音
def recorder():
    pa = PyAudio()
    stream = pa.open(format=paInt16, channels=1, rate=SAMPLING_RATE, input=True,
                     frames_per_buffer=NUM_SAMPLES)
    save_count = 0
    save_buffer = []
    #time_count = TIME_COUNT

    while True:
        pygame.mixer.music.stop()
        #time_count -= 1
        # 读入NUM_SAMPLES个取样
        string_audio_data = stream.read(NUM_SAMPLES)
        # 将读入的数据转换为数组
        audio_data = np.fromstring(string_audio_data, dtype=np.short)
        # 计算大于LEVEL的取样的个数
        large_sample_count = np.sum(audio_data > LEVEL)
        #print('正在录音...')
        pygame.display.set_caption('正在录音...')
        # 如果个数大于COUNT_NUM，则至少保存SAVE_LENGTH个块
        if large_sample_count > COUNT_NUM:
            save_count = SAVE_LENGTH
        else:
            save_count -= 1

        if save_count < 0:
            save_count = 0

        if save_count > 0:
            # 将要保存的数据存放到save_buffer中
            save_buffer.append(string_audio_data)
        else:
            # 将save_buffer中的数据写入WAV文件，WAV文件的文件名是保存的时刻
            if len(save_buffer) > 0:
                global Voice_String
                Voice_String = save_buffer
                print("Recode a piece of  voice successfully!")
                return True
        if event.type==KEYUP and (event.key == 13 or event.key==32):
            if len(save_buffer) > 0:
                Voice_String = save_buffer
                print("Recode a piece of  voice successfully!")
                return True
            else:
                return False
#字体变红的列表
wordRed = [0,0,0,0,0,0,0]
def changeWordToRed(index):
    for i in range(len(wordRed)):
        if i == index-1:
            wordRed[i] = 1
        else:
            wordRed[i] = 0

# 添加背景图片
bg = pygame.image.load("images/mu.jpg")
# 语音转换
def speech_recognition():
    # 百度AI接口
    APP_ID = '11807876'
    API_KEY = '0ldKm88lSv8ntYGlZIThZFxH'
    SECRET_KEY = 'mebRiVfGLONNNtc8ApDVhRhwx2VYKqkl'
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    speaker=win32com.client.Dispatch("SAPI.SpVoice")
    # 读取语音文件
    def get(filepath):
        with open(filepath, 'rb') as fp:
            return fp.read()

    # 识别保存到本地的语音文件
    file = get('./voices/say_voice.wav')
    dev = {
        'dev_pid': 1536,
        'format': 'wav'
    }
    rnt = client.asr(file, 'wav', 16000, dev)
    print(rnt)
    # 识别选择的角色
    try:
        pygame.display.set_caption('长按Enter或者空格录音选歌,松开即为录音结束')
        str = rnt['result'][0]
        if str.find('p') != -1 or str.find('o') != -1 or str.find('铺') != -1 or str.find('后')!=-1 or str.find('P')!=-1 or str.find('O')!=-1:  
            #speaker.Speak('你选择了hop')
            pygame.mixer.music.load('music/Hop.mp3')
            pygame.mixer.music.play()
            changeWordToRed(1)
        elif str.find('鸡你太美') != -1  or str.find('只因') != -1 or str.find('你太美') != -1 :
            pygame.mixer.music.load('music/只因你太美.mp3')
            pygame.mixer.music.play()
            changeWordToRed(2)
        elif str.find('心经') != -1  or str.find('多心经') != -1 or str.find('新津') != -1 :
            pygame.mixer.music.load('music/多心经.mp3')
            pygame.mixer.music.play()
            changeWordToRed(3)
        elif str.find('song') != -1  or str.find('送别') != -1 or str.find('诵憋') != -1 :
            pygame.mixer.music.load('music/送别.mp3')
            pygame.mixer.music.play()
            changeWordToRed(4)
        elif str.find('蓝莲花') != -1  or str.find('懒年华') != -1 or str.find('烂炼化') != -1 or str.find('兰莲花') !=-1 or str.find('莲花') !=-1:
            pygame.mixer.music.load('music/蓝莲花.mp3')
            pygame.mixer.music.play()
            changeWordToRed(5)
        elif str.find('因为') != -1  or str.find('刚好') != -1 or str.find('遇见你') != -1 or str.find('因为刚好遇见你') != -1:
            pygame.mixer.music.load('music/因为刚好遇见你.mp3')
            pygame.mixer.music.play()
            changeWordToRed(6)
        elif str.find('guy') != -1  or str.find('bad') != -1 or str.find('gay') != -1 or str.find('bag') != -1:
            pygame.mixer.music.load('music/Bad Guy.mp3')
            pygame.mixer.music.play()
            changeWordToRed(7)
        else:
            # 语音模糊无法识别，重新开始选择
            easygui.msgbox('识别失败')
            return None
        
    except Exception as e:
        print(e)






while True:
    #screen不是view放入循环
    screen.blit(bg,(0,0))
            
    screen.blit(text1, (0,0))
    screen.blit(text2, (0,50))
    screen.blit(text3, (0,100))
    screen.blit(text4, (0,150))
    screen.blit(text5, (0,200))
    screen.blit(text6, (0,250))
    screen.blit(text7, (0,300))
    
    # 获取事件列表
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # 下方书写你的代码
        if event.type == KEYDOWN :
            if event.key == 13 or event.key==32:
               recorder()
               savewav()
               result=speech_recognition()
    pygame.display.update()
