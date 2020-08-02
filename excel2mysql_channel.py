import openpyxl
from db import TvChannelDao
from data import TvChannelData


class TvChannelRegister:

    def __init__(self):
        self.channel_dao = TvChannelDao()
        self.excel_file = 'C:\\Users\\JuichiHirao\\Dropbox\\jhdata\\Interest\\BD番組録画.xlsx'
        # self.base_dir = 'F:\\TVREC'

        self.is_clear = True
        # self.is_clear = False
        self.is_check = True
        # self.is_check = False

    def export(self):

        if self.is_clear:
            self.channel_dao.clear_table()

        wb = openpyxl.load_workbook(self.excel_file)
        ws = wb['CHANNEL']
        rows = ws['A1':'J100']
        for row_idx, row in enumerate(rows):
            if row_idx == 0:
                continue
            cell_value = row[0].value
            if cell_value is None or type(cell_value) is not int:
                continue

            channel_data = TvChannelData()
            channel_data.channel_no = cell_value
            channel_data.type = row[1].value
            channel_data.name = row[2].value
            channel_data.ripId = row[3].value
            channel_data.startDate = row[4].value
            channel_data.endDate = row[5].value
            channel_data.video = row[6].value
            channel_data.voice = row[7].value
            channel_data.rate = row[8].value
            channel_data.detail = row[9].value
            self.channel_dao.export(channel_data)
            # data.print()


if __name__ == '__main__':
    tv_channel_register = TvChannelRegister()
    tv_channel_register.export()
