contents = open("output/index.html", encoding="utf8").readlines()
import re
import datetime
from email.utils import format_datetime


BASE_URL = "https://example.com/"
TITLE = "Example Blog"
DESCRIPTION = "Full of examples"


def generate(title, base_url, description):
    rss = f"""
    <rss version="2.0">
    <channel>
    <title>{title}</title>
    <link>{base_url}</link>
    <description>{description}</description>

    """

    insidePost = False

    for line in contents:
        line = line
        if 'id="post' in line and 'h2' in line:
            if insidePost:
                rss += "\t]]></description>\n"
                rss += "</item>\n"

            insidePost = True
            rss += "<item>\n"

            post_name = re.search('.html">(.*)</a>', str(line)).group(1)
            link = re.search('href="(.*)">', str(line)).group(1)

            rss += "\t<title>" + post_name + "</title>\n"
            rss += "\t<link>" + link + "</link>\n"
            rss += '\t<guid isPermaLink="true">' + link + '</guid>\n'

        elif 'id="date' in line and 'h6' in line:

            date = re.search('">(.*)</h', str(line)).group(1)
            dt = datetime.datetime.strptime(date, "%m/%d/%y") # Thankfully does not assume 1900s
            date = format_datetime(dt) # RFC 822 format

            rss += "\t<pubDate>" + date + "</pubDate>\n"
            rss += "\t<description><![CDATA[\n"
        elif insidePost:
            try:
                rss += "\t\t" + line + "\n"
            except Exception as e:
                print(line)
                print(e)

    # End item entry
    if insidePost:
        rss += "\t]]></description>\n"
        rss += "</item>\n"


    # End RSS feed
    rss += "</channel>\n"
    rss += "</rss>\n"

    return rss.encode()
    


if __name__ == "__main__":
    with open('rss.xml', 'wb') as f:
        f.write(generate(TITLE, BASE_URL, DESCRIPTION))
