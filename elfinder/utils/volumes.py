#from django.utils.importlib import import_module
from importlib import import_module
from elfinder.conf import settings as ls 
import logging
from lib.log import log
from config.views import get_dir

def get_path_driver(hash_, optionset):
    """
    Given an ``optionset`` and a path ``hash_`` this function returns
    a mounted volume driver for this path.
    
    This method assumes that the driver uses the default driver 
    :func:`elfinder.volumes.base.ElfinderVolumeDriver.id` implementation
    to generate its id.
    """
    for root_options in ls.ELFINDER_CONNECTOR_OPTION_SETS[optionset]['roots']:
        if 'driver' in root_options:
            if hash_.startswith('%s%s_' % (root_options['driver']._driver_id, root_options['id'])):
                return instantiate_driver(root_options)

 
def instantiate_driver(root_options):
    """
    Instantiate and return a  driver, given its ``root_options``.
    """
    class_ = root_options['driver'] if 'driver' in root_options else ''
    logging.info("---a-----")
    if 'driverInstance' in root_options and isinstance(root_options['driverInstance'], class_):
        return root_options['driverInstance']

    if isinstance(class_, basestring) and class_:
        try:
            logging.info("---b-----")
            split = class_.split('.')
            storage_module = import_module('.'.join(split[:-1]))
            volume = getattr(storage_module, split[-1])()
        except:
            raise Exception('Could not import driver "%s"' % class_)
    else:
        try:
            logging.info("---c-----")
            volume = class_()
        except TypeError:
            raise Exception('Driver "%s" does not exist' % class_)

    try:
        logging.info("---d-----")
        volume.mount(root_options)
    except Exception as e:
        logging.info("---e-----")
        raise Exception('Driver "%s" " %s' % (class_, e))

    #store driver instance in memory, if the 'keepAlive' option is set
    if 'keepAlive' in root_options and root_options['keepAlive']:
        logging.info("---f-----")
        root_options['driverInstance'] = volume

    return volume
