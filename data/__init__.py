from datetime import datetime
import re


class TvRecordedData:

    def __init__(self):

        self.id = -1
        self.diskNo = ''
        self.seqNo = ''
        self.ripStatus = ''
        self.onAirDate = None
        self.timeFlag = False
        self.channelNo = -1
        self.channelSeq = -1
        self.minute = 0
        self.channelStr = ''
        self.programName = ''
        self.timeStr = ''
        self.detail = ''
        self.remark = ''
        self.createdAt = None
        self.updatedAt = None

    def get_update_column(self, recorded_data):
        # recorded_data = TvRecordedData()
        is_equal = True
        remark = ''
        now_date_str = datetime.strftime(datetime.now(), '%Y-%m-%d')
        if self.ripStatus != recorded_data.ripStatus:
            remark = 'rip [{}] <- [{}]'.format(self.ripStatus, recorded_data.ripStatus)
            is_equal = False
        if self.onAirDate != recorded_data.onAirDate:
            remark = '{}, onAir [{}] <- [{}]'.format(remark, self.onAirDate, recorded_data.onAirDate)
            is_equal = False
        if self.minute != recorded_data.minute:
            remark = '{}, min [{}] <- [{}]'.format(remark, self.minute, recorded_data.minute)
            is_equal = False
        if self.channelNo != recorded_data.channelNo:
            remark = '{}, chNo [{}] <- [{}]'.format(remark, self.channelNo, recorded_data.channelNo)
            is_equal = False
        if self.channelSeq != recorded_data.channelSeq:
            remark = '{}, chSeq [{}] <- [{}]'.format(remark, self.channelSeq, recorded_data.channelSeq)
            is_equal = False
        if self.detail != recorded_data.detail:
            remark = '{}, detail'.format(remark, self.detail, recorded_data.detail)
            print('detail')
            is_equal = False

        if is_equal is False:
            re_remark = re.sub('^, ', '', remark.strip())
            if recorded_data.remark is None or len(recorded_data.remark.strip()) <= 0:
                remark = '{} {}'.format(now_date_str, re_remark)
            else:
                remark = '{} {}、{}'.format(now_date_str, re_remark, recorded_data.remark)
                remark = re.sub('、$', '', remark.strip())

        return is_equal, remark

    def get_rip_status(self, rip_status1, rip_status2):
        if rip_status1 is None and rip_status2 is None:
            return ''
        elif rip_status1 is None:
            return rip_status2
        elif rip_status2 is None:
            return rip_status1
        else:
            return '{} {}'.format(rip_status2, rip_status1).strip()

    def print(self):
        if self.onAirDate is None:
            print('【{}】 {} {} {}'.format(self.onAirDate
                                         , str(self.channelNo).zfill(3)
                                         , str(self.channelSeq).zfill(3)
                                         , self.programName))
        else:
            date_str = ''
            if self.onAirDate.hour > 0:
                date_str = datetime.strftime(self.onAirDate, '%Y-%m-%d %H:%M')
            else:
                date_str = datetime.strftime(self.onAirDate, '%Y-%m-%d')

            print('【{}】 {} {} {}'.format(date_str
                                         , str(self.channelNo).zfill(3)
                                         , str(self.channelSeq).zfill(3)
                                         , self.programName))

        # print('  {} {} {} '.format(str(self.channelNo).zfill(3), str(self.channelSeq).zfill(3), self.programName))
        print('  diskNo    [{}] [{}]'.format(self.diskNo, self.seqNo))
        print('  rip       [{}]'.format(self.ripStatus))
        print('  time(min) [{}] <-- [{}]'.format(self.minute, self.timeStr))
        print('  detail    [{}]'.format(self.detail))


