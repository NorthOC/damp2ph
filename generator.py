import json
import re
import unicodedata

# parse json file
def parsePages(jsonFile):
    """returns the contents of a .json file\n
    structure of json objects:\n
    output.html{
        head: "path to head template",
        body: "path to body template",
        content: "path to content",
    }
    """
    with open(jsonFile, 'r') as file:
        data = json.load(file)
        # Sets title param from h1 if title is not specifiend in pages.json
        for item in data:
            if 'title' not in data[item]:
                with open(data[item]["content"], 'r', encoding='utf-8') as f:
                    lines = f.read().split("\n")
                    for line in lines:
                        title = re.search("^# (.*)", line)
                        if title != None:
                            data[item]['title'] = title.group(1)
                            break
                        else:
                            data[item]['title'] = "Untitled Document"
        return data

def mdToWeb(mdFile):
    """takes a .md file and returns a compiled HTML string"""

    h_tags = [["# ", "h1"], ["## ", "h2"], 
    ["### ", "h3"], ["#### ", "h4"], ["##### ", "h5"], ["###### ", "h6"]]

    with open(mdFile, 'r', encoding="utf-8") as file:
        data = file.read()

    # process images
    images = re.findall("!\[(.*?)\]\((.*?)\)", data)

    for touple in images:
        md_tag = f"![{touple[0]}]({touple[1]})"
        image_tag = f"<figure>\n<img src=\"{touple[1]}\" alt=\"{touple[0]}\"/>\n<figcaption>{touple[0]}</figcaption>\n</figure>"
        data = data.replace(md_tag, image_tag)
    
    # process links
    links = re.findall("\[(.*?)\]\((.*?)\)", data)
    for touple in links:
        md_tag = f"[{touple[0]}]({touple[1]})"
        link_tag = f"<a href=\"{touple[1]}\">{touple[0]}</a>"
        data = data.replace(md_tag, link_tag)
    data = data.split("\n\n")

    for line in data:

        # html code
        if line.startswith("<") and not line.startswith("<a "):
            pass

        # ordered lists
        elif line.startswith("1. "):
            new_list = []
            new_string = ""
            current_depth = 0
            prev_depth = 0

            # single line contains full list
            listing = line.split("\n")
            for item in listing:
                ol_list = item.split(". ")
                current_depth = len(ol_list[0])

                # beginning of list
                if prev_depth == 0 and len(ol_list[0]) == 1:
                    new_list.append(f"<ol>\n<li>{ol_list[1]}</li>\n")

                # extra spacing before list item means nested
                elif current_depth > prev_depth:
                    new_list.append(f"<ol>\n<li>{ol_list[1]}</li>\n")

                # nested list ends
                elif current_depth < prev_depth:
                    last_item = str(new_list.pop())
                    last_item = last_item + "</ol>\n"
                    new_list.append(last_item)                
                    new_list.append(f"<li>{ol_list[1]}</li>\n")

                # just list item
                else:
                    new_list.append(f"<li>{ol_list[1]}</li>\n")
                prev_depth = current_depth
            # list end
            new_list.append("</ol>")

            # replace markdown with html
            for thing in new_list:
                new_string += thing
            data[data.index(line)] = new_string

        # Unordered list
        elif line.startswith("* "):
            temp = line.split("\n")
            new_list = []
            started = False
            new_string = ""
            current_depth = 0
            prev_depth = 0
            for item in temp:
                ul_list = re.findall("^(\s*?)(\* )(.*)", item)
                current_depth = len(ul_list[0][0])
                if not started and prev_depth == 0 and len(ul_list[0][0]) == 0:
                    new_list.append(f"<ul>\n<li>{ul_list[0][2]}</li>\n")
                    started = True
                elif current_depth > prev_depth:
                    new_list.append(f"<ul>\n<li>{ul_list[0][2]}</li>\n")
                elif current_depth < prev_depth:
                    last_item = str(new_list.pop())
                    last_item = last_item + "</ul>\n"
                    new_list.append(last_item)                
                    new_list.append(f"<li>{ul_list[0][2]}</li>\n")
                else:
                    new_list.append(f"<li>{ul_list[0][2]}</li>\n")
                prev_depth = current_depth
            new_list.append("</ul>")
            for thing in new_list:
                new_string += thing
            data[data.index(line)] = new_string

        # code blocks
        elif line.startswith("```"):

            # escape html
            comment = re.findall("(\/\/.*|#.*)", line)
            temp = line.replace("&", "&amp;").replace("<", "&lt;")\
                .replace(">", "&gt;").replace("\"", "&quot;").replace("\'", "&#39;")
            for touple in comment:
                temp = temp.replace(touple, f"<span class=\"comment\">{touple}</span>")
            new_list = []
            new_string = ""
            temp = temp.split("\n")
            started = False
            for code_line in temp:

                if not started:
                    # check if language is specified next to code block
                    code_class = code_line.split(" ")

                    if len(code_class) == 2:
                        new_list.append(f"<code class=\"{code_class[1]} code-block\">\n")
                    else:
                        new_list.append("<code class=\"code-block\">\n")
                    started = True
                elif code_line == "```":
                    new_list.append("</code>")
                else:
                    new_list.append(f"<pre>{code_line}</pre>\n")

            for thing in new_list:
                new_string += thing
            data[data.index(line)] = new_string

        # headings
        elif line.startswith("#"):
            for i in range(len(h_tags)):
                # remove all h1 tags for SEO and because it is in params[title]
                if line.startswith(h_tags[i][0]):
                    index = data.index(line)
                    if h_tags[i][0] == h_tags[0][0]:
                        data[index] = ''
                        break
                    else:
                        #create heading id for on-page link bookmarks
                        id_heading = line[len(h_tags[i][0]):].lower()
                        normalized = unicodedata.normalize('NFD', id_heading)
                        decoded = u"".join([c for c in normalized if not unicodedata.combining(c)])
                        h_id = re.sub(r"[^a-zA-Z0-9]+", ' ', decoded).strip().replace(" ", "_")

                        html_open_tag = "<" + h_tags[i][1] + f" id=\"{h_id}\">"
                        html_close_tag = "</" + h_tags[i][1] + ">"
                        line = line.replace(h_tags[i][0], html_open_tag, 1) + html_close_tag
                        data[index] = line
                        break

        # inline and p tags
        else:
            temp = line
            bold_italic = re.findall("(\*\*\*)(.*?)(\*\*\*)", temp)

            if len(bold_italic) != 0:
                for touple in bold_italic:
                    temp = temp.replace(\
                        touple[0] + touple[1] + touple[2], f"<strong><em>{touple[1]}</em></strong>")

            bold = re.findall("(\*\*)(.*?)(\*\*)", temp)

            if len(bold) != 0:
                for touple in bold:
                    temp = temp.replace(\
                        touple[0] + touple[1] + touple[2], f"<strong>{touple[1]}</strong>")

            italic = re.findall("(\*)(.*?)(\*)", temp)

            if len(italic) != 0:
                for touple in italic:
                    temp = temp.replace(\
                        touple[0] + touple[1] + touple[2], f"<em>{touple[1]}</em>")

            strikethrough = re.findall("(~~)(.*?)(~~)", temp)

            if len(strikethrough) != 0:
                for touple in strikethrough:
                    temp = temp.replace(\
                        touple[0] + touple[1] + touple[2], f"<s>{touple[1]}</s>")

            inline_code = re.findall("(`)([^`]{1}.*?)(`)", temp)

            if len(inline_code) != 0:
                for touple in inline_code:
                    temp = temp.replace(\
                        touple[0] + touple[1] + touple[2], f"<code>{touple[1]}</code>")

            data[data.index(line)] = f"<p>{temp}</p>"
    
    data_string = ''
    for item in data:
        if item != '<p></p>' and item != '':
            data_string += item + "\n"
    #print(data_string)
    return data_string
        

