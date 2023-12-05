import multiprocessing
import time
import subprocess
def daemon_function():
    while True:
        print("Daemon process is running...")
        output = subprocess.check_output(['ls', '-l'])
        print(output.decode('utf-8'))  # 将字节转换为字符串并打印输出
        time.sleep(1)

if __name__ == "__main__":
    daemon_process = multiprocessing.Process(target=daemon_function)
    daemon_process.daemon = True  # 设置为守护进程
    daemon_process.start()

    time.sleep(5)  # 主进程等待一段时间
    print("Main process is ending...")
