import sys
import traceback
import re
from db import TvRecordedDao
from db import TvDiskDao
from data import TvRecordedData
from datetime import datetime
from logging import getLogger, DEBUG, Formatter, FileHandler, StreamHandler

str_date = datetime.now().strftime('%Y%m%d')
logger = getLogger("logger")
logger.setLevel(DEBUG)

log_filename = 'log\\tool_recorded_disk_{}.log'.format(str_date)
handler_file = FileHandler(filename=log_filename, encoding='utf-8')
handler_file.setFormatter(Formatter("%(asctime)s %(levelname)4s %(message)s"))
logger.addHandler(handler_file)
handler_stream = StreamHandler(sys.stdout)
handler_stream.setFormatter(Formatter("%(asctime)s %(levelname)8s %(message)s"))
logger.addHandler(handler_stream)

class TvRecordedDiskArrange:

    def __init__(self):
        self.recorded_dao = TvRecordedDao()
        self.tv_disk_dao = TvDiskDao()
        # self.base_dir = 'F:\\TVREC'

        # self.is_check = True
        self.is_check = False

    def get_disk_no(self, disk_label: str = ''):

        m_recorded = re.search('^[0-9]{4}', disk_label)
        disk_no = -1
        if m_recorded:
            try:
                disk_no = int(m_recorded.group())
            except Exception as e:
                logger.error(f'label[{disk_label}]からm_recorded一致で取得しているのにException {e}')
                sys.exit(-1)
        else:
            m_recorded = re.search('^[0-9]{3}', disk_label)
            if m_recorded:
                try:
                    disk_no = int(m_recorded.group())
                except Exception as e:
                    logger.error(f'label[{disk_label}]からm_recorded一致で取得しているのにException {e}')
                    sys.exit(-1)
            else:
                m_recorded = re.fullmatch('[0-9]{1,2}', disk_label)
                if m_recorded:
                    disk_no = int(disk_label)

        if disk_no <= 0:
            # m_date = re.search('(?P<ura_date>[0-1][0-9][0-3][0-9][0-2][0-9])_[0-9]{3}', title)
            m_recorded = re.fullmatch('(?P<disk_no>[0-9]{2})F.*', disk_label)
            if m_recorded:
                disk_no = int(m_recorded.group('disk_no'))
            else:
                logger.error(f'label[{disk_label}]からm_recorded"(?P<disk_no>[0-9]{2})F.*"が一致しない')
                return -1

        if disk_no > 0:
            result_list = self.tv_disk_dao.get_where_list('WHERE no = %s', [disk_no])
            if len(result_list) != 1:
                logger.error(f'disk_no[{disk_no}]に一致するデータがtv.diskに存在しない label [{disk_label}]')
                return -1
                # sys.exit(-1)
        else:
            logger.error(f'label[{disk_label}]からdisk_noを取得できない')
            sys.exit(-1)

        return disk_no

    def execute(self):
        """
        recorded.diskを数字だけにするための確認
        """

        disk_list = self.recorded_dao.get_distinct_disk_no()
        logger.info(f'disk_list {len(disk_list)} {disk_list}')

        for idx, disk_label in enumerate(disk_list):
            disk_no = self.get_disk_no(disk_label)
            if disk_no < 0:
                logger.error(f'[{idx}] label[{disk_label}]')
                continue

            affected_rows = 0
            # affected_rows = self.recorded_dao.update_disk_no(disk_no, disk_label)
            logger.info(f'  [{disk_label}:{disk_no}] 反映行 [{affected_rows}]')

        return


if __name__ == '__main__':
    tv_recorded_arrange = TvRecordedDiskArrange()
    tv_recorded_arrange.execute()
