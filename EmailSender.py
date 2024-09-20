import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header


class EmailSender:
    def __init__(self, smtp_server, smtp_port, username, password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password

    def send_email(self, sender, receiver, subject, body, attachments=None):
        message = MIMEMultipart()
        message['From'] = Header(sender)
        message['To'] = Header(receiver)
        message['Subject'] = Header(subject)

        # 邮件正文内容
        message.attach(MIMEText(body, 'plain', 'utf-8'))

        # 添加附件
        if attachments:
            for attachment in attachments:
                with open(attachment, 'rb') as f:
                    part = MIMEText(f.read(), 'base64', 'utf-8')
                    part['Content-Disposition'] = 'attachment; filename="%s"' % attachment
                    message.attach(part)

        try:
            # 连接到SMTP服务器
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()  # 启用安全传输模式
            server.login(self.username, self.password)  # 登录验证
            server.sendmail(sender, receiver, message.as_string())  # 发送邮件
            print('邮件发送成功')
        except Exception as e:
            print('邮件发送失败', e)
        finally:
            server.quit()  # 断开服务器连接


# 使用示例
if __name__ == '__main__':
    smtp_server = 'smtp.163.com'
    smtp_port = 25
    username = 'kevinyulk@163.com'
    password = 'SWaYvNdTKZA4eEtJ'
    sender = 'kevinyulk@163.com'
    receiver = 'yulk48789@hundsun.com'
    subject = '邮件主题'
    body = '这是邮件正文'

    # 实例化EmailSender
    email_sender = EmailSender(smtp_server, smtp_port, username, password)

    # 发送邮件
    email_sender.send_email(sender, receiver, subject, body)

    # 发送带附件的邮件
    # attachments = ['example.txt', 'image.png']
    # email_sender.send_email(sender, receiver, subject, body, None)
