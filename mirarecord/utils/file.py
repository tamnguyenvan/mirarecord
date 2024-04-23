from datetime import datetime


def generate_filename(extension: str, prefix: str = 'MiraRecord'):
    time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return f'{prefix} {time_str}{extension}'