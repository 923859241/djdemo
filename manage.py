#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

# 直接运行当前文件即可

# 如果出现某某资源不存在，那是因为静态资源没加载，可以先运行一次feedback再跑manage
def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djdemo.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    # 返回的default：
    # True是有语意 不需要过滤
    # False就是代表没有语义 需要过滤

    main()
    os.system("python3 manage.py runserver 0.0.0.0:8000")
