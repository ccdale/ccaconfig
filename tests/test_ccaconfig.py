import os
from ccaconfig import __version__
from ccaconfig.config import ccaConfig


def test_version():
    assert __version__ == "0.3.9"


def test_object_creation():
    confo = ccaConfig()
    assert confo.appname is None


def test_object_naming():
    confo = ccaConfig(appname="ccaconfig")
    assert confo.appname == "ccaconfig"


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


def test_defaultconfig():
    dconf = {"environment": "staging", "defaultval": "NotSet"}
    iconf = {"environment": "prod", "product": "ccaconfig", "role": "config file"}
    oconf = {"environment": "pre-prod"}
    confo = ccaConfig(appname="ccaconfig", defaultd=dconf, overrided=oconf)
    conf = confo.envOverride()
    assert conf["defaultval"] == "NotSet"


def test_overconf():
    dconf = {"environment": "staging", "defaultval": "NotSet"}
    iconf = {"environment": "prod", "product": "ccaconfig", "role": "config file"}
    oconf = {"environment": "pre-prod"}
    os.environ["CCACONFIG_ENVIRONMENT"] = "prod"
    confo = ccaConfig(appname="ccaconfig", defaultd=dconf, overrided=oconf)
    conf = confo.envOverride()
    assert conf["environment"] == "pre-prod"
