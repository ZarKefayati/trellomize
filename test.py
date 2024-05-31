import logging

# تنظیمات logging برای خطاها
error_logger = logging.getLogger('error_logger')
error_logger.setLevel(logging.ERROR)
error_file_handler = logging.FileHandler('errors.log')
error_formatter = logging.Formatter('%(asctime)s - %(message)s')
error_file_handler.setFormatter(error_formatter)
error_logger.addHandler(error_file_handler)

# تنظیمات logging برای اطلاعات عمومی
info_logger = logging.getLogger('info_logger')
info_logger.setLevel(logging.INFO)
info_file_handler = logging.FileHandler('info.log')
info_formatter = logging.Formatter('%(asctime)s - %(message)s')
info_file_handler.setFormatter(info_formatter)
info_logger.addHandler(info_file_handler)

# تابعی که خطا رخ می‌دهد
def divide(x, y):
    try:
        result = x / y
    except ZeroDivisionError as e:
        error_logger.error(f'خطا: {e}')
    else:
        info_logger.info(f'نتیجه: {result}')

# فراخوانی تابع با پارامتر مناسب
divide(10, 2)

print('خطاها و اطلاعات با موفقیت در فایل‌های لاگ مربوطه ثبت شد.')
