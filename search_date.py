import sys
from db import TvRecordedDao, TvProgramDao
from datetime import datetime, timedelta
from logging import getLogger, DEBUG, Formatter, FileHandler, StreamHandler


str_date = datetime.now().strftime('%Y%m%d')
logger = getLogger("logger")
logger.setLevel(DEBUG)

handler_stream = StreamHandler(sys.stdout)
handler_stream.setFormatter(Formatter("%(message)s"))
logger.addHandler(handler_stream)


class TvContentsSearch:

    def __init__(self, param_date_str: str = ''):
        # self.tv_file_dao = TvFileDao()
        self.tv_recorded_dao = TvRecordedDao()
        self.tv_program_dao = TvProgramDao()

        self.search_date = datetime.strptime(param_date_str, '%Y-%m-%d')

    def get_channel_list(self, channel_no, channel_seq):

        program_list = self.tv_program_dao.get_where_list('WHERE channel_no = %s AND channel_seq = %s'
                                                            , [channel_no, channel_seq])

        return program_list

    def get_list(self):

        from_search_date = self.search_date
        to_search_date = timedelta(days=1) + self.search_date

        recorded_list = self.tv_recorded_dao.get_where_list('WHERE on_air_date >= %s AND on_air_date < %s' , [from_search_date, to_search_date])

        for recorded_data in recorded_list:
            channel_list = self.get_channel_list(recorded_data.channelNo, recorded_data.channelSeq)
            if channel_list is None or len(channel_list) <= 0:
                logger.info(recorded_data.print())
            else:
                logger.info(f'【{recorded_data.onAirDate}】 {recorded_data.channelNo} {recorded_data.channelSeq} {channel_list[0].name}')
                # logger.info(f'    {recorded_data.detail}')

        return


if __name__ == '__main__':

    if len(sys.argv) < 2:
        logger.info('param1 date(yyyy-mm-dd)')

        exit(0)

    tv_contents_search = TvContentsSearch(sys.argv[1])
    tv_contents_search.get_list()
