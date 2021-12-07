import urllib.request
from pathlib import Path

import jpype

url = "http://localhost:8080/v2/api-docs"
text = urllib.request.urlopen(url).read().decode("utf8")
jars = ";".join(map(str, Path("target").glob("**/*.jar")))
jvm = str(list(Path().glob("**/jvm.dll"))[-1])
jpype.startJVM(jvm, "-ea", f"-Djava.class.path={jars}")
className = "io.github.baijifeilong.swaggerconverter.SwaggerConverterApplication"
clazz = jpype.JClass(className)
html = clazz.swaggerToHtml(text)
print(html[:100])
