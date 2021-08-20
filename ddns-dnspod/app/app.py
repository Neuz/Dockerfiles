# -*- coding: utf-8 -*-

import json
import logging
import os
import configparser
import logging
import requests
import time


# 格式化logging
LOG_LEVEL = logging.DEBUG if os.getenv('DEBUG_MODE') and os.getenv('DEBUG_MODE') == '1' else logging.INFO
LOG_FORMAT = "[%(asctime)s][%(levelname)s] - %(message)s"
logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL)


class Config(object):
    dnspod_id       : str = None # dnspod id
    dnspod_token    : str = None # dnspod token
    domain          : str = None # 默认 域名 # 格式 domain.com
    sub_domain      : str = None # 子域名   # 格式 www
    internal        : int = 30   # 最小更新间隔 秒
    email           : str = None # 邮箱    # 格式 'my@email.com'
    record_ip       : str = None # DNSPOD记录IP
    record_id       : str = None # DNSPOD记录ID，系统生成
    last_update_time: int = None # 上次更新时间戳，系统生成

    cfg_file_path   : str = 'app.config' # 配置文件路径

    def __init__(self) -> None:
        super().__init__()
        # 配置文件 > 环境变量
        self.get_config_from_env()
        self.get_config_from_file()
        self.check_config()

    def check_config(self):
        try:
            if(not(self.dnspod_id)):
                raise Exception('配置参数异常：dnspod_id 为空')
            if(not(self.dnspod_token)):
                raise Exception('配置参数异常：dnspod_token 为空')
            if(not(self.domain)):
                raise Exception('配置参数异常：domain 为空')
            if(not(self.sub_domain)):
                raise Exception('配置参数异常：sub_domain 为空')
            if(not(self.internal)):
                raise Exception('配置参数异常：internal 为空')
            # if(self.internal < 3):
            #     raise Exception('配置参数异常：internal 执行间隔不允许小于3秒')
            if(not(self.email)):
                raise Exception('配置参数异常：email 为空')
            logging.info('配置校验完成')
            logging.debug(f'dnspod_id: {self.dnspod_id}')
            logging.debug(f'dnspod_token: {self.dnspod_token}')
            logging.debug(f'domain: {self.domain}')
            logging.debug(f'sub_domain: {self.sub_domain}')
            logging.debug(f'internal: {self.internal}')
            logging.debug(f'email: {self.email}')
        except Exception as err:
            logging.error(f'配置校验失败! {err}')
            logging.error('退出')
            exit()

    # 从环境变量获取配置
    def get_config_from_env(self):
        logging.info(f'读取环境变量')
        self.dnspod_id        = os.getenv('DNSPOD_ID')
        self.dnspod_token     = os.getenv('DNSPOD_TOKEN')
        self.domain           = os.getenv('DOMAIN')
        self.sub_domain       = os.getenv('SUB_DOMAIN')
        self.internal         = int(os.getenv('INTERNAL')) if os.getenv('INTERNAL') else 30
        self.email            = os.getenv('EMAIL')
        self.last_update_time = 0

    # 从文件获取配置
    def get_config_from_file(self):
        if(not(os.path.exists(self.cfg_file_path))):
            return
        logging.info(f'使用配置文件[{self.cfg_file_path}]')
        parser = configparser.ConfigParser()
        parser.read(self.cfg_file_path)

        self.dnspod_id        = parser.get('cfg', 'dnspod_id')
        self.dnspod_token     = parser.get('cfg', 'dnspod_token')
        self.domain           = parser.get('cfg', 'domain')
        self.sub_domain       = parser.get('cfg', 'sub_domain')
        self.internal         = int(parser.get('cfg', 'internal')) if parser.get('cfg', 'internal') else 30
        self.email            = parser.get('cfg', 'email')
        self.last_update_time = 0


class Tools(object):
    get_ip_url = 'http://www.httpbin.org/ip'
    # get_ip_url = 'https://api.ip.sb/ip'

    # 获取当前公网IP
    @classmethod
    def get_public_ip(cls) -> str:
        result = requests.get(cls.get_ip_url, verify=False)
        if(result.status_code != 200):
            raise Exception('公网IP获取失败', result)
        else:
            return str(json.loads(result.text)['origin'])


class DnspodApi(object):

    __API_NAME = 'Dnspod-Api'
    __API_VERSION = '0.0.2'

    get_record_url    = 'https://dnsapi.cn/Record.List'
    update_record_url = 'https://dnsapi.cn/Record.Modify'

    def __get_headers(self, email: str):
        return {
            'User-Agent': f'{self.__API_NAME}/{self.__API_VERSION}({email})',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

    @classmethod
    def update_record(cls, cfg: Config):
        headers = cls.__get_headers(cls, cfg.email)
        data = {
            'login_token': f'{cfg.dnspod_id},{cfg.dnspod_token}',
            'format': 'json',
            'lang': 'cn',
            'error_on_empty': 'no',
            'domain': cfg.domain,
            'sub_domain': cfg.sub_domain,
            'record_type': 'A',
            'record_line': '默认',
            'record_id': cfg.record_id,
            'value': cfg.record_ip
        }

        response = requests.post(url=cls.update_record_url, data=data, headers=headers, timeout=3)
        result = json.loads(response.text)
        if(int(result['status']['code']) != 1):
            raise Exception('更新记录操作失败', result)
        logging.info(f'更新记录操作成功:{cfg.sub_domain}.{cfg.domain} => {cfg.record_ip}')

    @classmethod
    def get_record(cls, cfg: Config):
        headers = cls.__get_headers(cls, cfg.email)
        data = {
            'login_token': f'{cfg.dnspod_id},{cfg.dnspod_token}',
            'format': 'json',
            'lang': 'cn',
            'error_on_empty': 'no',
            'record_type': 'A',
            'domain': cfg.domain,
            'sub_domain': cfg.sub_domain
        }
        response = requests.post(url=cls.get_record_url, data=data, headers=headers, timeout=3)
        result = json.loads(response.text)
        if(int(result['status']['code']) != 1):
            raise Exception('获取记录操作失败', result)
        records = [{'id': r['id'], 'value':r['value']} for r in result['records'] if str(r['name']) == cfg.sub_domain and int(r['enabled']) == 1]
        if(len(records) < 1):
            raise Exception(f'没有找到子域名[{cfg.sub_domain}]相关记录，请先前往dnspod进行添加', result)
        return records[0]


def run(cfg: Config):
    current_time = int(round(time.time() * 1000))
    is_record_timeout = (current_time - cfg.last_update_time) > 600000 # 10分钟
    
    # 初始化获取域名记录
    if(not(cfg.record_ip) or is_record_timeout):
        logging.debug('记录超时 或 没有域名记录')
        record = DnspodApi().get_record(cfg)
        cfg.record_ip        = record['value']
        cfg.record_id        = record['id']
        cfg.last_update_time = current_time

    # 获取公网IP
    public_ip = Tools().get_public_ip()

    if(cfg.record_ip == public_ip):
        logging.debug(f'公网IP没有变化: {public_ip}')
        return

    cfg.record_ip = public_ip
    DnspodApi().update_record(cfg)


if __name__ == '__main__':
    logging.info('开始启动...')
    cfg = Config()

    while True:
        try:
            run(cfg)
        except Exception as error:
            logging.error(error.args[0] if(len(error.args) > 0) else error)
            logging.debug(error.args[1] if(len(error.args) > 1) else '')

        time.sleep(cfg.internal)
