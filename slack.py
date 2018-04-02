import threading

from slackclient import SlackClient

lock = threading.Lock()


# noinspection PyBroadException
class SlackUtil(object):
    DEFAULT_CHANNEL = '_server_noti'
    API_TOKEN = ''  # FIXME
    slack_client = SlackClient(API_TOKEN)

    @classmethod
    def send_message(cls, message, channel=DEFAULT_CHANNEL):
        with lock:
            cls.slack_client.api_call("chat.postMessage", channel=channel, text=message)


if __name__ == '__main__':
    SlackUtil.send_message('슬랙 메시지 테스트', channel='_bot_test')
