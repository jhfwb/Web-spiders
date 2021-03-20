import subprocess
import threading
from _xhr_tool._utils import relpath
def chrome_browser_open():
    threading.Thread(target=subprocess.run,args=[relpath("../scripts/open_chrome_debugger.bat")]).start()

