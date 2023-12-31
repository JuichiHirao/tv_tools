import openpyxl
import sys
from db import TvProgramDao
from data import TvProgramData
from datetime import datetime
from logging import getLogger, DEBUG, Formatter, FileHandler, StreamHandler

str_date = datetime.now().strftime('%Y%m%d')
logger = getLogger("logger")
logger.setLevel(DEBUG)

log_filename = 'log\\tv_program_{}.log'.format(str_date)
handler_file = FileHandler(filename=log_filename, encoding='utf-8')
handler_file.setFormatter(Formatter("%(asctime)s %(levelname)4s %(message)s"))
logger.addHandler(handler_file)
handler_stream = StreamHandler(sys.stdout)
handler_stream.setFormatter(Formatter("%(asctime)s %(levelname)8s %(message)s"))
logger.addHandler(handler_stream)


class TvProgramRegister:

    def __init__(self):
        self.program_dao = TvProgramDao()
        self.excel_file = 'C:\\Users\\JuichiHirao\\Dropbox\\jhdata\\Interest\\BD番組録画.xlsx'

        # self.is_clear = True
        self.is_clear = False

        self.is_check = True
        # self.is_check = False

    def export(self):

        if self.is_clear:
            self.program_dao.clear_table()

        col_no_number = 1
        col_no_channel_name = 2 # CHANNELシートのVLOOKUP
        col_no_name = 3
        col_no_short_name = 4
        col_no_start_date = 5
        col_no_end_date = 6
        col_no_detail = 7
        wb = openpyxl.load_workbook(self.excel_file)
        sheet = wb['番組名']
        max_row = sheet.max_row + 1
        # rows = sheet['A1':'G4000']
        for row_idx in range(1, max_row):
            program_number = sheet.cell(row=row_idx, column=col_no_number).value
            if program_number is None or type(program_number) is not int:
                logger.warning(f'cell_value is None or not int {row_idx} {program_number}')
                continue

            program_data = TvProgramData()
            program_data.channelNo = program_number // 1000
            program_data.channelSeq = program_number % 1000
            # program_data.channelName = sheet.cell(row=row_idx, column=col_no_channel_name).value
            program_data.name = sheet.cell(row=row_idx, column=col_no_name).value
            program_data.shortName = sheet.cell(row=row_idx, column=col_no_short_name).value
            start_date = sheet.cell(row=row_idx, column=col_no_start_date).value
            end_date = sheet.cell(row=row_idx, column=col_no_end_date).value
            program_data.set_date(start_date, end_date)
            program_data.detail = sheet.cell(row=row_idx, column=col_no_detail).value
            # program_data.print()

            exist_data = self.program_dao.get_data(program_data.channelNo, program_data.channelSeq)
            if exist_data is not None:
                # logger.info(f'program_data is exist {program_data.channelNo} {program_data.channelSeq}')
                # exist_data.log_output(logger)
                pass
            else:
                logger.info(f'not exist register target program_data {program_data.channelNo} {program_data.channelSeq}')
                self.program_dao.export(program_data)

            # if row_idx > 10:
            #     break

        return


if __name__ == '__main__':
    tv_program_register = TvProgramRegister()
    tv_program_register.export()

