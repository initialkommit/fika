import os
import traceback
from ftplib import FTP
from ftplib import error_perm


class FtpUtil:

    def __init__(self,
                 download_path,
                 ftp_ip,
                 ftp_path,
                 ftp_id,
                 ftp_pwd):
        self.download_path = download_path
        self.ftp_ip = ftp_ip
        self.ftp_path = ftp_path
        self.ftp_id = ftp_id
        self.ftp_pwd = ftp_pwd
        self.ftp = None
        self.connect()

    def connect(self):
        """FTP 연결"""
        try:
            self.ftp = FTP(self.ftp_ip)
            self.ftp.login(self.ftp_id, self.ftp_pwd)
            # ftp.encoding = 'utf-8'
        except OSError:  # invalid ip
            print("[Errno 51] Network is unreachable")
        except error_perm as e:  # invalid login
            print(e)

        self.ftp.cwd(self.ftp_path)

    def get_files(self, filename=None):
        """다운로드 받을 파일 목록을 가져온다.

        Parameters:
            filename (str): 확장자를 포함한 다운로드 받을 파일

        Return:
            (dict) 파일별 날짜별 데이터
        """
        all_file = self.ftp.nlst()[1:]

        if filename:
            file_list = []
            for f in all_file:
                if filename == f:
                    file_list.append(filename)
            return file_list
        else:
            return all_file

    def download(self, filename):
        """Download a file"""
        try:
            with open(os.path.join(self.download_path, filename), "wb") as f:
                self.ftp.retrbinary("RETR " + filename, f.write)
                print('Downloaded successfully %s' % filename)
            return True
        except Exception as e:
            traceback.print_exc()
            return False
