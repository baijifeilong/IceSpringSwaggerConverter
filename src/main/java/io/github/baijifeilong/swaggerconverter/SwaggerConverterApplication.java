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
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;

@Slf4j
public class SwaggerConverterApplication {
    public static void main(String[] args) {
        System.out.println(swaggerToHtml(args[0]));
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
