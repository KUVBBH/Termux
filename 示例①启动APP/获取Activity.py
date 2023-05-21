import sys
from adb_cv import Android as an

pkg_name='com.tencent.mobileqq'  #app的包名

a=an(38201)

a.activity_get(pkg_name)