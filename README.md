This is a simple website generator. 
It uses:
- Python
- Node
- [highlight.js's css](https://highlightjs.org/)
- [github-markdown-css](https://github.com/sindresorhus/github-markdown-css)

and these npm packages:
- [showdown](https://github.com/showdownjs/showdown/)
- [showdown-highlight](https://github.com/Bloggify/showdown-highlight)


Also, it supports some custom tag options. You can tag h2 with {post} in order to get rid of the underline and bottom padding
You can tag h6 with {date} in order to get rid of the upper margin. This lets you do
```markdown
## Some post {post}
###### 05-22-22 {date}
```
and get a decent looking post title, with date.

You can also write <!header!> and it will automatically insert the header.md there.

<!pages!> will generate a list of pages on your website, generally for use in header.md

<!posts!> will generate a compilation of all the posts in 'posts'. This should have an option for size limits, but since I don't have many posts I decided it was okay for now. Also, it lists the posts based on file modification date, not the date in the file. Maybe this should change.

<!base_url!> will insert the variable BASE_URL in the python script in that spot. Useful for when you're doing local testing, and want the autogenerated links to work

<!this_page!> will insert the link to this page (or this post, if being generated in <!posts!>)