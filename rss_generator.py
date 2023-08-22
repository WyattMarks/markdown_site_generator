import urllib.request
contents = urllib.request.urlopen("http://wyattmarks.com/index.html").read().splitlines() # Currently just GETing the HTML file, need to integrate into the generator
import re
import datetime
from email.utils import format_datetime


BASE_URL = "https://wyattmarks.com/"
TITLE = "wyattmarks.com"
DESCRIPTION = "Wyatt Marks' Blog"



rss = f"""
<rss version="2.0">
<channel>
<title>{TITLE}</title>
<link>{BASE_URL}</link>
<description>{DESCRIPTION}</description>

"""

insidePost = False

for line in contents:
    if b'id="post' in line:
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

    elif b'id="date' in line:

        date = re.search('">(.*)</h', str(line)).group(1)
        dt = datetime.datetime.strptime(date, "%m/%d/%y") # Thankfully does not assume 1900s
        date = format_datetime(dt) # RFC 822 format

        rss += "\t<pubDate>" + date + "</pubDate>\n"
        rss += "\t<description><![CDATA[\n"
    elif insidePost:
        try:
            rss += "\t\t" + line.decode('utf-8') + "\n"
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


with open('rss.xml', 'wb') as f:
    f.write(rss.encode())
