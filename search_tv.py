import io
import os
import pathlib
import csv
import sys
from db import TvRecordedDao, TvProgramDao
from data import TvFileData
from datetime import datetime
from moviepy.editor import VideoFileClip


search_condition_csv = """
1,ドリフ,p
"""
def find_all_files(directory):
    for root, dirs, files in os.walk(directory):
        yield root
        for file in files:
            yield os.path.join(root, file)


class SearchConditionData:
    def __init__(self):
        self.label = ''
        self.name = ''
        self.type = ''


class TvContentsRegister:

    def __init__(self):
        # self.tv_file_dao = TvFileDao()
        self.tv_recorded_dao = TvRecordedDao()
        self.tv_program_dao = TvProgramDao()
        self.search_condition_list = []
        csv_data = csv.reader(io.StringIO(search_condition_csv))

        for row in csv_data:
            if len(row) <= 0:
                continue
            self.search_condition_list.append(row)
            # print(row)

    def get_list(self):

        # dir_id = self.tv_file_dao.get_dir_id(self.base_dir)
        # if dir_id <= 0:
        #     print('store_idに存在しないパスが設定されました {}'.format(self.base_dir))
        #     exit(-1)
        program_list = self.tv_program_dao.get_where_list('WHERE channel_no IN (644, 665)')

        print('{} 件'.format(len(program_list)))
        for program_data in program_list:
            print('{} {} {}'.format(program_data.channelNo, program_data.channelSeq, program_data.name))

        # print('')
        # print('base_dir {}'.format(self.base_dir))
        # print('label {}'.format(self.label))

    def get_list_by_condition(self, condition_data: list = None):

        if condition_data is None:
            return []

        param_list = [f'%{condition_data[1]}%']
        program_list = self.tv_program_dao.get_where_list('WHERE name LIKE %s', param_list)

        print('{} 件'.format(len(program_list)))
        # for program_data in program_list:
        #     print('{} {} {}'.format(program_data.channelNo, program_data.channelSeq, program_data.name))

        return program_list

    def get_channel_list(self, channel_no, channel_seq):

        recorded_list = self.tv_recorded_dao.get_where_list('WHERE channel_no = %s AND channel_seq = %s'
                                                            , [channel_no, channel_seq])

        print('{} 件'.format(len(recorded_list)))
        detail_list = []
        for recorded_data in recorded_list:
            detail = recorded_data.detail if recorded_data.detail is not None else ''
            detail_list.append(detail)

        sort_list = sorted(detail_list)
        for detail in sort_list:
            print('{}'.format(detail))

    def get_recorded_list(self, sql_where):

        print(sql_where)
        recorded_list = self.tv_recorded_dao.get_where_list(sql_where)

        print('{} 件'.format(len(recorded_list)))

        return recorded_list


if __name__ == '__main__':

    command_list = ['list']
    action_or_dir_name = ''

    channel_no = 0
    channel_seq = 0

    if len(sys.argv) < 2:
        print('param1 [list or channel_no], param2 [channel_seq]')
        tv_contents_register = TvContentsRegister()
        for data in tv_contents_register.search_condition_list:
            print(data)
        program_list = tv_contents_register.get_list_by_condition(tv_contents_register.search_condition_list[0])
        for program_data in program_list:
            print('{} {} {}'.format(program_data.channelNo, program_data.channelSeq, program_data.name))

        sql_condition = ''
        for program_data in program_list:
            sql_condition = sql_condition + ' OR (channel_no = {} AND channel_seq = {})'.format(program_data.channelNo, program_data.channelSeq)
        print(f'{sql_condition}')
        sql_condition = 'WHERE ' + sql_condition[4:] + ' ORDER BY on_air_date DESC'
        recorded_list = tv_contents_register.get_recorded_list(sql_condition)
        for recorded_data in recorded_list:
            on_air_date_str = datetime.strftime(recorded_data.onAirDate, '%Y-%m-%d')
            disk_seq = f'{recorded_data.diskNo} {recorded_data.seqNo}'
            print(f'{disk_seq:<20} {on_air_date_str:<10} {recorded_data.detail}')

        exit(0)

    if len(sys.argv) >= 2:
        param1 = sys.argv[1]
        if param1 in command_list:
            action_or_dir_name = sys.argv[1]
        else:
            channel_no = int(sys.argv[1])
            print(channel_no)

    if len(sys.argv) >= 3:
        channel_seq = int(sys.argv[2])
        print('no [{}] seq [{}]'.format(channel_no, channel_seq))

    if action_or_dir_name == 'list':
        tv_contents_register = TvContentsRegister()
        tv_contents_register.get_list()
    else:
        tv_contents_register = TvContentsRegister()
        tv_contents_register.get_channel_list(channel_no, channel_seq)
        # tv_contents_register.get_channel_list(644, 1)
    # local_html_arrangement = LocalHtmlArrangement()
    # local_html_arrangement.execute_arrangement(action_or_dir_name)
