from excel2mysql_program import TvProgramRegister
from excel2mysql_recorded import TvContentsRegister
from disk_no_setting import DiskNoSetting

tv_program_register = TvProgramRegister()
tv_program_register.export()

range_disk_no = '2864,2999'
tv_contents_register = TvContentsRegister(range_disk_no, False)
# tv_contents_register = TvContentsRegister(range_disk_no, False)
# tv_contents_register.export()
# tv_contents_register.export('TV録画2', 15000)
# tv_contents_register.export2('0001-1114')
tv_contents_register.export('ZIP')
# tv_contents_register.export('2030')

dick_no_setting = DiskNoSetting()
# dick_no_setting.pickup_no_from_label()
# dick_no_setting.update_path()
# dick_no_setting.exist_check()
# dick_no_setting.pickup_disk_from_recorded()
dick_no_setting.pickup_disk_from_recorded(False)
