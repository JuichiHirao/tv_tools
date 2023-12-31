import os
import pathlib
import sys
from db import TvRecordedDao, TvProgramDao
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
        # self.tv_file_dao = TvFileDao()
        self.tv_recorded_dao = TvRecordedDao()
        self.tv_program_dao = TvProgramDao()

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


if __name__ == '__main__':

    command_list = ['list']
    action_or_dir_name = ''

    channel_no = 0
    channel_seq = 0

    if len(sys.argv) < 2:
        print('param1 [list or channel_no], param2 [channel_seq]')
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
