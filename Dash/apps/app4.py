# _*_ coding: utf-8 _*_

"""
app4实例
"""

import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from Dash.apps.app4data import *


# 创建layout
layout = dbc.Container(children=[
    html.H3("DataTable Sizing", className="mt-2"),
    html.Div(children=dash_table.DataTable(
        data=df_election.to_dict('rows'),
        columns=[{'id': c, 'name': c} for c in df_election.columns]
    ), className="mt-2"),

    dash_table.DataTable(
            style_table={'width': '100%'},
            style_data={'whiteSpace': 'normal'},
            content_style='grow',
            css=[{
                'selector': '.dash-cell div.dash-cell-value',
                'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
            }],
            data=df_election.to_dict('rows'),
            columns=[{'id': c, 'name': c} for c in df_election.columns]
        ),

    html.Div(children=dash_table.DataTable(
        data=df_election.to_dict('rows'),
        columns=[{'id': c, 'name': c} for c in df_election.columns],
        style_cell={
            'whiteSpace': 'no-wrap',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
            'maxWidth': 0,
        },
    ), className="mt-2"),

    dash_table.DataTable(
    style_data={'whiteSpace': 'normal'},
        style_cell={
            'whiteSpace': 'no-wrap',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
            'maxWidth': 0,
        },
        css=[{
        'selector': '.dash-cell div.dash-cell-value',
        'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
    }],
    data=df_long.to_dict('rows'),
    columns=[{'id': c, 'name': c} for c in df_long.columns]
)
],
)

#
# import dash
#
# app = dash.Dash(
#     __name__, external_stylesheets=["https://codepen.io/chriddyp/pen/dZVMbK.css"]
# )
# app.config["suppress_callback_exceptions"] = True
#
# server = app.server
#
# app.layout = layout
#
# app.css.config.serve_locally = True
# app.scripts.config.serve_locally = True
#
# if __name__ == "__main__":
#     app.run_server(debug=True)
