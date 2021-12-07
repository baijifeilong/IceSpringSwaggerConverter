# Created by BaiJiFeiLong@gmail.com at 2021/12/7 18:05
import os
import pathlib
import shutil

import PyInstaller.__main__

name = "IceSpringSwaggerConverter"

excluded_files = """
Qt5DataVisualization.dll
Qt5Pdf.dll
Qt5Quick.dll
Qt5VirtualKeyboard.dll
d3dcompiler_47.dll
libGLESv2.dll
opengl32sw.dll
""".strip().splitlines()

print("Building...")
if pathlib.Path("dist").exists():
    print("Folder dist exists, removing...")
    shutil.rmtree("dist")

if pathlib.Path(f"{name}.7z").exists():
    print("Target archive exists, removing...")
    pathlib.Path(f"{name}.7z").unlink()

print("\nBuilding jar...")
os.system("mvn package -DskipTests")

print("\nPacking...")
PyInstaller.__main__.run([
    "main.py",
    "--noconsole",
    "--noupx",
    "--name",
    name,
    "--ico",
    "resources/crown.ico",
    "--add-data",
    "resources;resources",
])

print("\nCopying JRE...")
shutil.copytree("jre", f"dist/{name}/jre")

print("\nCopying jar...")
jar = list(pathlib.Path(".").glob("**/swagger-converter*.jar"))[0]
shutil.copy(jar, f"dist/{name}")

print("\nCleaning...")
for file in pathlib.Path("dist").glob("*/*"):
    if file.name in excluded_files:
        print(f"Removing {file.name}")
        file.unlink()

print("\nCompressing...")
os.system(f"cd dist && 7z a -mx=9 ../{name}.7z {name}")
