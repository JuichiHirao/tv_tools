import os
import pathlib
import sys
from db import TvFileDao
from data import TvFileData
from datetime import datetime
from moviepy.editor import VideoFileClip


def find_all_files(directory):
    for root, dirs, files in os.walk(directory):
        yield root
        for file in files:
            yield os.path.join(root, file)


class TvContentsRegister:

    def __init__(self):
        self.tv_file_dao = TvFileDao()
        self.base_dir = 'M:\\TV_CONTENTS'
        # self.base_dir = 'M:\\TV_CONTENTS_PAST'
        # self.base_dir = 'F:\\TVREC'
        # self.base_dir = 'F:\\JH-STORAGE\\SHARE0\\TVOUT_TEMP'
        # self.base_dir = 'F:\\JH-STORAGE\\SHARE0\\TVOUT'

        self.is_check = True
        # self.is_check = False

    def __get_duration(self, pathname: str = ''):

        duration = 0
        try:
            clip = VideoFileClip(pathname)
            duration = int(clip.duration)
        except:
            print(sys.exc_info())

        return duration

    def execute(self):

        dir_id = self.tv_file_dao.get_dir_id(self.base_dir)
        print(dir_id)
        if dir_id <= 0:
            print('store_idに存在しないパスが設定されました {}'.format(self.base_dir))
            exit(-1)
        for file in find_all_files(self.base_dir):

            p_file = pathlib.Path(file)
            if p_file.is_dir():
                continue

            if self.tv_file_dao.is_exist(p_file.name):
                # print('is_exist {}'.format(p_file.name))
                continue

            file_data = TvFileData()
            file_data.duration = self.__get_duration(str(p_file.resolve()))
            file_data.storeId = dir_id
            file_data.name = p_file.name
            file_data.label = 'MEDIA2020'
            # data.label = 'MEDIA2018-TVREC'
            file_data.source = 'my'
            p_file_stat = p_file.stat()
            file_data.size = p_file_stat.st_size
            file_data.fileDate = datetime.fromtimestamp(p_file_stat.st_mtime)
            file_data.set_time()
            file_data.print()
            if self.is_check is False:
                self.tv_file_dao.export(file_data)

            # idx = idx + 1

    def update_target_duration(self):
        data_list = self.tv_file_dao.get_where_list('WHERE time is null and file_date >= "2020-06-01"')
        for data in data_list:
            data.set_time()
            self.tv_file_dao.update_time(data)
            data.print()


if __name__ == '__main__':
    tv_contents_register = TvContentsRegister()
    tv_contents_register.execute()
    # tv_contents_register.update_target_duration()
