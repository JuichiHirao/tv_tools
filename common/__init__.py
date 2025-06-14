import re
from db import TvDiskDao


class RecordedTool:
    def __init__(self, logger):
        self.logger = logger
        pass

    def get_disk_no_label(self, disk_label: str = '', disk_dao: TvDiskDao = None):
        disk_label = '' if disk_label is None else disk_label
        m_recorded = re.fullmatch('(?P<disk_no>[0-9]{4}).*', disk_label)
        if m_recorded:
            disk_no = int(m_recorded.group('disk_no'))
            result_list = disk_dao.get_where_list('WHERE no = %s', [disk_no])
            if len(result_list) != 1:
                message = f'tv.diskテーブルに一致するnoが存在しない label [{disk_label}]'
                self.logger.error(message)
                # raise Exception(f'tv.diskテーブルに一致するnoが存在しない label [{disk_label}]')
        else:
            disk_no = -1

        return disk_no

class DiskTool:
    def __init__(self, logger):
        self.logger = logger
        pass

    def get_path(self, disk_no: int):
        if 1 <= disk_no <= 268:
            disk_path = 'J:\\BDR-Backup'
        elif 269 <= disk_no <= 530:
            disk_path = 'K:\\BDR-Backup'
        elif 531 <= disk_no <= 785:
            disk_path = 'I:\\BDR-Backup'
        elif 786 <= disk_no <= 1022:
            disk_path = 'M:\\BDR-Backup'
        elif 1023 <= disk_no <= 1275:
            disk_path = 'N:\\BDR-Backup'
        elif 1276 <= disk_no <= 1531:
            disk_path = 'O:\\BDR-Backup'
        elif 1532 <= disk_no <= 1780:
            disk_path = 'P:\\BDR-Backup'
        elif 1781 <= disk_no <= 2113:
            disk_path = 'Q:\\BDR-Backup'
        elif 2114 <= disk_no <= 2443:
            disk_path = 'R:\\BDR-Backup'
        elif 2444 <= disk_no <= 2775:
            disk_path = 'V:\\BDR-Backup'
        else:
            disk_path = 'U:\\BDR-Backup'

        return disk_path

if __name__ == '__main__':
    tv_recorded_tool = RecordedTool()
    disk_dao = TvDiskDao()
    disk_no = tv_recorded_tool.get_disk_no_label('RE0001', disk_dao)
    print(f'disk no [{disk_no}]')
    disk_no = tv_recorded_tool.get_disk_no_label('2700 2030', disk_dao)
    print(f'disk no [{disk_no}]')
    disk_no = tv_recorded_tool.get_disk_no_label('2701_2030', disk_dao)
    print(f'disk no [{disk_no}]')
    disk_no = tv_recorded_tool.get_disk_no_label('2702 4X6', disk_dao)
    print(f'disk no [{disk_no}]')
