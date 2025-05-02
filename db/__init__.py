import yaml
import mysql.connector
from data import TvRecordedData
from data import TvProgramData
from data import TvFileData
from data import TvChannelData
from data import TvDisk
from data import TvStoreData


class MysqlBase:

    def __init__(self, table_name='', dbname=''):
        self.max_time = 0
        self.user = ''
        self.password = ''
        self.hostname = ''
        self.dbname = ''
        self.cursor = None

        self.conn = self.get_conn()

        # テーブル名が指定されていた場合は取得済みの回数を設定
        if len(table_name) > 0:
            self.table_name = table_name
            max_time = self.db.prepare("SELECT max(times) FROM " + table_name)
            for row in max_time():
                self.max_time = int(row[0])

        if len(dbname) > 0:
            self.dbname = dbname

        self.cursor = self.conn.cursor()

    def get_conn(self):

        with open('credentials.yml') as file:
            obj = yaml.load(file, Loader=yaml.FullLoader)
            self.user = obj['user']
            self.password = obj['password']
            self.hostname = obj['hostname']
            if len(self.dbname) <= 0:
                self.dbname = obj['dbname']

        return mysql.connector.connect(user=self.user, password=self.password,
                                       host=self.hostname, database=self.dbname)


class TvFileDao(MysqlBase):

    def get_dir_id(self, path: str = ''):
        sql = 'SELECT id FROM tv.real_dir WHERE path = %s '

        self.cursor.execute(sql, (path,))

        rs = self.cursor.fetchall()

        for row in rs:
            return row[0]

        return -1

    def get_where_list(self, where_sql: str = '', param_list: list = []):

        sql = 'SELECT id' \
              '  , contents_id, detail_id, store_id, label ' \
              '  , `name`, source, duration, `time` ' \
              '  , video_info, comment, `size`, priority_num ' \
              '  , file_date, file_status,quality, remark ' \
              '  , rating1, rating2 ' \
              '  , created_at, updated_at ' \
              '  FROM tv.file '

        if len(where_sql) > 0:
            sql = '{} {}'.format(sql, where_sql)
            self.cursor.execute(sql, param_list)
        else:
            self.cursor.execute(sql)

        rs = self.cursor.fetchall()

        data_list = []
        for row in rs:
            data = TvFileData()
            data.id = row[0]
            data.contentsId = row[1]
            data.detailId = row[2]
            data.storeId = row[3]
            data.label = row[4]
            data.name = row[5]
            data.source = row[6]
            data.duration = row[7]
            data.time = row[8]
            data.videoInfo = row[9]
            data.comment = row[10]
            data.size = row[11]
            data.priorityNUmber = row[12]
            data.fileDate = row[13]
            data.fileStatus = row[14]
            data.quality = row[15]
            data.remark = row[16]
            data.rating1 = row[17]
            data.rating2 = row[18]
            data.createdAt = row[19]
            data.updatedAt = row[20]

            data_list.append(data)

        return data_list

    def is_exist(self, filename: str = ''):

        sql = 'SELECT id FROM tv.file WHERE name = %s '

        self.cursor.execute(sql, (filename,))

        rs = self.cursor.fetchall()

        for row in rs:
            return True

        return False

    def update_time(self, file_data: TvFileData = None):

        if file_data is None:
            return

        sql = 'UPDATE tv.file ' \
              '  SET time = %s ' \
              '  WHERE id = %s '

        self.cursor.execute(sql, (file_data.time, file_data.id))

        self.conn.commit()

    def export(self, file_data: TvFileData = None):

        if file_data is None:
            return

        sql = 'INSERT INTO tv.file (store_id' \
              '  , label, `name`, source, duration ' \
              '  , `time`, video_info, comment, `size` ' \
              '  , file_date, file_status ' \
              '  ) ' \
              ' VALUES(%s ' \
              '  , %s, %s, %s, %s' \
              '  , %s, %s, %s, %s' \
              '  , %s, %s ' \
              ' )'

        self.cursor.execute(sql, (file_data.storeId
                                  , file_data.label, file_data.name, file_data.source, file_data.duration
                                  , file_data.time, file_data.videoInfo, file_data.comment, file_data.size
                                  , file_data.fileDate, file_data.fileStatus)
                            )

        self.conn.commit()


