import sys

try:
    s=input('enter something-->')
except EOFError:
    print('/nWhy did you do an EOF on me?')
    sys.exit()  # 退出程序
except:
    print('/nSome error/exception occurred.')

print('Done')