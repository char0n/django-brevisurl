from django.utils import importlib


def load_object(import_path):
    """Util for importing objects from import path.

    :param import_path: import path of object to be imported e.g. module.submodule.Class
    :type import_path: string
    :returns: imported object
    :rtype: object
    :raises: ValueError, ImportError, AttributeError

    """
    if not (isinstance(import_path, basestring) and '.' in import_path):
        raise ValueError('There must be at least one dot in import path: "%s"', import_path)
    module_name, object_name = import_path.rsplit('.', 1)
    module = importlib.import_module(module_name)
    return getattr(module, object_name)