class TvChannelDao(MysqlBase):

    def clear_table(self):
        sql = """
        drop table tv.channel
        """
        self.cursor.execute(sql)

        self.conn.commit()

        sql = """
        create table tv.channel
        (
            id mediumint auto_increment
                primary key,
            channel_no int null,
            type varchar(128) null,
            name text null,
            rip_id varchar(64) null,
            start_date datetime null,
            end_date datetime null,
            video varchar(255) null,
            voice varchar(255) null,
            rate varchar(128) null,
            detail text null,
            created_at timestamp default CURRENT_TIMESTAMP null,
            updated_at timestamp null on update CURRENT_TIMESTAMP
        );
        """

        self.cursor.execute(sql)

        self.conn.commit()

    def get_where_list(self, where_sql: str = '', param_list: list = []):

        sql = 'SELECT id' \
              '  , contents_id, detail_id, store_id, label ' \
              '  , `name`, source, duration, `time` ' \
              '  , video_info, comment, `size`, priority_num ' \
              '  , file_date, file_status,quality, remark ' \
              '  , rating1, rating2 ' \
              '  , created_at, updated_at ' \
              '  FROM tv.file '

        if len(where_sql) > 0:
            sql = '{} {}'.format(sql, where_sql)
            self.cursor.execute(sql, param_list)
        else:
            self.cursor.execute(sql)

        rs = self.cursor.fetchall()

        data_list = []
        for row in rs:
            data = TvProgramData()
            data.id = row[0]
            data.contentsId = row[1]
            data.detailId = row[2]
            data.storeId = row[3]
            data.label = row[4]
            data.name = row[5]
            data.source = row[6]
            data.duration = row[7]
            data.time = row[8]
            data.videoInfo = row[9]
            data.comment = row[10]
            data.size = row[11]
            data.priorityNUmber = row[12]
            data.fileDate = row[13]
            data.fileStatus = row[14]
            data.quality = row[15]
            data.remark = row[16]
            data.rating1 = row[17]
            data.rating2 = row[18]
            data.createdAt = row[19]
            data.updatedAt = row[20]

            data_list.append(data)

        return data_list

    def is_exist(self, channel_no: int = 0):

        sql = 'SELECT channel_no FROM tv.channel WHERE cnannel_no = %s '

        self.cursor.execute(sql, (channel_no,))

        rs = self.cursor.fetchall()

        for row in rs:
            return True

        return False

    def export(self, channel_data: TvChannelData = None):

        if channel_data is None:
            return

        sql = 'INSERT INTO tv.channel (channel_no' \
              '  , `type`, `name`, rip_id, start_date' \
              '  , end_date, video, voice, rate ' \
              '  , detail ' \
              '  ) ' \
              ' VALUES(%s ' \
              '  , %s, %s, %s, %s' \
              '  , %s, %s, %s, %s' \
              '  , %s ' \
              ' )'

        self.cursor.execute(sql, (channel_data.channel_no
                                  , channel_data.type, channel_data.name, channel_data.ripId, channel_data.startDate
                                  , channel_data.endDate, channel_data.video, channel_data.voice, channel_data.rate
                                  , channel_data.detail)
                            )

        self.conn.commit()


