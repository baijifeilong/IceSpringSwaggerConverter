# Created by BaiJiFeiLong@gmail.com at 2021/12/7 18:05
import os
import shutil
from pathlib import Path

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
if Path("dist").exists():
    print("Folder dist exists, removing...")
    shutil.rmtree("dist")

if Path(f"{name}.7z").exists():
    print("Target archive exists, removing...")
    Path(f"{name}.7z").unlink()

print("\nBuilding jar...")
os.system("mvn -DskipTests package dependency:copy-dependencies")

print("\nPackaging...")
PyInstaller.__main__.run([
    "main.py",
    "--noconsole",
    "--noupx",
    "--name",
    name,
    "--ico",
    "resources/crown.ico"
])

print("\nCopying resources...")
shutil.copytree("resources", f"dist/{name}/resources")

print("\nRemoving unused resources...")
for file in Path(f"dist/{name}/resources").glob("**/*"):
    if file.name in ["crown.png"]:
        print(f"\tRemoving {file}...")
        file.unlink()

print("\nCopying JRE...")
shutil.copytree("jre", f"dist/{name}/jre")

print("\nCopying dependency jars...")
shutil.copytree("target/dependency", f"dist/{name}/jars")

print("\nCopying main jar...")
jar = next(Path("target").glob("swagger-converter*.jar"))
shutil.copy(jar, f"dist/{name}/jars")

print("\nCleaning...")
for file in Path("dist").glob("*/*"):
    if file.name in excluded_files:
        print(f"\tRemoving {file.name}...")
        file.unlink()

print("\nCompressing...")
os.system(f"cd dist && 7z a -mx=9 ../{name}.7z {name}")
