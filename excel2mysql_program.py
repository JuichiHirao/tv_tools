import openpyxl
from db import TvProgramDao
from data import TvProgramData


class TvProgramRegister:

    def __init__(self):
        self.program_dao = TvProgramDao()
        self.excel_file = 'C:\\Users\\JuichiHirao\\Dropbox\\jhdata\\Interest\\BD番組録画.xlsx'

        self.is_clear = True
        # self.is_clear = False

        self.is_check = True
        # self.is_check = False

    def export(self):

        if self.is_clear:
            self.program_dao.clear_table()

        wb = openpyxl.load_workbook(self.excel_file)
        ws = wb['番組名']
        rows = ws['A1':'G3000']
        for row_idx, row in enumerate(rows):
            if row_idx == 0:
                continue
            cell_value = row[0].value
            if cell_value is None or type(cell_value) is not int:
                continue

            if row[2] is None:
                continue

            program_data = TvProgramData()
            program_data.channelNo = cell_value // 1000
            program_data.channelSeq = cell_value % 1000
            program_data.channelName = row[1].value
            program_data.name = row[2].value
            program_data.shortName = row[3].value
            program_data.set_date(row[4].value, row[5].value)
            program_data.detail = row[6].value

            self.program_dao.export(program_data)
            program_data.print()


if __name__ == '__main__':
    tv_program_register = TvProgramRegister()
    tv_program_register.export()

