import subprocess
import threading

threading.Thread(target=subprocess.run,
                 args=["D:\编程\workpathByPython\seleniumRobot\scripts\open_chrome_debugger.bat"]).start()