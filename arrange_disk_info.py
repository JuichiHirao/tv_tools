from db import TvRecordedDao


class ArrangeDiskInfo:
    def __init__(self):
        self.recorded_dao = TvRecordedDao()

        # self.disk_name = disk_name
        # self.disk_size = disk_size
        # self.disk_free_size = disk_free_size
        recorded_list = self.recorded_dao.get_where_list('WHERE disk_no LIKE %s', ['%RE'])
        disk_no_list = [recorded.diskNo for recorded in recorded_list]
        print(len(recorded_list))
        uniq_disk_no_list = list(set(disk_no_list))
        print(len(uniq_disk_no_list))
        print(uniq_disk_no_list)
        edit_disk_no_list = []
        for disk_no in uniq_disk_no_list:
            edit_disk_no = disk_no.replace('RE', '')
            edit_disk_no_list.append(int(edit_disk_no))
        print(sorted(edit_disk_no_list))


if __name__ == '__main__':
    arrange_disk_info = ArrangeDiskInfo()
