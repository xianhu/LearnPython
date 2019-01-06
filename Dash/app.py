# _*_ coding: utf-8 _*_

"""
app主文件
"""

import dash
import dash_bootstrap_components as dbc

# 创建应用
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.__setattr__("title", "Dash Demo")

server = app.server
app.scripts.config.serve_locally = True
app.config.suppress_callback_exceptions = True
