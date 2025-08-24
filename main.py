import subprocess
import sys
import PCscript
import PhoneScript
def install_requirements():
    subprocess.check_call([
        sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
    ])








if __name__ == "__main__":
    # install_requirements()
    PCscript.StartPCBing()
    PhoneScript.StartPhoneBing()