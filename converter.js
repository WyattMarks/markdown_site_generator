const cli = require("commander");
const fs = require('fs');
const showdown = require('showdown');
const showdownHighlight = require("showdown-highlight");



cli.parse();

pre_html = "";
post_html = "";

//Load static HTML stuff
try {
    pre_html = fs.readFileSync('static/static_pre.html', 'utf8');
} catch (err) {
    console.error(err);
    return;
}

try {
    post_html = fs.readFileSync('static/static_post.html', 'utf8');
} catch (err) {
    console.error(err);
    return;
}


//Load the file we're converting
try {
    data = fs.readFileSync(cli.args[0], 'utf8');
    let converter = new showdown.Converter({
        extensions: [showdownHighlight({ pre: true })]
    });

    converter.setOption('customizedHeaderId', true);
    converter.setOption('strikethrough', true);
    converter.setOption('emoji', true);

    //Convert and write the file
    data = pre_html + converter.makeHtml(data) + post_html;
    fs.writeFileSync(cli.args[1], data);

} catch (err) {
    console.error(err);
    return;
}