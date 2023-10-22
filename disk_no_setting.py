import os
import pathlib
import re
import sys
import glob
from pathlib import Path
from db import TvDiskDao
from data import TvFileData
from datetime import datetime
from moviepy.editor import VideoFileClip


def find_all_files(directory):
    for root, dirs, files in os.walk(directory):
        yield root
        for file in files:
            yield os.path.join(root, file)


class DiskNoSetting:

    def __init__(self):
        self.tv_disk_dao = TvDiskDao()
        # self.base_dir = 'G:\\TV_CONTENTS'
        self.base_dir = 'H:\\TV_CONTENTS'
        self.gravure_dir = 'G:\\GRAVURE_CONTENTS'
        # self.base_dir = 'G:\\TV_CONTENTS_PAST'
        # self.label = 'MEDIA2020'
        self.label = 'MEDIA2022'
        # self.base_dir = 'F:\\TVREC'
        # self.base_dir = 'F:\\JH-STORAGE\\SHARE0\\TVOUT_TEMP'
        # self.base_dir = 'F:\\JH-STORAGE\\SHARE0\\TVOUT'

        # self.is_check = True
        self.is_check = False

    def pickup_no_from_label(self):

        data_list = self.tv_disk_dao.get_where_list()
        # print(dir_id)

        err_count = 0
        for disk_data in data_list:

            label = ''
            try:
                label = re.sub(' ZIP[0-9]{1,3}', '', disk_data.label)
                label = re.sub(' BW970-[0-9]{1,3}', '', label)
                label = re.sub('\(RE[0-9]{1,3}\).*', '', label)
                label = re.sub('F\(RE[0-9]{1,3}\)', '', label)
                label = re.sub('F\([0-9]{1,3}\)', '', label)
                label = re.sub(' STB[0-9]{1,3}', '', label)
                label = re.sub(' 4CW400 START', '', label)
                label = re.sub(' 830.*', '', label)
                label = re.sub(' 100G', '', label)
                label = label.replace('RE', '')
                label = label.replace('F', '')
                label = label.replace(' 2030', '')
                # label = label.replace(' 830', '')
                label = re.sub('\(BW970-[0-9]{1,3}\)', '', label)
                label = re.sub('BW970-[0-9]{1,3}', '', label)
                disk_no = int(label)
                self.tv_disk_dao.update_no(disk_no, disk_data.id)

            except ValueError as verr:
                err_count = err_count + 1
                print(f'disk_no [{disk_data.label}] is not int edit[{label}]')
                continue

        print(err_count)

    def update_path(self):

        data_list = self.tv_disk_dao.get_where_list()
        # print(dir_id)

        # err_count = 0
        for disk_data in data_list:
            if disk_data.path is not None and len(disk_data.path.strip()) > 0:
                continue

            if disk_data.no is None:
                print(f'disk_no is None {disk_data.id} {disk_data.label}')
                continue
            if 1 <= disk_data.no <= 268:
                self.tv_disk_dao.update_path('J:\\BDR-Backup', disk_data.id)
            elif 269 <= disk_data.no <= 530:
                self.tv_disk_dao.update_path('K:\\BDR-Backup', disk_data.id)
            elif 531 <= disk_data.no <= 785:
                self.tv_disk_dao.update_path('I:\\BDR-Backup', disk_data.id)
            elif 786 <= disk_data.no <= 1022:
                self.tv_disk_dao.update_path('M:\\BDR-Backup', disk_data.id)
            elif 1023 <= disk_data.no <= 1275:
                self.tv_disk_dao.update_path('N:\\BDR-Backup', disk_data.id)
            elif 1276 <= disk_data.no <= 1531:
                self.tv_disk_dao.update_path('O:\\BDR-Backup', disk_data.id)
            elif 1532 <= disk_data.no <= 1780:
                self.tv_disk_dao.update_path('P:\\BDR-Backup', disk_data.id)
            elif 1781 <= disk_data.no <= 2113:
                self.tv_disk_dao.update_path('Q:\\BDR-Backup', disk_data.id)
            elif 2114 <= disk_data.no <= 3000:
                self.tv_disk_dao.update_path('R:\\BDR-Backup', disk_data.id)

        # print(err_count)

    def exist_check(self):

        data_list = self.tv_disk_dao.get_where_list()
        # print(dir_id)

        err_count = 0
        for disk_data in data_list:
            # if disk_data.path is not None and len(disk_data.path.strip()) > 0:
            #     print(f'SKIP {disk_data.id}')
            #     continue

            if disk_data.path is None:
                print(f'path None SKIP {disk_data.id}')
                continue

            label = disk_data.label
            if 1 <= disk_data.no <= 93:
                if re.search('[0-9]{1,2}$', label):
                    label = f'{label:0>3}'
                elif re.search('[0-9]{1,2}F$', label):
                    label = f'{disk_data.no:0>3}'
            pathname = os.path.join(disk_data.path, label)
            if os.path.exists(pathname):
                continue

            path_list = glob.glob(os.path.join(disk_data.path, '*'))
            # path_list = glob.glob('N:\\BDR-Backup\\*')
            label = ''
            for path_data in path_list:
                if '1276' in disk_data.label:
                    idx_idx = 0
                p_path = Path(path_data)
                pattern_str = f'{disk_data.no}.*'
                # if str(disk_data.no) in p_path.name:
                if re.search(pattern_str, p_path.name):
                    label = p_path.name
                    # print(label)
                    break

            if len(label) <= 0:
                err_count = err_count + 1
                print(f'disk_no is None {disk_data.no} {disk_data.label} {disk_data.path}')
            else:
                print(f'find {label} <-- {disk_data.no} {disk_data.label}')
                self.tv_disk_dao.update_label(label, disk_data.id)

        print(err_count)



if __name__ == '__main__':
    dick_no_setting = DiskNoSetting()
    # dick_no_setting.pickup_no_from_label()
    # dick_no_setting.update_path()
    dick_no_setting.exist_check()
