import os
import re
import sys
import glob
from pathlib import Path
from logging import getLogger, DEBUG, Formatter, FileHandler, StreamHandler

from common import DiskTool
from db import TvDiskDao, TvRecordedDao
from datetime import datetime


str_date = datetime.now().strftime('%Y%m%d')
logger = getLogger("logger")
logger.setLevel(DEBUG)

log_filename = 'log\\disk_no_setting_{}.log'.format(str_date)
handler_file = FileHandler(filename=log_filename, encoding='utf-8')
handler_file.setFormatter(Formatter("%(asctime)s %(levelname)4s %(message)s"))
logger.addHandler(handler_file)
handler_stream = StreamHandler(sys.stdout)
handler_stream.setFormatter(Formatter("%(asctime)s %(levelname)8s %(message)s"))
logger.addHandler(handler_stream)

def find_all_files(directory):
    for root, dirs, files in os.walk(directory):
        yield root
        for file in files:
            yield os.path.join(root, file)


class DiskNoSetting:

    def __init__(self):
        self.tv_disk_dao = TvDiskDao()
        self.tv_recorded_dao = TvRecordedDao()

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
                logger.info(f'disk_no [{disk_data.label}] is not int edit[{label}]')
                continue

        logger.info(err_count)

    def check_missing_elements(self, arr):
        # 配列をソート
        sorted_arr = sorted(arr)

        # 配列の最初と最後の要素を取得
        start = sorted_arr[0]
        end = sorted_arr[-1]

        # 完全な範囲を作成
        full_range = set(range(start, end + 1))

        # 元の配列をsetに変換
        arr_set = set(arr)

        # 抜けている要素を見つける
        missing_elements = full_range - arr_set

        if missing_elements:
            sorted_missing_element_list = sorted(list(missing_elements))
            logger.info(f'Missing elements: {sorted_missing_element_list}')
        else:
            logger.info("There are no missing elements.")

    # 使用例
    # arr = [1, 2, 4, 6, 7, 8]
    # check_missing_elements(arr)

    def pickup_disk_from_recorded(self, is_checked: bool = True):

        data_list = self.tv_recorded_dao.get_where_list('WHERE created_at >= "2024-11-01" AND disk_no IS NOT NULL')
        disk_data_list = self.tv_disk_dao.get_where_list()
        # print(dir_id)

        recorded_disk_info_list = []
        for data in data_list:
            recorded_disk_info_list.append(f'{data.diskNo},{data.diskLabel}')

        distinct_recorded_disk_info_list = list(set(recorded_disk_info_list))
        logger.info(f'disk_data_list {distinct_recorded_disk_info_list}')

        disk_tool = DiskTool(logger)
        for disk_info in distinct_recorded_disk_info_list:
            disk_no, disk_label = disk_info.split(',')
            disk_no = int(disk_no)
            filter_list = list(filter(lambda disk_data: disk_data.no is not None and disk_data.no == disk_no, disk_data_list))
            base_path = disk_tool.get_path(disk_no)
            if len(filter_list) == 1:
                # logger.info(f'登録済み {filter_list[0].no}')
                pass
            elif len(filter_list) == 0:
                pathname = os.path.join(base_path, disk_label)
                if os.path.isdir(pathname):
                    logger.info(f'exist [{pathname}] no [{disk_no}] label [{disk_label}]')
                else:
                    logger.error(f'パス[{base_path}]が存在しないため強制終了 {disk_no} [{disk_label}]')
                    sys.exit(-1)
                if is_checked is False:
                    self.tv_disk_dao.export(disk_no, disk_label, base_path)
                    logger.info(f'export no [{disk_no}] label [{disk_label}] path [{base_path}]')
                    pass
                else:
                    logger.info(f'dry export no [{disk_no}] label [{disk_label}] path [{base_path}]')
            else:
                logger.warning(f'many exist no [{disk_no}] label [{disk_label}] match_list({len(filter_list)}) {filter_list}')
                pass


        no_list = []
        disk_data_list = self.tv_disk_dao.get_where_list()
        for data in disk_data_list:
            if data.no is None:
                continue
            no_list.append(data.no)
        logger.info(f'max {max(no_list)}')

        self.check_missing_elements(no_list)

        return

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
    # dick_no_setting.exist_check()
    # dick_no_setting.pickup_disk_from_recorded()
    dick_no_setting.pickup_disk_from_recorded(False)
    # dick_no_setting.pickup_disk_from_recorded(True)