class TvDao(MysqlBase):

    def get_dir_id(self, path: str = ''):
        sql = 'SELECT id FROM tv.real_dir WHERE path = %s '

        self.cursor.execute(sql, (path,))

        rs = self.cursor.fetchall()

        for row in rs:
            return row[0]

        return -1

    def get_where_list(self, where_sql: str = '', param_list: list = []):

        sql = 'SELECT id' \
              '  , contents_id, detail_id, store_id, label ' \
              '  , `name`, source, duration, `time` ' \
              '  , video_info, comment, `size`, priority_num ' \
              '  , file_date, file_status,quality, remark ' \
              '  , rating1, rating2 ' \
              '  , created_at, updated_at ' \
              '  FROM tv.file '

        if len(where_sql) > 0:
            sql = '{} {}'.format(sql, where_sql)
            self.cursor.execute(sql, param_list)
        else:
            self.cursor.execute(sql)

        rs = self.cursor.fetchall()

        data_list = []
        for row in rs:
            data = TvProgramData()
            data.id = row[0]
            data.contentsId = row[1]
            data.detailId = row[2]
            data.storeId = row[3]
            data.label = row[4]
            data.name = row[5]
            data.source = row[6]
            data.duration = row[7]
            data.time = row[8]
            data.videoInfo = row[9]
            data.comment = row[10]
            data.size = row[11]
            data.priorityNUmber = row[12]
            data.fileDate = row[13]
            data.fileStatus = row[14]
            data.quality = row[15]
            data.remark = row[16]
            data.rating1 = row[17]
            data.rating2 = row[18]
            data.createdAt = row[19]
            data.updatedAt = row[20]

            data_list.append(data)

        return data_list

    def is_exist(self, channel_no: int = 0):

        sql = 'SELECT channel_no FROM tv.channel WHERE cnannel_no = %s '

        self.cursor.execute(sql, (channel_no,))

        rs = self.cursor.fetchall()

        for row in rs:
            return True

        return False

    def export(self, channel_data: TvChannelData = None):

        if channel_data is None:
            return

        sql = 'INSERT INTO tv.channel (channel_no' \
              '  , `type`, `name`, rip_id, start_date' \
              '  , end_date, video, voice, rate ' \
              '  , detail ' \
              '  ) ' \
              ' VALUES(%s ' \
              '  , %s, %s, %s, %s' \
              '  , %s, %s, %s, %s' \
              '  , %s ' \
              ' )'

        self.cursor.execute(sql, (channel_data.channel_no
                                  , channel_data.type, channel_data.name, channel_data.ripId, channel_data.startDate
                                  , channel_data.endDate, channel_data.video, channel_data.voice, channel_data.rate
                                  , channel_data.detail)
                            )

        self.conn.commit()

    def export_program(self, program_data: TvProgramData = None):

        if program_data is None:
            return

        sql = 'INSERT INTO tv.program (channel_no' \
              '  , channel_seq, `name`, short_name, start_date' \
              '  , start_date_str, end_date, end_date_str, detail' \
              '  ) ' \
              ' VALUES(%s ' \
              '  , %s, %s, %s, %s' \
              '  , %s, %s, %s, %s' \
              ' )'

        self.cursor.execute(sql, (program_data.channelNo
                                  , program_data.channelSeq, program_data.name, program_data.shortName, program_data.startDate
                                  , program_data.startDateStr, program_data.endDate, program_data.endDateStr, program_data.detail
                                  )
                            )

        self.conn.commit()


