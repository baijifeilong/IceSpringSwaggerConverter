# Created by BaiJiFeiLong@gmail.com at 2021/12/8 11:26
import logging
import os
from pathlib import Path

import colorlog

consolePattern = "%(log_color)s%(asctime)s %(levelname)8s %(name)-10s %(message)s"
logging.getLogger().handlers = [logging.StreamHandler()]
logging.getLogger().handlers[0].setFormatter(colorlog.ColoredFormatter(consolePattern))
logging.getLogger().setLevel(logging.DEBUG)

logging.info("Maven packaging...")
os.system("mvn -DskipTests package")

logging.info("Removing tmp directory if exists...")
os.system("busybox rm -rf target/tmp")
logging.info("Uncompressing target jar...")
os.system("7z x target/*.jar -otarget/tmp")

logging.info("Removing jars directory if exists...")
os.system("busybox rm -rf jars")
logging.info("Creating jars directory if exists...")
os.system("busybox mkdir -p jars")

jarBase = next(Path("target").glob("*.jar.original")).name[:-len(".jar.original")]
logging.info("Copying main jar %s.jar...", jarBase)
os.system(f"busybox cp target/{jarBase}.jar.original jars/{jarBase}.jar")
logging.info("Copying dependencies...")
os.system("busybox cp -r target/tmp/BOOT-INF/lib/*.jar jars")

logging.info("Done.")
