# Denis's Automatic Markdown Parser To Pretty HTML (damp2ph)

My biggest project so far.

It is a Markdown parser + Static site generator + HTML beautifier (ALL IN ONE!) written with built-in libraries and RegEx.

As for the why - I'm making my own [webpage](https://www.denislisunov.xyz).

## Version 3.0

* Different page groups can now set different default templates in `config/defaults.json`
* Now includes automatic clean-up of previously generated pages from a generated `config/indexer.txt` file
* Head template variables are now properly set with &#123;&#123;= variable &#125;&#125; instead of &#123;&#123; variable &#125;&#125;;

## Version 2.0

* Now includes partials (0.01 alpha version)
* Pages now use the `body.html` and `head.html` templates by default
* Base template makes for more readable template setups
* Syntax changes from `{% key %}` to `&#123;&#123; key &#125;&#125;`
* Automatic `index.html` generation for directories (see example1 in /config/pages.json)

## Install & Generate

``` bash
#Install and Run
git clone https://github.com/NorthOC/damp2ph
cd ./damp2ph
python3 generator.py
```

## File structure

* `generator.py` - This is the engine
* `config/defaults.json` - set default templates for each group of pages.
* `config/pages.json` - This is a page group file and contains metadata for each page.
* `templates/` - Html templates. Important ones are `base.html`, `body.html` and `head.html`. All other ones are optional.
* `templates/partials` - This is where the partials are stored.
* `pages/` - This is the dir I chose for storing generated html examples (you can set your own in a page group json file)
* `content/` - This is the dir I chose for storing md content files (you can set your own in a page group json file)

## Examples

Examples are included in `pages/` directory.

## Understanding how it works

Each page is stored in `pages.json` with data in the form of key:value pairs. 

To generate a page you need only three key value pairs: a base template aka. `base.html`, the body template aka. `body.html` and the head template `head.html` which can be found in the `/templates/` directory. In version 3, these templates are not set by default. You need to set them in `config/defaults.json` for each page group.

## Predefined key value pairs

Here is a list of predefined key value pairs for a page:

* base_template - the `base.html` template
* head - the `head.html` template
* body - the `body.html` template
* title - is generated from an md file from Heading 1
* description or desc - is generated from an md file
* og-img - is generated from the first image encountered on a page or is set to none.

To overwrite these parameters for a page, you have to set them explicitly for each page.

## Body variables

The body can use only one markdown file for content. There is no specified keyword for placing content in the body, thus you have to explicitly set the key value pair for content in the `pages.json` file and set the keyword in the body template as &#123;&#123; keyword &#125;&#125;. It is best practices to just use 'content' as a keyword.

There are also string literal variables which are denoted as &#123;&#123;= variable &#125;&#125;. The equals sign signifies to the compiler that this variable will be replaced with a value of a string found in the specified page group file. For example &#123;&#123;= title &#125;&#125; variable in the body will generate a title.

## Head variables

The head template only supports string literal variables. As of version 3.0, they are denoted as &#123;&#123;= variable &#125;&#125;.

## Automatic meta description, title and og image

Each page generates an automatic description and will automatically set the meta tag for description. To override this behavior for a specific page, set the "description" or "desc" key to anything (an empty string will do too!)

The title is generated as well, however, you have to place the title yourself. In case the Heading 1 cannot be found in the markdown file, the title will be set as "Untitled Document". To set your own title or to override this behavior for a page, set the "title" key to anything.

An og image is generated from the first encountered image in a content document. To override this behavior set the "og-img" variable to anything.

## Partials! (experimental)

Yep, you can now set partials in markdown files! Each partial takes 3 arguments (partial_file_name, no_of_times, data_file). An example of a partial:

&#123;&#123; `md_dir` `all` `pages.json` &#125;&#125;

This would take the `templates/partials/md_dir.html` file and generate all content file paths with which each page is generated with in `pages.json`

&#123;&#123; `md_dir` `1` `pages.json` &#125;&#125;

This would only generate one location for one page

Partials are not user friendly yet and are subject to change