class TvProgramDao(MysqlBase):

    def clear_table(self):
        sql = """
        drop table tv.program
        """
        self.cursor.execute(sql)

        self.conn.commit()

        sql = """
            create table tv.program
            (
                id mediumint auto_increment
                    primary key,
                channel_no int null,
                channel_seq int null,
                name text null,
                short_name text null,
                start_date datetime null,
                start_date_str varchar(128) null,
                end_date datetime null,
                end_date_str varchar(128) null,
                detail text null,
                created_at timestamp default CURRENT_TIMESTAMP null,
                updated_at timestamp null on update CURRENT_TIMESTAMP
            );
        """

        self.cursor.execute(sql)

        self.conn.commit()

    def get_where_list(self, where_sql: str = '', param_list: list = None):

        sql = 'SELECT id' \
              '  , channel_no, channel_seq, `name`, short_name ' \
              '  , start_date, start_date_str, end_date, end_date_str ' \
              '  , detail ' \
              '  , created_at, updated_at ' \
              '  FROM tv.program '

        if param_list is not None and len(param_list) > 0:
            sql = '{} {}'.format(sql, where_sql)
            self.cursor.execute(sql, param_list)
        else:
            self.cursor.execute(sql)

        rs = self.cursor.fetchall()

        data_list = []
        for row in rs:
            one_data = TvProgramData()
            one_data.id = row[0]
            one_data.channelNo = row[1]
            one_data.channelSeq = row[2]
            one_data.name = row[3]
            one_data.shortName = row[4]
            one_data.startDate = row[5]
            one_data.startDateStr = row[6]
            one_data.endDate = row[7]
            one_data.endDateStr = row[8]
            one_data.detail = row[9]
            one_data.createdAt = row[10]
            one_data.updatedAt = row[11]

            data_list.append(one_data)

        return data_list

    def is_exist(self, channel_no: int = 0):

        sql = 'SELECT channel_no FROM tv.channel WHERE cnannel_no = %s '

        self.cursor.execute(sql, (channel_no,))

        rs = self.cursor.fetchall()

        for row in rs:
            return True

        return False

    def get_data(self, channel_no: int = -1, channel_seq: int = -1) -> TvProgramData:

        sql = """
          SELECT id
               , channel_no, channel_seq, `name`, short_name
               , start_date, start_date_str, end_date, end_date_str
               , detail, created_at, updated_at
             FROM tv.program WHERE channel_no = %s and channel_seq = %s
        """

        self.cursor.execute(sql, (channel_no, channel_seq))

        rs = self.cursor.fetchall()

        for row in rs:
            program_data = TvProgramData()
            program_data.id = row[0]
            program_data.channelNo = row[1]
            program_data.channelSeq = row[2]
            # program_data.channelName = sheet.cell(row=row_idx, column=col_no_channel_name).value
            program_data.name = row[3]
            program_data.shortName = row[4]
            program_data.startDate = row[5]
            program_data.startDateStr = row[6]
            program_data.endDate = row[7]
            program_data.endDateStr = row[8]
            program_data.detail = row[9]
            program_data.createdAt = row[10]
            program_data.updatedAt = row[11]
            # program_data.print()

            return program_data

        return None

    def export(self, program_data: TvProgramData = None):

        if program_data is None:
            return

        sql = 'INSERT INTO tv.program (channel_no' \
              '  , channel_seq, `name`, short_name, start_date' \
              '  , start_date_str, end_date, end_date_str, detail' \
              '  ) ' \
              ' VALUES(%s ' \
              '  , %s, %s, %s, %s' \
              '  , %s, %s, %s, %s' \
              ' )'

        self.cursor.execute(sql, (program_data.channelNo
                                  , program_data.channelSeq, program_data.name, program_data.shortName, program_data.startDate
                                  , program_data.startDateStr, program_data.endDate, program_data.endDateStr, program_data.detail
                                  )
                            )

        self.conn.commit()

    def update(self, program_data: TvProgramData = None, program_id: int = -1):

        if program_data is None:
            return

        sql = """
          UPDATE tv.program
            SET
              `name` = %s 
              , short_name = %s 
              , start_date = %s 
              , start_date_str = %s 
              , end_date = %s 
              , end_date_str = %s 
              , detail = %s 
            WHERE id = %s
        """

        self.cursor.execute(sql, (program_data.name
                                  , program_data.shortName
                                  , program_data.startDate
                                  , program_data.startDateStr
                                  , program_data.endDate
                                  , program_data.endDateStr
                                  , program_data.detail
                                  , program_id))

        self.conn.commit()


