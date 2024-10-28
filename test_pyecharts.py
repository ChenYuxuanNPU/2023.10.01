import json
from pyecharts.charts import Line
from pyecharts.options import ToolboxOpts
from pyecharts.charts import Pie

my_line = Pie()
my_line.add("",[["a",1],["b",2]])
my_line.set_global_opts(
 toolbox_opts = ToolboxOpts(is_show = True)
)
my_line.render()