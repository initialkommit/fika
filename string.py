import re


class StringUtil(object):
    REGEX_TOKEN = r''' |=|\(|\)|\[|\]|<|>'''

    @staticmethod
    def mask_passwd_in_url(url):
        """
        e.g. mongodb://user:passwd@ip:27017/...
        -> mongodb://user:******@ip:27017/...
        """
        try:
            a, b = url.index(r'://') + len(r'://'), url.index('@')
            head, auth, tail = url[:a], url[a:b], url[b:]
            if len(auth) > 0:
                user, passwd = auth.split(':')
                if len(passwd) > 0:
                    passwd = '*' * len(passwd)
                    auth = '%s:%s' % (user, passwd)
            return head + auth + tail
        except:
            return url

    @staticmethod
    def split_by_bracket(s, regex=REGEX_TOKEN):
        return [t for t in re.split(regex, s) if len(t) > 0]

    @staticmethod
    def extract(s, start_s, end_s):
        if s and s.count(start_s) > 0 and s.count(end_s) > 0:
            start = s.find(start_s) + len(start_s)
            end = s.find(end_s, start)
            if start > 0 and end > 0:
                return s[start:end]
        return ''

    @staticmethod
    def split_by_size(s, size=100):
        lines = s.split('\n')
        result = ''
        for line in lines:
            if len(result) + len(line) > size:
                yield result
                result = line + '\n'
            else:
                result += line + '\n'
        yield result

    @staticmethod
    def merge(x, merge_tabs=False, merge_newlines=False, multi_blank_to_one=True):
        """
        TEXT인 경우, 공백, 탭, 줄바꿈 종류별로 merge를 한다.
        :param multi_blank_to_one: one blank 여부
        :param x:
        :param merge_tabs:
        :param merge_newlines:
        :return:
        """
        if multi_blank_to_one:
            multi_blank_to_one = ' '
        else:
            multi_blank_to_one = ''

        x = x.replace('\xa0', '')  # space
        x = re.sub(' +', multi_blank_to_one, x)  # replace multiple blanks to one blank.
        if merge_tabs:
            x = re.sub(r'\t+', r'\t', x)
        if merge_newlines:
            x = re.sub(r'\n+', r'\n', x)
        return x.strip()

    @staticmethod
    def merge_to_one_line(x):
        """
        HTML인 경우, 다수의 공백, 탭, 줄바꿈을 유지할 필요가 없으므로, 모두 단일 공백으로 합쳐준다.
        :param x:
        :return:
        """
        # replace multiple blanks, tabs, new lines to one blank.
        return ' '.join(x.split()).strip()

    @staticmethod
    def find_nth(s, x, n, i=0):
        i = s.find(x, i)
        if n == 1 or i == -1:
            return i
        else:
            return StringUtil.find_nth(s, x, n - 1, i + len(x))

    @staticmethod
    def remove_comment_line(text):
        lines = []
        for line in text.splitlines():
            if not line.startswith('#') and len(line) > 0:
                lines.append(line)
        return ' '.join(lines)

    @staticmethod
    def is_all_space(chars):
        if chars == '':
            return True

        for char in chars:
            if char.isalnum():
                return False
        return True


if __name__ == '__main__':
    print(StringUtil.merge('과    목', multi_blank_to_one=False))
    print(StringUtil.is_all_space('  '))
