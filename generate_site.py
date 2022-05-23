import os
import re
import subprocess
from shutil import copy2, rmtree
import glob

BASE_URL = "file:///home/lord/Documents/markdown_site_generator/output"

def specialOperation(operation, currentPage):
    if operation == "pages":
        return generate_pages(currentPage)
    elif operation == "header":
        return generate_header(currentPage)
    elif operation == "posts":
        return generate_posts()
    elif operation == "base_url":
        return BASE_URL
    elif operation == "this_page":
        return f"{BASE_URL}/{currentPage[0:-3]}.html"


def generate_posts(separator="<br/><br/><br/>\n"):
    posts = ''
    files = list(filter(os.path.isfile, glob.glob('posts/' + "*")))
    files.sort(key=lambda x: os.path.getmtime(x))

    files.reverse()

    for filename in files: 
        filename = filename.replace('posts/', '')
        posts += preprocess('posts/', filename, write=False) + separator

    return posts

def generate_pages(currentPage, separator=' &nbsp; '):
    pages = ''
    currentPage = currentPage[0:-3].capitalize()

    def handle_page(dir, filename):
        f = f"{dir}/{filename}"
        if os.path.isfile(f):
            pageName = filename[0:-3]
            capitalPage = pageName.capitalize()
            if capitalPage == currentPage:
                return currentPage + separator
            else:
                return f"[{capitalPage}]({BASE_URL}/{pageName}.html)" + separator

    #Index page should be first in list
    pages += handle_page("pages", "index.md")

    for filename in os.listdir('pages'): 
        f = f"pages/{filename}"
        if filename != "index.md":
            pages += handle_page("pages", filename)

    # Some static page entries, for offsite things
    pages += "[GitHub](https://github.com/WyattMarks)"

    return pages

def generate_header(currentPage):
    return preprocess('', "header.md", write=False, currentPage=currentPage)

def preprocess(dir, file, write=True, currentPage=None):
    if currentPage == None:
        currentPage = file

    f = open(f"{dir}{file}", 'r')
    contents = ""

    for line in f.readlines():
        if "<!" in line:
            results = re.search('<!(.*)!>', line)
            for result in results.groups():
                line = re.sub(f"<!{result}!>", specialOperation(result, currentPage), line)
        contents += line

    f.close()
    if write:
        f = open(f"{dir}{file}", 'w')
        f.write(contents)
        f.close()

    return contents


def generate_site():
    #Remove old output
    try:
        rmtree('output')
    except:
        pass

    os.mkdir('output')

    #Create temp dir
    try:
        rmtree('temp_md_files')
    except:
        pass
    os.mkdir('temp_md_files')
    

    #Copy over files
    for filename in os.listdir('pages'):
        f = f"pages/{filename}"
        if os.path.isfile(f):
            copy2(f, f"temp_md_files/{filename}")

    for filename in os.listdir('posts'):
        f = f"posts/{filename}"
        if os.path.isfile(f):
            copy2(f, f"temp_md_files/{filename}")
            f = f"temp_md_files/{filename}"
            # We want the header to show up on posts, as well, but only when on their dedicated page.
            t = open(f, 'r')
            contents = t.read()
            t.close()
            contents = "<!header!>\n" + contents
            t = open(f, 'w')
            t.write(contents)
            t.close()

    #Process each file
    for filename in os.listdir('temp_md_files'):
        f = f"temp_md_files/{filename}"
        if os.path.isfile(f):
            preprocess("temp_md_files/", filename)
            subprocess.run(["node", "converter.js", f, f"output/{filename[0:-3]}.html"])

    #Copy CSS files over
    copy2("static/github-dark.css", "output")
    copy2("static/github-markdown-dark.css", "output")
    copy2("static/style.css", "output")
            

    #Delete temp files
    rmtree('temp_md_files')
        



if __name__ == "__main__":
    generate_site()