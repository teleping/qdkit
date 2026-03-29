# -*- coding: utf-8 -*-
"""
@Time ： 2023/12/28
@Auth ： zhangping
"""
import os, base64, yaml, logbook, logbook.more, pandas as pd
# from jinja2 import Environment, FileSystemLoader

pd.set_option('display.max_columns', None), pd.set_option('display.max_rows', None)
pd.set_option('display.width', 10000), pd.set_option('mode.use_inf_as_na', True)

find_path = lambda name, depth=5: ['../' * i + name for i in range(depth) if os.path.exists('../' * i + name)][0]
config = yaml.safe_load(open(find_path('config.yaml'), 'r', encoding='utf-8'))


# class FileUtils:
#     @classmethod
#     def image2base64(cls, image_file, with_frefix=False, clear_file=False):
#         with open(image_file, "rb") as file:
#             encoded_string = base64.b64encode(file.read()).decode('utf-8')
#         if clear_file: os.remove(image_file)
#         return f'data:image/png;base64,{encoded_string}' if with_frefix else encoded_string
#
#     @classmethod
#     def render_template(cls, target, context, template_file='template.html', template_root='./'):
#         env = Environment(loader=FileSystemLoader(template_root))
#         template = env.get_template(template_file)
#         with open(target, 'w', encoding='utf-8') as file:
#             file.write(template.render(**context))


def get_logger(level='INFO', std_log=True, file_log=True, file_folder='logs'):
    logs_dir = find_path(file_folder)
    # if not os.path.exists(logs_dir): os.makedirs(logs_dir)
    logbook.set_datetime_format('local')
    log = logbook.Logger('log')
    log.handlers = []
    log_formate = lambda record, handler: \
        f'[{record.time}] [{record.level_name}] [{os.path.split(record.filename)[-1]}] [{record.func_name}] [{record.lineno}] {record.message}'

    if std_log:  # 屏幕打印
        std_handler = logbook.more.ColorizedStderrHandler(level=level, bubble=True)
        std_handler.formatter = log_formate
        log.handlers.append(std_handler)
    if file_log:  # 日志文件
        file_handler = logbook.TimedRotatingFileHandler(
            os.path.join(logs_dir, '%s.log' % 'log'), level=level, date_format='%Y-%m-%d', bubble=True,
            encoding='utf-8')
        file_handler.formatter = log_formate
        log.handlers.append(file_handler)
    return log


logger = get_logger()