# static site generator
def generateHTML(params):

    # json file generated key value pairs
    for page in params:

        # templates specified in json file
        head_template = params[page]["head"]
        body_template = params[page]["body"]

        # these variables will hold the output of each filled out template
        head_blob = ''
        body_blob = ''
        # generate meta desc for seo purposes if desc or description key is not specified in json file
        if "desc" in params[page] or "description" in params[page]:
            auto_description = False
        else:
            auto_description = True

        # CLI indicator
        print(f"CREATE {page} FROM [{head_template}, {body_template}] WITH", end=' ')

    # generate body section
        with open(body_template, 'r', encoding="utf-8") as body:

            for line in body:
                first = line.find("{%")
                second = line.find("%}")

                #check for variables in template

                if first != -1 and second != -1:
                    key = line[first + 2: second].replace(" ", '')
                    #print(key)
                    # if var is found, check if var should output a string(=) or generate html
                    if key.startswith("="):
                        line = line.replace(line[first: second + 2], f"{params[page][key[1:]]}")
                    else:
                        contents = params[page][key]
                        print(contents, end=' ')
                        generated_html = mdToWeb(contents)
                        
                        # generate auto description
                        if auto_description:
                            sanitized_desc = generateDesc(generated_html)

                        #print(generated_html)
                        line = line.replace(line[first: second + 2], generated_html)
                
                # final html_body generated
                body_blob += line
            #print(body_blob)



        # generate head template
        with open(head_template, 'r', encoding="utf-8") as head:
            
            head = head.read()

            to_fill_out = re.findall("({%)(.*?)(%})", head)

            # (%)(tag_name)(%)
            for touple in to_fill_out:

                # tag_name
                key = touple[1].strip()
                head = head.replace(touple[0] + touple[1] + touple[2], params[page][key])
            
            #print(head)

            head_lines = head.split("\n")

            # auto generate  meta description if desc or description key not specified in json (for seo)
            if auto_description:
                desc_tag = f"    <meta name=\"description\" content=\"{sanitized_desc}\">"
                head_lines.insert(-1, desc_tag)

            # final head
            head_blob = "\n".join(head_lines)
            #print(head_blob)


        with open(page, 'w', encoding="utf-8") as result:
            result.write(head_blob)
            result.write("\n")
            result.write(body_blob)
        
        if not auto_description:
            print("(MANUAL DESCRIPTION!)", end=" ")
        print("...done!")
        
        lookGoodHTML(page)

