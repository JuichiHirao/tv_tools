import os
import pathlib
import sys
import glob
from db import TvFileDao, TvStoreDao
from data import TvFileData
from datetime import datetime
from moviepy.editor import VideoFileClip


def find_all_files(directory):
    for root, dirs, files in os.walk(directory):
        yield root
        for file in files:
            yield os.path.join(root, file)


class NetContentsArrangement:

    def __init__(self):
        # self.tv_file_dao = TvFileDao()
        # self.base_dir = 'G:\\TV_CONTENTS'
        self.base_dir = 'H:\\NET'
        self.label = 'MEDIA2022_NET'

        # self.is_check = True
        self.is_check = False

    def __get_duration(self, pathname: str = ''):

        duration = 0
        try:
            clip = VideoFileClip(pathname)
            duration = int(clip.duration)
        except:
            print(sys.exc_info())

        return duration

    def execute(self):

        path_list = glob.glob(os.path.join(self.base_dir, '24*'))
        self.tv_file_dao = TvFileDao()
        self.tv_store_dao = TvStoreDao()
        where_sql = f'WHERE path = %s'
        store_list = self.tv_store_dao.get_where_list(where_sql, [self.base_dir])
        if store_list is None or len(store_list) <= 0:
            print(f'not store [{self.base_dir}]')
            sys.exit(-1)
        elif len(store_list) > 1:
            print(f'many store [{self.base_dir}]')
            sys.exit(-1)
        store_data = store_list[0]

        register_cnt = 0
        for idx, path in enumerate(path_list):
            p_file = pathlib.Path(path)

            if self.tv_file_dao.is_exist(p_file.name):
                continue

            file_data = TvFileData()
            file_data.duration = self.__get_duration(str(p_file.resolve()))
            file_data.storeId = store_data.id
            file_data.name = p_file.name
            file_data.label = self.label
            file_data.source = 'net'
            p_file_stat = p_file.stat()
            file_data.size = p_file_stat.st_size
            file_data.fileDate = datetime.fromtimestamp(p_file_stat.st_mtime)
            file_data.set_video_info()
            file_data.set_time()
            file_data.print()
            if self.is_check is False:
                print('execute {}'.format(file_data.name))
                self.tv_file_dao.export(file_data)
            else:
                print('check {}'.format(file_data.name))
                self.tv_file_dao.export(file_data, True)

            register_cnt = register_cnt + 1
            # if register_cnt > 3:
            #     break

        print(f'register_count {register_cnt}   base_dir [{self.base_dir}] label {self.label}')


if __name__ == '__main__':
    net_contents_arrangement = NetContentsArrangement()
    net_contents_arrangement.execute()
