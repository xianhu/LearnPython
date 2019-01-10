# _*_ coding: utf-8 _*_

"""
app4实例
"""

import dash_table
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
from Dash.app import app


# 创建layout
def layout(df_data):
    return dbc.Container(children=[
        html.Label(id="label", className="mt-2"),
        html.Div(children=dash_table.DataTable(
            id="datatable",
            data=df_data.to_dict("rows"),
            columns=[{
                "id": col,
                "name": col,
                "type": "text",
                "hidden": False,
                "deletable": False,
                "editable_name": False
            } for col in df_data.columns[:10]],

            # # 数据可编辑
            # editable=True,
            # # 行可删除
            # row_deletable=True,
            # # 虚拟化，加载大数据
            # virtualization=True,
            #
            # # 过滤: "fe", "be", True, False
            # filtering=True,
            # filtering_settings="",

            # 排序: "fe", "be", True, False
            sorting=True,
            sorting_type="multi",
            sorting_settings=[],

            # 选择: multi|single
            row_selectable="multi",
            selected_rows=[],
            selected_cells=[[]],

            # # 分页功能
            # pagination_settings={
            #     "current_page": 0,
            #     "page_size": 10
            # },
            # # 分页方式: "fe", "be", True, False
            # pagination_mode="be",
            #
            # # 固定行、列
            # n_fixed_rows=1,
            # n_fixed_columns=1,
            # # 像list一样：只有行边框
            # style_as_list_view=True,
            # # 多个表头：需columns配合
            # merge_duplicate_headers=True,
            # # 内容样式：fit|grow
            # content_style="grow",
            #
            # # 数据利用dropdown编辑
            # column_static_dropdown=[{
            #     "id": "climate",
            #     "dropdown": [
            #         {"label": i, "value": i} for i in ["a", "b"]
            #     ]
            # }, {
            #     "id": "city",
            #     "dropdown": [
            #         {"label": i, "value": i} for i in ["c", "d"]
            #     ]
            # }],
            # column_conditional_dropdowns=[[{
            #     "id": "Neighborhood",
            #     "dropdowns": [{
            #         "condition": "City eq 'NYC'",
            #         "dropdown": [
            #             {"label": i, "value": i} for i in ["Brooklyn", "Queens", "Staten Island"]
            #         ]
            #     }, {
            #         "condition": "City eq 'Montreal'",
            #         "dropdown": [
            #             {"label": i, "value": i} for i in ["Mile End", "Plateau", "Hochelaga"]
            #         ]
            #     }],
            # }]],
            #
            # # 表格样式
            # style_table={
            #     # 设置宽度: maxHeight
            #     "height": "300px",
            #     # 设置X轴平移
            #     "overflowX": "scroll",
            #     # 设置Y轴最大高度及平移
            #     "maxHeight": "300px",
            #     "overflowY": "scroll",
            #     # 边框样式
            #     "border": "thin lightgrey solid",
            # },

            # 包括Header-cells, Data-cells, 和Filter-cells
            style_cell={
                # 基本设置
                # "color": "white",
                # "fontSize": "medium",
                "padding": "5px",
                # "width": "180px",
                "minWidth": "0px",
                "maxWidth": "180px",
                # 多行显示: no-wrap|normal
                "whiteSpace": "no-wrap",
                "overflow": "hidden",
                # 显示省略号
                "textOverflow": "ellipsis",
                # 文本对齐方式
                "textAlign": "center",
            },
            # style_cell_conditional=[
            #     # 自定义列宽
            #     {"if": {"column_id": "Date"}, "width": "30%"},
            #     {"if": {"column_id": "Region"}, "width": "30%"},
            #     {"if": {"column_id": "Temperature"}, "width": "130px"},
            #     {"if": {"column_id": "Humidity"}, "width": "130px"},
            #     # 自定义文本对齐方式
            #     {"if": {"column_id": "Region"}, "textAlign": "left"},
            # ] + [
            #    # 自定义文本对齐方式：for循环
            #    {"if": {"column_id": c}, "textAlign": "left"} for c in ["Date", "Region"]
            # ] + [
            #     # Striped行
            #     {"if": {"row_index": "odd"}, "backgroundColor": "rgb(248, 248, 248)"}
            # ],

            # # Header-cells样式
            # style_header={
            #     # 设置表头样式
            #     "textAlign": "center",
            #     "fontWeight": "bold",
            #     "backgroundColor": "white",
            # },
            # style_header_conditional=[],

            # # Data-cells样式
            # style_data={
            #     # 忽略空白
            #     "whiteSpace": "normal",
            # },
            # style_data_conditional=[
            #     # 第3行的字体加粗
            #     {"if": {"row_index": 3}, "fontWeight": "bold"},
            #     # 第4行高亮显示
            #     {"if": {"row_index": 4}, "backgroundColor": "#3D9970", "color": "white"},
            #     # Temperature列高亮显示
            #     {"if": {"column_id": "Temperature"}, "backgroundColor": "#3D9970", "color": "white"},
            #     # 高亮部分Cell，if中添加一个filter，eq > <
            #     {
            #         "if": {
            #             "column_id": "Region",
            #             "filter": "Region eq 'Montreal'"
            #         }, "backgroundColor": "#3D9970", "color": "white",
            #     }, {
            #         "if": {
            #             "column_id": "Humidity",
            #             "filter": "Humidity eq num(20)"
            #         }, "backgroundColor": "#3D9970", "color": "white",
            #     }, {
            #         "if": {
            #             "column_id": "Temperature",
            #             "filter": "Temperature > num(3.9)"
            #         }, "backgroundColor": "#3D9970", "color": "white",
            #     },
            # ],

            # # Filter-cells样式
            # style_filter={},
            # style_filter_conditional=[],

            css=[{
                "selector": ".dash-cell div.dash-cell-value",
                "rule": "display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;"
            }],
        ), className="mt-2"),
    ])


@app.callback(Output("label", "children"), [
    Input("datatable", "data"),
    Input("datatable", "selected_rows")
])
def update_date(rows, selected_rows):
    if rows is None:
        rows = []
    if selected_rows is None:
        selected_rows = []
    string = "总行数：%d" % len(rows)
    string += "，被选中的行：%s" % ",".join(map(str, selected_rows))
    return string
