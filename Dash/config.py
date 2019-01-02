# _*_ coding: utf-8 _*_

"""
配置文件
"""

import pandas as pd

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

# https://getbootstrap.com/docs/4.0/utilities
"""
ALL:
    sm / md / lg / xl
    top / right / bottom / left
    primary / secondary / success / danger / warning / info

Borders: 
    border, border-top, border-primary, 
    border-light, border-dark, border-white
    rounded, rounded-top, rounded-circle, rounded-0

Color:
    Text: text-primary, text-light, text-dark, text-white, text-muted
    Backgroud: bg-primary, bg-light, bg-dark, bg-white, bg-gradient-primary, bg-gradient-light, bg-gradient-dark
    
Display:
    d-[none/inline/inline-block/block/table/table-cell/table-row/flex/inline-flex]
    d-[sm/md/lg/xl]-[none/inline...]

Flex:
    Display: d-flex, d-inline-flex
    Direction: flex-row, flex-row-reverse, flex-column, flex-column-reverse
    Justify content: justify-content-[start/end/center/between/around]
    Align items: align-items-[start/end/center/baseline/stretch]
    Align self: align-self-[start/end/center/baseline/stretch]
    Align content: align-content-[start/end/center/around/stretch]
    Wrap: flex-wrap, flex-nowrap
    
Float:
    float-left, float-right, float-none, float-sm-left
    
Position:
    position-static, position-relative, position-absolute, position-fixed, position-sticky

Sizing:
    w-25, w-50, w-75, w-100, mw-50, mw-100
    h-25, h-50, h-75, h-100, mh-50, mh-100

Spacing:
    Margin: m-2, mt-1, mr-2, mb-3, ml-4, mx-3, my-2, m-auto
    Padding: p-2, pt-1, pr-2, pb-3, pl-4, px-3, py-2, p-auto

Text:
    text-primary, text-light, text-dark, text-white, text-muted
    text-left, text-center, text-right, text-sm-left, text-lg-left
    text-lowercase, text-uppercase, text-capitalize
    font-weight-[bold/normal/light], font-italic

Vertical alignment:
    align-baseline, align-top, align-middle, align-bottom, align-text-top, align-text-bottom
    
Visibility:
    visible, invisible
"""