class TvFileData:

    def __init__(self):

        self.id = -1
        self.contentsId = -1
        self.detailId = -1
        self.storeId = -1
        self.label = ''
        self.name = ''
        self.source = ''
        self.duration = 0
        self.time = ''
        self.videoInfo = ''
        self.comment = ''
        self.size = 0
        self.priorityNUmber = 0
        self.fileDate = None
        self.fileStatus = 'exist'
        self.quality = 0
        self.remark = ''
        self.rating1 = 0
        self.rating2 = 0
        self.createdAt = None
        self.updatedAt = None

    def set_time(self):

        hour = 0
        min = 0
        sec = 0
        if self.duration <= 0:
            return
        hour = self.duration // 3600
        min = self.duration // 60
        sec = self.duration % 60

        time_str = ''
        if hour > 0:
            time_str = '{}h'.format(hour)
        if min > 0:
            time_str = '{}{}m'.format(time_str, min)

        time_str = '{}{}s'.format(time_str, str(sec).zfill(2))

        self.time = time_str
        return


    def print(self):
        print('【{}】 '.format(self.name))
        print('  id {} c_id {} store_id {}'.format(self.id, self.contentsId, self.storeId))
        print('  label {}'.format(self.label))
        print('  source [{}] duration [{}]->[{}]'.format(self.source, self.duration, self.time))
        print('  v_info {} quality {}'.format(self.videoInfo, self.quality))
        print('  size {}'.format(self.size))
        print('  file_date {}, file_status {}'.format(self.fileDate, self.fileStatus))
        print('  r1 {} r2 {}'.format(self.rating1, self.rating2))
        print('  comment {}'.format(self.comment))
        print('  createdAt {}  updatedAt {}'.format(self.createdAt, self.updatedAt))


class TvChannelData:

    def __init__(self):
        self.id = -1
        self.channel_no = -1
        self.type = ''
        self.name = ''
        self.ripId = ''
        self.startDate = None
        self.endDate = None
        self.video = ''
        self.voice = ''
        self.rate = ''
        self.detail = ''
        self.createdAt = None
        self.updatedAt = None

    def print(self):
        print('{} 【{}】 {}'.format(self.channel_no, self.name, self.id))
        print('    {} '.format(self.type))
        print('    {} '.format(self.name))
        print('    {} '.format(self.ripId))
        print('    {} - {}'.format(self.startDate, self.endDate))
        print('    {} '.format(self.video))
        print('    {} '.format(self.voice))
        print('    {} '.format(self.rate))
        print('    {} '.format(self.detail))


class TvProgramData:

    def __init__(self):

        self.id = -1
        self.channelNo = -1
        self.channelSeq = -1
        self.channelName = ''
        self.name = ''
        self.shortName = ''
        self.startDate = None
        self.startDateStr = ''
        self.endDate = None
        self.endDateStr = ''
        self.detail = ''
        self.createdAt = None
        self.updatedAt = None

    def set_date(self, start_date, end_date):

        try:
            if start_date is not None:
                if type(start_date) is not datetime:
                    self.startDate = datetime.strptime(start_date, '%Y/%m/%d')
                else:
                    self.startDate = start_date
        except:
            print('except start_date {}'.format(start_date))
            self.startDateStr = start_date

        try:
            if end_date is not None:
                if type(end_date) is not datetime:
                    self.endDate = datetime.strptime(end_date, '%Y/%m/%d')
                else:
                    self.endDate = end_date
        except:
            print('except end_date {}'.format(end_date))
            self.endDateStr = end_date

        return

    def print(self):
        print('{} {} 【{}】 '.format(str(self.channelNo).zfill(3), str(self.channelSeq).zfill(3), self.name))
        print('  {}'.format(self.channelName))
        print('  {}'.format(self.shortName))

        if self.startDate is None:
            print('  start {} [{}]'.format(self.startDate, self.startDateStr))
        else:
            print('  start {} [{}]'.format(datetime.strftime(self.startDate, '%Y-%m-%d'), self.startDateStr))

        if self.endDate is None:
            print('  end   {} [{}]'.format(self.endDate, self.endDateStr))
        else:
            print('  end   {} [{}]'.format(datetime.strftime(self.endDate, '%Y-%m-%d'), self.endDateStr))

        print('  {}'.format(self.detail))
        print('  createdAt {}  updatedAt {}'.format(self.createdAt, self.updatedAt))
