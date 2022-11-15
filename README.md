# Denis's Automatic Markdown Parser To Pretty HTML

It is a Markdown to HTML parser, an HTML beautifier and a static site generator (ALL IN ONE!) written with built-in libraries using a ton of RegEx.

As for the why - I'm making my own [webpage](https://www.denislisunov.xyz) and I wanted to ease the pain of writing blog articles using pure html.

## Install & Generate

``` bash
# Install
git clone https://github.com/NorthOC/damp2ph
# run
cd ./damp2ph
python3 generator.py
```

## Examples

In the `index.html` you will find this README generated as an example. Other examples are included in `pages/` directory. Feel free to explore and ask any questions if needed.

## Understanding how it works

The generator requires only three things: a head template, a body template and a markdown file with content.

In short, the markdown file is processed into a html body blob. After that, the head blob is generated based on the template. Then both blobs are written to a file and a beautifier is applied.

There are only three reserved keywords: title, head and body.

* title - the page title
* head - the head template
* body - the body template

You could even generate pages without markdown files.

Template variables are stored in `pages.json` in the form of key:value pairs (variable_name: string). 

### Body

The body template can have two different types of variables: string literal and html. 

In the body templates, the string literal variables are denoted as `{%= variable %}`. The equals sign signifies to the compiler that this variable will be replaced with a value of a string found in the `pages.json` file.

The html variables in body templates are denoted as `{% variable %}`. The compiler will then generate html code and input that code into the template where the variable is written. For such a variable, the location of the markdown file needs to be provided in `pages.json`.

### Head

The head template only supports string literal variables, however, they are denoted as `{% variable %}`. This design is subject to change.

If your head template contains the keyword `{% description %}`, you need to provide the same key : value pair to your `pages.json` file. Example: `'description': 'my example of something here'`

### Automatic meta description

The reason body templates are processed first, is to generate meta descriptions. In order to disable or override this feature, include a key:value pair in your `pages.json` either featuring the key `desc` or `description` with any value. The compiler knows not to generate an automatic meta description for a url which includes one of these keys.