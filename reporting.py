import pdfkit
import os
import shutil


class HTMLDocument:
    # Required:
    # https://github.com/wkhtmltopdf/wkhtmltopdf/releases/tag/0.12.6
    def __init__(self, title, resource_queue, name_dict):
        self.title = title
        self.name_dict = name_dict
        self.doctext = """
        <html>
        <head></head>
        <body>\n
        <center><h1>
        """ + title + '</h1></center><br>'
        for resource in resource_queue:
            self.add_resource(resource)
        self.close_report()
        self.save_report()

    def save_report(self):
        f = open(self.title + '.html', 'wt')
        f.write(self.doctext)
        f.close()
        pdfkit.from_file(self.title + '.html', self.title + '.pdf', options={'enable-local-file-access': ''})
        os.remove(self.title + '.html')
        shutil.rmtree('output')

    def add_image(self, image_name):
        self.doctext += '<center><img src=output/' + image_name + '></center>\n'

    def add_text(self, file_name):
        f = open('output/' + file_name, 'r')
        text = f.readlines()
        for line in text:
            self.doctext += line + '<br>'

    def add_resource(self, resource_name):
        self.doctext += '<h2>' + self.name_dict[resource_name] + '</h2>'
        if '.png' in resource_name or '.jpg' in resource_name:
            self.add_image(resource_name)
        else:
            self.add_text(resource_name)

    def close_report(self):
        self.doctext += '</body>\n</head>'
