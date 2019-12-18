# ccaConfig

a config file utility. Will read yaml formatted config files from various
locations in the following order, so that the 'nearer' files override the
further ones.  Finally, it checks the environment for variables and
overrides any set in the config file.

The order of files to read is
```
/etc/appname.yaml
/etc/appname/appname.yaml
$HOME/.config/appname.yaml
$HOME/.appname.yaml
$(pwd)/appname.yaml
```

Any environment variables of the form

```
APPNAME_VARIABLENAME
```

will be found, chopped at the underscore, lower cased and set into the
final configuration.

## Usage
```
from ccaconfig import ccaConfig

confo = ccaConfig(appname="appname")
config = confo.envOverride()
```

or, to not take environment variables into account:
```
from ccaconfig import ccaConfig

confo = ccaConfig(appname="appname")
config = confo.findConfig()
```

Two additional dictionaries can be supplied, the first `defaultd` can be
used to set a default config, and the 2nd, `overrided` can be used for
config variables that you do not want overridden by any config file found
or from the environment.

```
from ccaconfig import ccaConfig

defd = {"environment": "dev"}
overd = {"product": "myapp"}
confo = ccaConfig(appname="appname", defaultd=defd, overrided=overd)
config = confo.envOverride()
# config["environment"] == "dev" if it is not overridden by a subsequent
# config file or from and environment variable
#
# config["product"] == "myapp" and will not be overridden, at all
```
