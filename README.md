# Denis's Automatic Markdown Parser To Pretty HTML

## What it does? What it is? Why?

Parses `pages.json` -> selects template files and content based on set params -> generates `.html` files -> formats them for human readability

It is a markdown parser and html formatter written from scratch using a ton of RegEx.

As for the why - I'm making my own (webpage)[denislisunov.xyz] and I wanted to ease the pain of writing blog articles using pure html.

## Install

``` bash
git clone https://github.com/NorthOC/damp2ph
cd ./damp2ph
python generate.py
```

## Examples

In the `index.html` you will find this README generated as an example. Other examples are included in `pages/` directory

## Understanding what is where

HTML code consists of two sections: head and body. The templates for these are stored in `templates/`
The compiler will fill out each variable you provide in the template (example of variable `{% author %}`)

To create a page, all you need to do is pass in the head and body templates to the `pages.json` file in such format:

``` json
output-filename.html: {
    'head': 'path to head template',
    'body': 'path to body template',
}
```

all other keywords in the json file, for each page, depend on your template keywords. 

body and head templates are generated seperately

If your head template contains the keyword `{% description %}`, you need to provide the same parameter to your `pages.json` file in the form of `'description': 'my example of something here'`

Every param that is in the body (except for title) is set to compile markdown text to html.

The `generator.py` contains the source code functions.

The `generate.py` generates the pages using those functions.

I prefer to store my generated pages in `pages/` directory, but you can store it anywhere, based on the provided `output-filename.html` in your `pages.json` file.