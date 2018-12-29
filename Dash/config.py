# _*_ coding: utf-8 _*_

"""
配置文件
"""

import pandas as pd

# 定义颜色值
color_primary, color_primary_light = "#2d7df6", "#d0e4fc"
color_secondary, color_secondary_light = "#6e757c", "#e2e3e5"
color_success, color_success_light = "#53a451", "#d9ecdb"
color_info, color_info_light = "#49a0b5", "#d6ebf0"
color_warning, color_warning_light = "#f6c244", "#fdf3d1"
color_danger, color_danger_light = "#cb444a", "#f3d8da"

# 有用的数据
df = pd.read_csv("Dash/data.csv")
markdown_text = """
### Dash and Markdown

Dash apps can be written in Markdown.
Dash uses the [CommonMark](http://commonmark.org/)
specification of Markdown.
Check out their [60 Second Markdown Tutorial](http://commonmark.org/help/)
if this is your first introduction to Markdown!
"""
