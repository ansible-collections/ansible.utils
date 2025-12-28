#
# Capture any deprecation warnings of e.g. ansible.module_utils for pytest
#
import warnings

import ansible.utils.display


ansible.utils.display.Display().deprecated = lambda msg, *args, **kwargs: warnings.warn(
    msg,
    DeprecationWarning,
    stacklevel=3,
)