class TvDiskDao(MysqlBase):

    def get_where_list(self, where_sql: str = '', param_list: list = []):

        sql = 'SELECT id' \
              '  , `no`, label, path' \
              '  , created_at, updated_at ' \
              '  FROM tv.disk '
              # '  FROM tv.disk ORDER BY `no`'

        if len(where_sql) > 0:
            sql = f'{sql} {where_sql} ORDER BY `no`'
            self.cursor.execute(sql, param_list)
        else:
            sql = f'{sql} ORDER BY `no`'
            self.cursor.execute(sql)

        rs = self.cursor.fetchall()

        data_list = []
        for row in rs:
            data = TvDisk()
            data.id = row[0]
            data.no = row[1]
            data.label = row[2]
            data.path = row[3]
            data.createdAt = row[4]
            data.updatedAt = row[5]

            data_list.append(data)

        return data_list

    def export(self, no: int = -1, label: str = '', path: str = ''):

        sql = 'INSERT INTO tv.disk(no, label, path)  VALUES(%s, %s, %s)'

        self.cursor.execute(sql, (no, label, path))

        self.conn.commit()

    def update_no(self, no: int = -1, disk_id: int = -1):

        sql = 'UPDATE tv.disk' \
              '  SET no = %s ' \
              '  WHERE id = %s '

        self.cursor.execute(sql, (no, disk_id))

        self.conn.commit()

    def update_path(self, path: str = '', disk_id: int = -1):

        sql = 'UPDATE tv.disk' \
              '  SET path = %s ' \
              '  WHERE id = %s '

        self.cursor.execute(sql, (path, disk_id))

        self.conn.commit()

    def update_label(self, label: str = '', disk_id: int = -1):

        sql = 'UPDATE tv.disk' \
              '  SET label = %s ' \
              '  WHERE id = %s '

        self.cursor.execute(sql, (label, disk_id))

        self.conn.commit()


