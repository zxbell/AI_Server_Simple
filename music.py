# -*- coding:utf-8 -*-

import os
import re
import requests

UC_PATH = r'C:\Users\zhongxuefei\AppData\Local\Netease\CloudMusic\Cache\Cache'  # 缓存路径
MP3_PATH = r'D:\mp3'  # 存放歌曲路径


class Transform():
    def do_transform(self):
        files = os.listdir(UC_PATH)
        for file in files:
            #if file[-3:] == 'uc!':  # 后缀uc!结尾为歌曲缓存
            if file[-2:] == 'uc':  # 后缀uc!结尾为歌曲缓存
                print(file)

                song_id = self.get_songid_by_filename(file)
                song_name, singer_name = self.get_song_info(song_id)
                if song_name !=None and singer_name!= None:
                    a = re.findall(r'[^\*"/:?\\|<>]', song_name, re.S)  # 去除不能做文件名的字符
                    #a = re.findall(r'[\ / \\\:\ * \?\"\<\>\|]', song_name, re.S)

                    song_name = "".join(a)
                else:
                    song_name=song_id

                #song_name = 'Israel Philharmonic Orchestra'
                #singer_name='Itzhak Perlman'
                mp3_file_name = MP3_PATH + '%s - %s.mp3' % (singer_name, song_name)
                if os.path.exists(mp3_file_name) == False:
                    uc_file = open(UC_PATH + file, mode='rb')
                    uc_content = uc_file.read()
                    mp3_content = bytearray()
                    for byte in uc_content:
                        byte ^= 0xa3
                        mp3_content.append(byte)

                    mp3_file = open(mp3_file_name, 'wb')
                    mp3_file.write(mp3_content)
                    uc_file.close()
                    mp3_file.close()
                    print('success %s' % mp3_file_name)
                else:
                    print('%s exists already!' % mp3_file_name)
                if os.path.exists(mp3_file_name):
                    os.remove(UC_PATH + file)

    def get_songid_by_filename(self, file_name):
        match_inst = re.match('\d*', file_name)  # -前面的数字是歌曲ID，例：1347203552-320-0aa1
        if match_inst:
            return match_inst.group()
        return ''

    def get_song_info(self, song_id):
        if not song_id:
            return str(song_id), ''

        try:
            url = 'https://api.imjad.cn/cloudmusic/'  # 请求url例子：https://api.imjad.cn/cloudmusic/?type=detail&id=1347203552
            payload = {'type': 'detail', 'id': song_id}
            reqs = requests.get(url, params=payload)
            jsons = reqs.json()
            song_name = jsons['songs'][0]['name']
            singer = jsons['songs'][0]['ar'][0]['name']
            print(song_name,singer)
            return song_name, singer
        except:
            return str(song_id), ''


def check_path():
    global UC_PATH, MP3_PATH

    if not os.path.exists(UC_PATH):
        print('缓存路径错误: %s' % UC_PATH)
        return False
    if not os.path.exists(MP3_PATH):
        print('目标路径错误: %s' % MP3_PATH)
        return False

    if UC_PATH[-1] != '/':  # 容错处理 防止绝对路径结尾不是/
        UC_PATH += '/'
    if MP3_PATH[-1] != '/':
        MP3_PATH += '/'
    return True


if __name__ == '__main__':
    if not check_path():
        exit()

    transform = Transform()
    transform.do_transform()