import os
from ccaconfig import __version__
from ccaconfig.config import ccaConfig


def test_version():
    assert __version__ == "0.1.0"


def test_object_creation():
    confo = ccaConfig()
    assert confo.appname is None


def test_object_naming():
    confo = ccaConfig(appname="ccaconfig")
    assert confo.appname == "ccaconfig"


def test_config_environment_set():
    env = {"environment": "dev"}
    confo = ccaConfig(envd=env)
    assert confo.envd == env


def test_findconfig():
    iconf = {"environment": "dev", "product": "ccaconfig", "role": "config file"}
    confo = ccaConfig(appname="ccaconfig")
    conf = confo.findConfig()
    assert conf == iconf


def test_envOverrides():
    iconf = {"environment": "prod", "product": "ccaconfig", "role": "config file"}
    os.environ["CCACONFIG_ENVIRONMENT"] = "prod"
    confo = ccaConfig(appname="ccaconfig")
    conf = confo.envOverride()
    assert conf == iconf