class TvFileDao(MysqlBase):

    def get_dir_id(self, path: str = ''):
        sql = 'SELECT id FROM tv.real_dir WHERE path = %s '

        self.cursor.execute(sql, (path,))

        rs = self.cursor.fetchall()

        for row in rs:
            return row[0]

        return -1

    def get_where_list(self, where_sql: str = '', param_list: list = []):

        sql = 'SELECT id' \
              '  , contents_id, detail_id, store_id, label ' \
              '  , `name`, source, duration, `time` ' \
              '  , video_info, comment, `size`, priority_num ' \
              '  , file_date, file_status,quality, remark ' \
              '  , rating1, rating2 ' \
              '  , created_at, updated_at ' \
              '  FROM tv.file '

        if len(where_sql) > 0:
            sql = '{} {}'.format(sql, where_sql)
            self.cursor.execute(sql, param_list)
        else:
            self.cursor.execute(sql)

        rs = self.cursor.fetchall()

        data_list = []
        for row in rs:
            data = TvFileData()
            data.id = row[0]
            data.contentsId = row[1]
            data.detailId = row[2]
            data.storeId = row[3]
            data.label = row[4]
            data.name = row[5]
            data.source = row[6]
            data.duration = row[7]
            data.time = row[8]
            data.videoInfo = row[9]
            data.comment = row[10]
            data.size = row[11]
            data.priorityNUmber = row[12]
            data.fileDate = row[13]
            data.fileStatus = row[14]
            data.quality = row[15]
            data.remark = row[16]
            data.rating1 = row[17]
            data.rating2 = row[18]
            data.createdAt = row[19]
            data.updatedAt = row[20]

            data_list.append(data)

        return data_list

    def get_where_list(self, where_sql: str = '', param_list: list = []):

        sql = 'SELECT id' \
              '  , contents_id, detail_id, store_id, label ' \
              '  , `name`, source, duration, `time` ' \
              '  , video_info, comment, `size`, priority_num ' \
              '  , file_date, file_status,quality, remark ' \
              '  , rating1, rating2 ' \
              '  , created_at, updated_at ' \
              '  FROM tv.file '

        if len(where_sql) > 0:
            sql = '{} {}'.format(sql, where_sql)
            self.cursor.execute(sql, param_list)
        else:
            self.cursor.execute(sql)

        rs = self.cursor.fetchall()

        data_list = []
        for row in rs:
            data = TvFileData()
            data.id = row[0]
            data.contentsId = row[1]
            data.detailId = row[2]
            data.storeId = row[3]
            data.label = row[4]
            data.name = row[5]
            data.source = row[6]
            data.duration = row[7]
            data.time = row[8]
            data.videoInfo = row[9]
            data.comment = row[10]
            data.size = row[11]
            data.priorityNUmber = row[12]
            data.fileDate = row[13]
            data.fileStatus = row[14]
            data.quality = row[15]
            data.remark = row[16]
            data.rating1 = row[17]
            data.rating2 = row[18]
            data.createdAt = row[19]
            data.updatedAt = row[20]

            data_list.append(data)

        return data_list

    def is_exist(self, filename: str = ''):

        sql = 'SELECT id FROM tv.file WHERE name = %s '

        self.cursor.execute(sql, (filename,))

        rs = self.cursor.fetchall()

        for row in rs:
            return True

        return False

    def update_time(self, file_data: TvFileData = None):

        if file_data is None:
            return

        sql = 'UPDATE tv.file ' \
              '  SET time = %s ' \
              '  WHERE id = %s '

        self.cursor.execute(sql, (file_data.time, file_data.id))

        self.conn.commit()

    def export(self, file_data: TvFileData = None, is_check: bool = False):

        if file_data is None:
            return

        sql = 'INSERT INTO tv.file (store_id' \
              '  , label, `name`, source, duration ' \
              '  , `time`, video_info, comment, `size` ' \
              '  , file_date, file_status ' \
              '  ) ' \
              ' VALUES(%s ' \
              '  , %s, %s, %s, %s' \
              '  , %s, %s, %s, %s' \
              '  , %s, %s ' \
              ' )'

        self.cursor.execute(sql, (file_data.storeId
                                  , file_data.label, file_data.name, file_data.source, file_data.duration
                                  , file_data.time, file_data.videoInfo, file_data.comment, file_data.size
                                  , file_data.fileDate, file_data.fileStatus)
                            )

        if is_check is False:
            self.conn.commit()


