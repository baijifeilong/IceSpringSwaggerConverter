"""
Created by BaiJiFeiLong@gmail.com at 2021/12/9 19:43
"""

import logging
import os
from pathlib import Path

import colorlog

consolePattern = "%(log_color)s%(asctime)s %(levelname)8s %(name)-10s %(message)s"
logging.getLogger().handlers = [logging.StreamHandler()]
logging.getLogger().handlers[0].setFormatter(colorlog.ColoredFormatter(consolePattern))
logging.getLogger().setLevel(logging.DEBUG)

logging.info("Maven cleaning...")
os.system("mvn clean") and exit(-1)

logging.info("Maven packaging...")
os.system("mvn package -DskipTests") and exit(-1)

jar = next(Path().glob("target/swagger-converter-*-SNAPSHOT.jar")).absolute()
logging.info("Generated jar: %s", jar)

logging.info("Creating target/tmp directory...")
os.system("busybox mkdir target/tmp") and exit(-1)

logging.info("Entering target/tmp directory...")
os.chdir("target/tmp")

logging.info("Uncompressing jar file...")
os.system(f"7z x {jar}") and exit(-1)

logging.info("Recreating jar again...")
os.system(f"7z a -tzip -mx=0 {jar.name} .") and exit(-1)

logging.info("Returning to previous directory...")
os.chdir("../..")

logging.info("Removing JRE if exists...")
os.system("busybox rm -rf jre") and exit(-1)

jlink = Path(r"~\scoop\apps\openjdk11\current\bin\jlink.exe").expanduser()
logging.info("jlink: %s", jlink)

modules = "java.base,java.compiler,java.desktop,java.logging,java.management,java.naming,java.scripting,java.sql," \
          "java.xml,jdk.unsupported"
logging.info("Creating jre...")
os.system(f"{jlink} --add-modules {modules} --strip-debug --output jre --verbose") and exit()

jre = Path("jre/bin/java")
logging.info("Created jre: %s", jre)
os.system(f"{jre} -version") and exit()

logging.info("Done.")
