"""
config.py

read and merge config files and environment values

later values overwrite earlier values, order of precedence is

  /etc/appname.yaml
  /etc/appname/appname.yaml
  $HOME/.config/appname.yaml
  $HOME/.appname.yaml
  $(pwd)/appname.yaml
  Environment Values
"""
import os
import sys
import yaml
import ccalogging

# from ccaconfig.errors import errorExit
# from ccaconfig.errors import errorNotify
from ccaconfig.errors import errorRaise

ccalogging.setConsoleOut()
ccalogging.setDebug()
log = ccalogging.log


class NoApplicationName(Exception):
    pass


class ccaConfig:
    """
    object to encapsulate reading and merging config files
    """

    def __init__(self, appname=None, envd=None):
        log.debug(f"ccaConfig starting. appname={appname}, envd={envd}")
        self.configfn = None
        self.setAppName(appname)
        self.setEnvD(envd)

    def setEnvD(self, envd):
        log.debug(f"envd={envd}")
        self.envd = envd

    def setAppName(self, appname):
        log.debug(f"appname={appname}")
        self.appname = appname

    def checkAndLoad(self, config, fn):
        try:
            tconfig = {}
            log.debug(f"checking for {fn}")
            if os.path.isfile(fn):
                log.debug(f"opening {fn}")
                with open(fn, "r") as ifn:
                    log.info(f"reading {fn}")
                    tconfig = yaml.safe_load(ifn)
            for item in tconfig:
                config[item] = tconfig[item]
            return config
        except Exception as e:
            fname = sys._getframe().f_code.co_name
            log.error(f"Exception {e} in {fname}: file: {fn}")
            errorRaise(fname, e)

    def findConfig(self):
        config = {}
        if self.appname is not None:
            cfn = f"{self.appname}.yaml"
            log.debug(f"will look for {cfn} as a config file")
            try:
                files = [
                    f"/etc/{cfn}",
                    f"/etc/{self.appname}/{cfn}",
                    os.path.expanduser(f"~/.config/{cfn}"),
                    os.path.expanduser(f"~/.{cfn}"),
                    os.getcwd() + f"/{cfn}",
                ]
                for fn in files:
                    config = self.checkAndLoad(config, fn)
            except Exception as e:
                fname = sys._getframe().f_code.co_name
                log.error(f"Exception {e} in {fname}")
                errorRaise(fname, e)
        return config

    def envOverride(self):
        try:
            prefix = self.appname.upper() + "_"
            config = self.findConfig()
            for item in os.environ:
                if item.startswith(prefix):
                    vname = item.split(prefix)[1].lower()
                    config[vname] = os.environ[item]
            return config
        except Exception as e:
            fname = sys._getframe().f_code.co_name
            log.error(f"Exception {e} in {fname}")
            errorRaise(fname, e)
