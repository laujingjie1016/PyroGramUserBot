import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


def __list_all_modules():
    import glob
    from os.path import basename, dirname, isfile

    mod_paths = glob.glob(dirname(__file__) + "/*.py")
    return [
        basename(f)[:-3]
        for f in mod_paths
        if isfile(f) and f.endswith(".py") and not f.endswith("__init__.py")
    ]


ALL_MODULES = sorted(__list_all_modules())
logger.info("Modules to load:\n{}\n".format(", ".join(ALL_MODULES)))
__all__ = ALL_MODULES + ["ALL_MODULES"]
