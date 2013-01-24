from django.core.management import setup_environ
import sys

sys.path.insert(0,os.getcwd().replace("/Common/hook",""))
import GitPower.settings as settings
setup_environ(settings)