class TvDao(MysqlBase):

    def get_dir_id(self, path: str = ''):
        sql = 'SELECT id FROM tv.real_dir WHERE path = %s '

        self.cursor.execute(sql, (path,))

        rs = self.cursor.fetchall()

        for row in rs:
            return row[0]

        return -1

    def get_where_list(self, where_sql: str = '', param_list: list = []):

        sql = 'SELECT id' \
              '  , contents_id, detail_id, store_id, label ' \
              '  , `name`, source, duration, `time` ' \
              '  , video_info, comment, `size`, priority_num ' \
              '  , file_date, file_status,quality, remark ' \
              '  , rating1, rating2 ' \
              '  , created_at, updated_at ' \
              '  FROM tv.file '

        if len(where_sql) > 0:
            sql = '{} {}'.format(sql, where_sql)
            self.cursor.execute(sql, param_list)
        else:
            self.cursor.execute(sql)

        rs = self.cursor.fetchall()

        data_list = []
        for row in rs:
            data = TvProgramData()
            data.id = row[0]
            data.contentsId = row[1]
            data.detailId = row[2]
            data.storeId = row[3]
            data.label = row[4]
            data.name = row[5]
            data.source = row[6]
            data.duration = row[7]
            data.time = row[8]
            data.videoInfo = row[9]
            data.comment = row[10]
            data.size = row[11]
            data.priorityNUmber = row[12]
            data.fileDate = row[13]
            data.fileStatus = row[14]
            data.quality = row[15]
            data.remark = row[16]
            data.rating1 = row[17]
            data.rating2 = row[18]
            data.createdAt = row[19]
            data.updatedAt = row[20]

            data_list.append(data)

        return data_list

    def is_exist(self, channel_no: int = 0):

        sql = 'SELECT channel_no FROM tv.channel WHERE cnannel_no = %s '

        self.cursor.execute(sql, (channel_no,))

        rs = self.cursor.fetchall()

        for row in rs:
            return True

        return False

    def export(self, channel_data: TvChannelData = None):

        if channel_data is None:
            return

        sql = 'INSERT INTO tv.channel (channel_no' \
              '  , `type`, `name`, rip_id, start_date' \
              '  , end_date, video, voice, rate ' \
              '  , detail ' \
              '  ) ' \
              ' VALUES(%s ' \
              '  , %s, %s, %s, %s' \
              '  , %s, %s, %s, %s' \
              '  , %s ' \
              ' )'

        self.cursor.execute(sql, (channel_data.channel_no
                                  , channel_data.type, channel_data.name, channel_data.ripId, channel_data.startDate
                                  , channel_data.endDate, channel_data.video, channel_data.voice, channel_data.rate
                                  , channel_data.detail)
                            )

        self.conn.commit()

    def export_program(self, program_data: TvProgramData = None):

        if program_data is None:
            return

        sql = 'INSERT INTO tv.program (channel_no' \
              '  , channel_seq, `name`, short_name, start_date' \
              '  , start_date_str, end_date, end_date_str, detail' \
              '  ) ' \
              ' VALUES(%s ' \
              '  , %s, %s, %s, %s' \
              '  , %s, %s, %s, %s' \
              ' )'

        self.cursor.execute(sql, (program_data.channelNo
                                  , program_data.channelSeq, program_data.name, program_data.shortName,
                                  program_data.startDate
                                  , program_data.startDateStr, program_data.endDate, program_data.endDateStr,
                                  program_data.detail
                                  )
                            )

        self.conn.commit()


