import openpyxl
from db import TvRecordedDao
from db import TvProgramDao
from data import TvRecordedData
from datetime import datetime


class TvContentsRegister:

    def __init__(self):
        self.recorded_dao = TvRecordedDao()
        self.program_dao = TvProgramDao()
        self.excel_file = 'C:\\Users\\JuichiHirao\\Dropbox\\jhdata\\Interest\\BD番組録画.xlsx'
        # self.base_dir = 'F:\\TVREC'

        # self.is_check = True
        self.is_check = False

    def __check_program_id(self, target_idx, row):
        # H829 不明なので、OK
        # H2129 不明なので、OK
        program_id = -1
        cell_value = row[target_idx].value
        if cell_value is None:
            print('program id None {} {}'.format(row[target_idx], cell_value))
        elif type(cell_value) is not int:
            print('program id not int {} {} {}'.format(target_idx, row[target_idx], cell_value))
        else:
            program_id = int(cell_value)

        return program_id

    def __get_minute(self, time_str):

        if time_str is None or len(str(time_str)) <= 0:
            return 0

        time_list = str(time_str).split(':')
        minute = 0
        if len(time_list) == 2:
            minute = (int(time_list[0]) * 60) + int(time_list[1])

        return minute

    def __get_cell_data(self, target_idx, row):
        cell_value = row[target_idx].value
        if cell_value is not None and type(cell_value) is not str:
            print('{} {} {} not type str'.format(target_idx, row[target_idx], cell_value))
        elif cell_value is not None and len(cell_value) > 0:
            print('{} {} {}'.format(target_idx, row[target_idx], cell_value))

        return cell_value

    def __get_on_air_datetime(self, row, idx_date, idx_time):

        on_air_datetime = None
        on_air_date_str = None
        date_value = row[idx_date].value
        time_value = str(row[idx_time].value)
        # print('date_value {} time_value {}'.format(date_value, time_value))
        try:
            if date_value is not None:
                if type(date_value) is not datetime:
                    on_air_date_str = datetime.strftime(on_air_datetime, '%Y/%m/%d')
                else:
                    # on_air_datetime = datetime.strptime(date_value, '%Y/%m/%d')
                    on_air_date_str = datetime.strftime(date_value, '%Y/%m/%d')
        except:
            print('{} except on_air_date {}'.format(row, on_air_datetime))

        is_time_flag = True
        if time_value is not None:
            time_list = time_value.split(':')
            if on_air_date_str is None:
                print('{} on_air_date_strがNoneのため、SKIP'.format(row))
                return None, False
            else:
                if len(time_list) == 2:
                    on_air_datetime = datetime.strptime('{} {}'.format(on_air_date_str, time_value), '%Y/%m/%d %H:%M')
                else:
                    on_air_datetime = datetime.strptime(on_air_date_str, '%Y/%m/%d')
            # print('on_air_datetime {} '.format(on_air_datetime))
        else:
            on_air_datetime = datetime.strptime(on_air_date_str, '%Y/%m/%d')
            is_time_flag = False
            # print('on_air_datetime {} '.format(on_air_datetime))

        return on_air_datetime, is_time_flag

    def export(self):
        """
        「TV録画」のシートの主要な列以外の列に何が入っているかの確認用
        :return:
        """
        wb = openpyxl.load_workbook(self.excel_file)
        ws = wb['TV録画']
        # rows = ws['A540':'V570']
        rows = ws['A1':'V9263']
        program_list = self.program_dao.get_where_list()
        recorded_list = self.recorded_dao.get_where_list()
        for row_idx, row in enumerate(rows):

            if row_idx == 0:
                continue

            if row[0].value is None:
                print('diskNoがないためSKIP')
                continue
            tv_data = TvRecordedData()
            program_id = self.__check_program_id(7, row)

            tv_data.channelNo = program_id // 1000
            tv_data.channelSeq = program_id % 1000
            tv_data.diskNo = row[0].value
            tv_data.seqNo = row[1].value
            tv_data.ripStatus = tv_data.get_rip_status(row[2].value, row[4].value)
            tv_data.onAirDate = row[3].value
            tv_data.timeFlag = False
            tv_data.timeStr = row[12].value
            tv_data.minute = self.__get_minute(tv_data.timeStr)
            tv_data.detail = row[10].value
            tv_data.source = 'excel'

            # result_exist = self.recorded_dao.is_exist(tv_data.diskNo, tv_data.seqNo)

            # if result_exist:
            #     print('exist {} {}'.format(tv_data.diskNo, tv_data.seqNo))
            #     continue

            """
            filter_list = list(filter(lambda program_data:
                                      program_data.channelNo == tv_data.channelNo
                                      and program_data.channelSeq == tv_data.channelSeq, program_list))

            if len(filter_list) == 1:
                tv_data.programName = filter_list[0].name
                tv_data.print()
            elif program_id == -1:
                print('not found program id {} {}'.format(program_id, row[0]))
            else:
                print('{} channelNo/seq {}/{}'.format(len(filter_list), tv_data.channelNo, tv_data.channelSeq))
                break
            """

            filter_list = list(filter(lambda recorded_data:
                                      recorded_data.diskNo == str(tv_data.diskNo)
                                      and recorded_data.seqNo == str(tv_data.seqNo), recorded_list))

            if len(filter_list) == 1:
                is_equal, remark = tv_data.get_update_column(filter_list[0])
                if is_equal is False:
                    tv_data.id = filter_list[0].id
                    tv_data.remark = remark
                    self.recorded_dao.update_all(tv_data)
                    print('update target {} {} [{}]'.format(tv_data.diskNo, tv_data.seqNo, remark))
                # else:
                #     print('same data {} {}'.format(tv_data.diskNo, tv_data.seqNo))
            else:
                self.recorded_dao.export(tv_data)
                print('register target {} {}'.format(tv_data.diskNo, tv_data.seqNo))

    def export2(self, sheet_name: str = ''):
        """
        「TV録画2」のシートの主要な列以外の列に何が入っているかの確認用
        :return:
        """

        if len(sheet_name) <= 0:
            return

        wb = openpyxl.load_workbook(self.excel_file)
        ws = wb[sheet_name]
        max_row = ws.max_row + 1
        # max_row = 10
        rows = ws['A2':'J{}'.format(max_row)]
        # rows = ws['A645':'J660']
        # rows = ws['A1':'V9263']
        # recorded_list = self.recorded_dao.get_where_list('WHERE created_at > "2020-08-01"')
        recorded_list = self.recorded_dao.get_where_list()

        # program_list = self.program_dao.get_where_list()
        for row_idx, row in enumerate(rows):

            if row_idx == 0:
                if row[0].value == 'Disk No':
                    continue

            if row[0].value is None:
                if row[1].value is None or row[3].value is None:
                    print('diskNo ( seqNo & onAirDate ) がないためSKIP {}'.format(str(row[0])))
                    continue
                else:
                    disk_no = before_disk_no
            else:
                disk_no = str(row[0].value)

            tv_data = TvRecordedData()
            program_id = self.__check_program_id(5, row)

            tv_data.channelNo = program_id // 1000
            tv_data.channelSeq = program_id % 1000
            tv_data.diskNo = disk_no
            tv_data.seqNo = str(row[1].value)
            tv_data.ripStatus = tv_data.get_rip_status(row[2].value, '')
            tv_data.onAirDate, tv_data.timeFlag = self.__get_on_air_datetime(row, 3, 7)
            tv_data.timeStr = row[8].value
            tv_data.minute = self.__get_minute(tv_data.timeStr)
            tv_data.detail = row[9].value
            before_disk_no = tv_data.diskNo

            tv_data.source = 'excel'

            filter_list = list(filter(lambda recorded_data:
                                      recorded_data.diskNo == tv_data.diskNo
                                      and recorded_data.seqNo == tv_data.seqNo, recorded_list))

            if len(filter_list) == 1:
                is_equal, remark = tv_data.get_update_column(filter_list[0])
                if is_equal is False:
                    tv_data.id = filter_list[0].id
                    tv_data.remark = remark
                    print('update target {} {} [{}]'.format(tv_data.diskNo, tv_data.seqNo, remark))
                    if self.is_check is False:
                        self.recorded_dao.update_all(tv_data)
                # else:
                #     print('same data {} {}'.format(tv_data.diskNo, tv_data.seqNo))
            else:
                print('register target {} {}'.format(tv_data.diskNo, tv_data.seqNo))
                if self.is_check is False:
                    self.recorded_dao.export(tv_data)


if __name__ == '__main__':
    tv_contents_register = TvContentsRegister()
    # tv_contents_register.export()
    tv_contents_register.export2('TV録画2')
    # tv_contents_register.export2('0001-1114')
    tv_contents_register.export2('ZIP')
    tv_contents_register.export2('2030')
