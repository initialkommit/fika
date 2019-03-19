import html
import re

import lxml.html

from string import StringUtil


class HtmlUtil:
    @staticmethod
    def remove_tags_in_html(html):
        return re.sub(r'<[a-zA-Z/][^>]*>',
                      '',
                      html,
                      count=0,
                      flags=re.DOTALL | re.IGNORECASE)

    @staticmethod
    def remove_comments_in_html(html):
        return re.sub(r'<!--.*?-->',
                      '',
                      html,
                      count=0,
                      flags=re.DOTALL | re.IGNORECASE)

    @staticmethod
    def remove_javascripts_in_doc(doc):
        for element in doc.iter("script"):
            element.drop_tree()

        return doc

    @staticmethod
    def remove_elements(doc, css_pattern_list, remove_string_list=[]):
        for p in css_pattern_list:  # remove unnecessary links
            for e in doc.select(p):
                if len(remove_string_list) > 0:
                    if e.text:
                        for string in remove_string_list:
                            if string in e.text:
                                e.extract()
                else:
                    e.extract()
        return doc

    # noinspection PyUnresolvedReferences
    @staticmethod
    def trim(html, prefix_url=None):
        """코멘트 제거, 자바스크립트 제거 (100.daum.net 제외)

        \r\n -> \n
        html에 포함된 <br>, <p>를 \n 으로 변환
        다수의 공백, \t, \n 을 하나로 합침
        """
        html = html.replace('\r\n', '\n')
        convert_dic = {
            '<br>': '\n', '<br/>': '\n', '<br />': '\n',
            '<p>': '\n', '<p/>': '\n', '<p />': '\n',
            '<BR>': '\n', '<BR/>': '\n', '<BR />': '\n',
            '<P>': '\n', '<P/>': '\n', '<P />': '\n'
        }
        for _from, _to in convert_dic.items():
            html = html.replace(_from, _to)
        # remove html comments.
        html = HtmlUtil.remove_comments_in_html(html)

        # convert to html element.r
        doc = lxml.html.document_fromstring(html)

        if prefix_url:
            # convert links to absolute links.
            doc.make_links_absolute(prefix_url)
            # javascript를 지우면 일부가 안 보이는 HTML도 있음
            # (100.daum.net)
            if '100.daum.net' not in prefix_url:
                # remove javascript elements.
                doc = HtmlUtil.remove_javascripts_in_doc(doc)
        # convert to html string.
        html = lxml.html.tostring(doc,
                                  encoding='utf8',
                                  include_meta_content_type=True)
        html = html.decode('utf8')  # bytes -> string
        # replace multiple blanks to one blank.
        html = StringUtil.merge(html)
        return html.strip()

    @staticmethod
    def unescape(_html):
        """
        &로 시작하는 HTML 문자를 원형으로 복원
        &gt; -> >
        &lt; -> <
        :param _html:
        :return:
        """
        return html.unescape(_html)