# prettifier
def lookGoodHTML(page, spaces = 2):
    no_indent = ["meta", "link"]
    depth = 0
    indent = ' ' * spaces
    data = ''
    with open(page, 'r', encoding="utf-8") as f:
        data = f.read().split("\n")
    with open(page, 'w', encoding="utf-8") as f:
        for item in data:
            if item != '':
                item = item.strip()
                open_tag = re.findall("<[^!\/ ]*?>|<[^!\/]*? ", item)
                close_tag = re.findall("<\/.*?>|\/>", item)
                if len(open_tag) != 0:
                    f.write(f"{indent * depth}{item}\n")
                    #print(depth, open_tag, close_tag)
                    if open_tag[0][1: -1] not in no_indent and len(close_tag) == 0:
                        depth += 1
                elif len(close_tag) != 0:
                    depth -= 1
                    #print(depth, open_tag, close_tag)
                    f.write(f"{indent * depth}{item}\n")
                else:
                    f.write(f"{indent * depth}{item}\n")

# generate meta description
def generateDesc(body_blob):
    inner_html = re.sub("<figcaption>[^<]*<\/figcaption>", "", body_blob)
    inner_html = re.sub("<figcaption>[^<]*<\/figcaption>|<[^>]*>", "",inner_html)
    inner_html = re.sub('\s+',' ',inner_html)
    inner_html = re.sub("\"|\'", "", inner_html)
    inner_html = (inner_html[:449] + '...') if len(inner_html) > 449 else inner_html

    return inner_html.strip()


if __name__ == "__main__":

    params = parsePages("pages.json")
    generateHTML(params)