class TvRecordedDao(MysqlBase):

    def get_distinct_disk_no(self):
        # sql = 'SELECT distinct disk_label FROM tv.recorded WHERE disk_no is null OR disk_no <= 0'
        sql = 'SELECT distinct disk_label FROM tv.recorded WHERE disk_no is null'

        self.cursor.execute(sql)
        rs = self.cursor.fetchall()

        disk_list = []
        for row in rs:
            disk_list.append(row[0])

        return disk_list

    def get_where_list(self, where_sql: str = '', param_list: list = None):

        sql = 'SELECT id' \
              '  , disk_no, disk_label, seq_no, rip_status, on_air_date ' \
              '  , time_flag, `minute`, channel_no, channel_seq' \
              '  , detail, `source`, remark ' \
              '  , created_at, updated_at ' \
              '  FROM tv.recorded '

        if len(where_sql) > 0:
            sql = '{} {}'.format(sql, where_sql)
            if param_list is None:
                self.cursor.execute(sql)
            else:
                self.cursor.execute(sql, param_list)
        else:
            self.cursor.execute(sql)

        rs = self.cursor.fetchall()

        data_list = []
        for row in rs:
            one_data = TvRecordedData()
            one_data.id = row[0]
            one_data.diskNo = row[1]
            one_data.diskLabel = row[2]
            one_data.seqNo = str(row[3])
            one_data.ripStatus = row[4]
            one_data.onAirDate = row[5]
            one_data.timeFlag = row[6]
            one_data.minute = row[7]
            one_data.channelNo = row[8]
            one_data.channelSeq = row[9]
            one_data.detail = row[10]
            one_data.source = row[11]
            one_data.remark = row[12]
            one_data.createdAt = row[13]
            one_data.updatedAt = row[14]

            data_list.append(one_data)

        return data_list

    def is_exist(self, disk_label: str = '', seq_no: str = ''):

        sql = 'SELECT channel_no FROM tv.recorded WHERE disk_label = %s and seq_no = %s '

        self.cursor.execute(sql, (disk_label, seq_no))

        rs = self.cursor.fetchall()

        for row in rs:
            return True

        return False

    def update_disk_no(self, disk_no: int = -1, disk_label: str = ''):

        if disk_no < -1 or len(disk_label) <= 0:
            return

        sql = """UPDATE tv.recorded 
                   SET disk_no = %s 
                   WHERE disk_label = %s"""

        self.cursor.execute(sql, (disk_no, disk_label))
        affected_rows = self.cursor.rowcount

        self.conn.commit()

        return affected_rows


    def update_all(self, recorded_data: TvRecordedData() = None):

        if recorded_data is None:
            return

        sql = 'UPDATE tv.recorded ' \
              '  SET ' \
              '  disk_no = %s ' \
              '  , disk_label = %s ' \
              '  , seq_no = %s ' \
              '  , rip_status = %s ' \
              '  , on_air_date = %s ' \
              '  , time_flag = %s ' \
              '  , `minute` = %s ' \
              '  , channel_no = %s ' \
              '  , channel_seq = %s ' \
              '  , detail = %s ' \
              '  , `source` = %s ' \
              '  , remark = %s ' \
              '  WHERE id = %s '

        self.cursor.execute(sql, (recorded_data.diskNo, recorded_data.diskLabel, recorded_data.seqNo, recorded_data.ripStatus, recorded_data.onAirDate
                                  , recorded_data.timeFlag, recorded_data.minute, recorded_data.channelNo, recorded_data.channelSeq
                                  , recorded_data.detail, recorded_data.source, recorded_data.remark, recorded_data.id
                                  )
                            )

        self.conn.commit()

    def export(self, recorded_data: TvRecordedData() = None):

        if recorded_data is None:
            return

        sql = 'INSERT INTO tv.recorded (' \
              '  disk_no, disk_label, seq_no, rip_status, on_air_date ' \
              '  , time_flag, `minute`, channel_no, channel_seq' \
              '  , detail, source ' \
              '  ) ' \
              ' VALUES( ' \
              '  %s, %s, %s, %s, %s' \
              '  , %s, %s, %s, %s' \
              '  , %s, %s ' \
              ' )'

        self.cursor.execute(sql, (recorded_data.diskNo, recorded_data.diskLabel, recorded_data.seqNo, recorded_data.ripStatus, recorded_data.onAirDate
                                  , recorded_data.timeFlag, recorded_data.minute, recorded_data.channelNo, recorded_data.channelSeq
                                  , recorded_data.detail, recorded_data.source
                                  )
                            )

        self.conn.commit()


class TvStoreDao(MysqlBase):

    def get_where_list(self, where_sql: str = '', param_list: list = None):

        sql = 'SELECT id' \
              '  , name, path, remark, created_at, updated_at' \
              '  FROM tv.real_dir '

        if len(where_sql) > 0:
            sql = '{} {}'.format(sql, where_sql)
            if param_list is None:
                self.cursor.execute(sql)
            else:
                self.cursor.execute(sql, param_list)
        else:
            self.cursor.execute(sql)

        rs = self.cursor.fetchall()

        data_list = []
        for row in rs:
            one_data = TvStoreData()
            one_data.id = row[0]
            one_data.name = row[1]
            one_data.path = row[2]
            one_data.remark = row[3]
            one_data.createdAt = row[4]
            one_data.updatedAt = row[5]

            data_list.append(one_data)

        return data_list

    def is_exist(self, path: str = ''):

        sql = 'SELECT id FROM tv.real_dir WHERE path = %s'

        self.cursor.execute(sql, (path, ))

        rs = self.cursor.fetchall()

        for row in rs:
            return True

        return False
