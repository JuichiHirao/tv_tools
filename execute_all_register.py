from excel2mysql_program import TvProgramRegister
from excel2mysql_recorded import TvContentsRegister
from disk_no_setting import DiskNoSetting

tv_program_register = TvProgramRegister()
tv_program_register.export()

tv_contents_register = TvContentsRegister()
tv_contents_register.export2('TV録画2')
tv_contents_register.export2('ZIP')
tv_contents_register.export2('2030')

dick_no_setting = DiskNoSetting()
dick_no_setting.pickup_disk_from_recorded(False)
