# _*_ coding: utf-8 _*_

"""
python发送邮件
"""

import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

# 第三方 SMTP 服务（以腾讯企业邮件为例）
mail_host = "smtp.exmail.qq.com"
mail_user = "from@from.com.cn"
mail_pass = "pwd"
mail_sender = mail_user
mail_receivers = ["to@to.com", "to@qq.com"]

# 设置邮件格式、内容等 -- 普通格式 ================================================
msg_plain = "邮件内容"
message = MIMEText("邮件内容", "plain", "utf-8")

# 设置邮件格式、内容等 -- HTML格式 ===============================================
msg_html = """
<p>Python 邮件发送测试...</p>
<p><a href="http://www.runoob.com">这是一个链接</a></p>
<table border="1">
    <tr><th>Month</th><th>Savings</th></tr>
    <tr><td>January</td><td>$100</td></tr>
    <tr><td>February</td><td>$80</td></tr>
</table>
"""
message = MIMEText(msg_html, "html", "utf-8")

# 设置邮件格式、内容等 -- HTML格式（带有图片和附件）==================================
msg_html = """
<p>Python 邮件发送测试...</p>
<p><a href="http://www.runoob.com">这是一个链接</a></p>
<p>图片演示：</p>
<p><img src="cid:image_id_1"></p>
"""
msg_content = MIMEText(msg_html, "html", "utf-8")
msg_image = MIMEImage(open("test.png", "rb").read())
msg_image.add_header("Content-ID", "<image_id_1>")

msg_file = MIMEText(open("test.csv", "rb").read(), "base64", "utf-8")
msg_file["Content-Type"] = "application/octet-stream"
msg_file["Content-Disposition"] = "attachment; filename=\"test.csv\""

message = MIMEMultipart("related")
message.attach(msg_content)
message.attach(msg_image)
message.attach(msg_file)
# ==============================================================================

# 设置邮件的收发件、标题等
message["From"] = mail_sender
message["To"] = ";".join(mail_receivers)
message["Subject"] = Header("邮件标题", "utf-8")

try:
    # 登录，并发送邮件
    smtpObj = smtplib.SMTP()
    smtpObj.connect(mail_host, 25)
    smtpObj.login(mail_user, mail_pass)
    smtpObj.sendmail(mail_sender, mail_receivers, message.as_string())
    print("success")
except smtplib.SMTPException as excep:
    print("error", excep)
