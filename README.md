# Denis's Automatic Markdown Parser To Pretty HTML

It is a Markdown to HTML parser, an HTML beautifier and a static site generator (ALL IN ONE!) written with built-in libraries and RegEx.

As for the why - I'm making my own [webpage](https://www.denislisunov.xyz) and I wanted to ease the pain of writing blog articles using pure html.

## Why not use Hugo?

Because It is always good important to understand what is under the hood.

## Version 2

* Now includes partials (0.01 alpha version)
* Pages now use the `body.html` and `head.html` templates by default
* Base template makes for more readable template setups
* Syntax changes from `{% key %}` to `{{ key }}`
* Automatic `index.html` generation for directories (see example1 in pages.json)

## Install & Generate

``` bash
#Install and Run
git clone https://github.com/NorthOC/damp2ph
cd ./damp2ph
python3 generator.py
```

## File structure

* `pages.json` - This file contains metadata about each page that will be generated
* `generator.py` - This is where the magic happens
* `templates/` - Html templates. Important ones are `base.html`, `body.html` and `head.html`
* `pages/` - This is the dir I chose for storing generated html examples (you can set your own)
* `content/` - This is the dir I chose for storing md content files (you can set your own)

## Examples

In the `index.html` you will find this README generated as an example. Other examples are included in `pages/` directory.

## Understanding how it works

Each page is stored in `pages.json` with data in the form of key:value pairs. 

To generate a page you need only three key value pairs: a base template aka. `base.html`, the body template aka. `body.html` and the head template `head.html` which can be found in the `/templates/` directory. In version 2, these templates are now set by default, so specification of templates is only required when you want to use a non default one.

## Predefined key value pairs

Here is a list of predefined key value pairs for a page:

* base_template - the `base.html` template
* head - the `head.html` template
* body - the `body.html` template
* title - is generated from an md file from Heading 1
* description or desc - is generated from an md file

These keys can also be set to your liking by stating them in `pages.json`

## Body

The body can use only one markdown file for content. There is no specified keyword for placing content in the body, thus you have to explicitly set the key value pair for content in the `pages.json` file and set the keyword in the body template as {{ keyword }}. It is best practices to just use 'content' as a keyword.

There are also string literal variables are denoted as {{= variable }}. The equals sign signifies to the compiler that this variable will be replaced with a value of a string found in the `pages.json` file. For example {{= title }} variable in the body will generate a title.

## Head

The head template only supports string literal variables, they are denoted as {{ variable }}.

## Automatic meta description and title

Each page generates an automatic description will automatically set the meta tag for description. To override this behavior for a specific page, set the "description" or "desc" key to anything (an empty string will do too!)

The title is generated as well, however, you have to place the title yourself. In case the Heading 1 cannot be found in the markdown file, the title will be set as "Untitled Document". To set your own title or to override this behavior for a page, set the "title" key to anything.

## Partials! (experimental)

Yep, you can now set partials in markdown files! Each partial takes 3 arguments (partial_file_name, no_of_times, data_file). An example of a partial:

&#123;&#123; `md_dir` `all` `pages.json` &#125;&#125;

This would take the `templates/partials/md_dir.html` file and generate all md file locations for each page in `pages.json`

&#123;&#123; `md_dir` `1` `pages.json` &#125;&#125;

This would only generate one location for one page

Partials are not user friendly yet and are subject to change