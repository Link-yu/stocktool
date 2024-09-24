import requests
import json


class DingTalkBot:
    def __init__(self, webhook_url, secret=None):
        """
        初始化DingTalkBot对象。
        :param webhook_url: 钉钉机器人的Webhook URL
        :param secret: 钉钉机器人的加签密钥（如果需要的话）
        """
        self.webhook_url = webhook_url
        self.secret = secret

    def send_text(self, message):
        """
        发送文本消息。
        :param message: 要发送的文本消息内容
        """
        data = {
            "msgtype": "text",
            "text": {
                "content": message
            }
        }
        headers = {'Content-Type': 'application/json;charset=utf-8'}
        self._send(data, headers)

    def send_markdown(self, title, text):
        """
        发送Markdown消息。
        :param title: 消息标题
        :param text: 消息内容
        """
        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": text
            }
        }
        headers = {'Content-Type': 'application/json;charset=utf-8'}
        self._send(data, headers)

    def _send(self, data, headers):
        """
        发送消息。
        :param data: 要发送的消息数据
        :param headers: 请求头
        """
        url = self.webhook_url

        response = requests.post(url, data=json.dumps(data), headers=headers)
        if response.status_code != 200:
            raise Exception("Failed to send message to DingTalk: {}".format(response.text))

