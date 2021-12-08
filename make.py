# Created by BaiJiFeiLong@gmail.com at 2021/12/7 18:05
import logging
import os
from pathlib import Path

import PyInstaller.__main__
import colorlog

consolePattern = "%(log_color)s%(asctime)s %(levelname)8s %(name)-10s %(message)s"
logging.getLogger().handlers = [logging.StreamHandler()]
logging.getLogger().handlers[0].setFormatter(colorlog.ColoredFormatter(consolePattern))
logging.getLogger().setLevel(logging.DEBUG)

name = "IceSpringSwaggerConverter"

excluded_files = """
Qt5DataVisualization.dll Qt5Pdf.dll Qt5Quick.dll Qt5VirtualKeyboard.dll
d3dcompiler_47.dll libGLESv2.dll opengl32sw.dll crown.png
""".strip().split()

logging.info("Removing dist folder if exists...")
os.system("busybox rm -rf dist")
logging.info(f"Removing {name}.7z if exists...")
os.system(f"busybox rm -rf {name}.7z")

command = f"main.py --noconsole --noupx --name {name} --ico resources/crown.ico " \
          f"--add-data resources;resources --add-data jre;jre --add-data jars;jars"
logging.info("Executing PyInstaller...")
PyInstaller.__main__.run(command.split())

logging.info("Cleaning...")
for file in Path("dist").glob("**/*"):
    if file.name in excluded_files:
        logging.debug(f"Removing %s...", file.name)
        file.unlink()

logging.info("Compressing...")
os.system(f"cd dist && 7z a -mx=9 ../{name}.7z {name}")

logging.info("Done.")
