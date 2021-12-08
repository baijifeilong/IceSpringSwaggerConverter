package io.github.baijifeilong.swaggerconverter;

import io.github.swagger2markup.Swagger2MarkupConverter;
import lombok.SneakyThrows;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.io.FileUtils;
import org.asciidoctor.Asciidoctor;
import org.asciidoctor.Attributes;
import org.asciidoctor.Options;
import org.asciidoctor.Placement;

import java.io.File;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Scanner;

@Slf4j
public class SwaggerConverterApplication {
    @SneakyThrows
    public static void main(String[] args) {
        String text = new Scanner(new URL(args[0]).openStream(), "UTF-8").useDelimiter("\\A").next();
        System.out.println(swaggerToHtml(text));
    }

    @SneakyThrows
    public static String swaggerToHtml(String swagger) {
        Path tmp = Files.createTempFile(null, null);
        String markup = Swagger2MarkupConverter.from(swagger).build().toString();
        FileUtils.writeStringToFile(tmp.toFile(), markup, StandardCharsets.UTF_8);
        Asciidoctor.Factory.create().convertFile(tmp.toFile(), Options.builder().attributes(Attributes.builder()
                .linkCss(false).sectionNumbers(true).tableOfContents(Placement.LEFT).build()).build());
        log.debug("Temporary html file: {}", tmp.toString().replace(".tmp", ".html"));
        return FileUtils.readFileToString(new File(tmp.toString().replace(".tmp", ".html")), StandardCharsets.UTF_8);
    }
}
