import imp
import os

import logging
logger = logging.getLogger()


def load_module(module_type, config, base_path, verify_clz):

    try:
        # try local directory path first using base_path for non-installed packages
        res = imp.find_module(module_type, [base_path])
    except ImportError:
        try:
            # try installed modules rooted at base_path
            res = imp.find_module(base_path + '/' + module_type)
        except ImportError:
            # look system-wide
            res = imp.find_module(module_type)

    (fileobj, pathname, description) = res
    try:
        mod = imp.load_module(module_type.replace('/', '.'), fileobj, pathname, description)

        mod_name = os.path.splitext(os.path.basename(module_type))[0]
        clz = getattr(mod, mod_name)
        module = clz(**config)

        # verify the class is the correct type
        if not isinstance(module, verify_clz):
            raise Exception(mod_name + " is not an instance of " + verify_clz.__name__)

        return module

    finally:
        if fileobj:
            fileobj.close()