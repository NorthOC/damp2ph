import generator

params = generator.parsePages("pages.json")
generator.generateHTML(params)