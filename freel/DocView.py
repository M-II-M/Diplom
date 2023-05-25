import os

import docx
from bs4 import BeautifulSoup
import codecs
import aspose.words as aw
from htmldocx import HtmlToDocx


class DocView:
    def __init__(self, document):
        self.document = document
        self.convert_doc = ''  # название файла для отображения на сайте
        self.interim_code = ''  # код промежуточного шаблона
        self.html = self.word2html()  # для поиска чекпоинтов

    def word2html(self):
        doc = aw.Document(self.document)

        # Включить двустороннюю информацию
        saveOptions = aw.saving.HtmlSaveOptions()
        saveOptions.export_roundtrip_information = True

        # Сохранение в HTML
        # TODO генерировать имя из названия документа
        htmldoc_name = "Document.html"
        self.convert_doc = htmldoc_name
        doc.save(htmldoc_name, saveOptions)

        f = codecs.open(htmldoc_name, 'r', 'utf-8')
        html = f.read()

        # убираем ватермарки
        html = html.replace(
            '<span style="font-weight:bold; color:#ff0000">Evaluation Only. Created with Aspose.Words. Copyright '
            '2003-2023 Aspose Pty Ltd.</span>', "")

        html = html.replace(
            '<span style="font-weight:bold; color:#ff0000">Created with an evaluation copy of Aspose.Words. To '
            'discover the full versions of our APIs please visit: https://products.aspose.com/words/</span>',
            '')

        html = html.replace('<div><div style="-aw-different-first-page:true; -aw-headerfooter-type:header-primary; '
                            'clear:both"><p style="margin-top:0pt; margin-bottom:0pt"><span style="height:0pt; display:block; '
                            'position:absolute; z-index:-65537"><img src="Document.001.png" width="643" height="350" alt="" '
                            'style="margin-top:243.35pt; -aw-left-pos:0pt; -aw-rel-hpos:margin; -aw-rel-vpos:margin; '
                            '-aw-top-pos:0pt; -aw-wrap-type:none; position:absolute" /></span><span '
                            'style="-aw-import:ignore">&#xa0;</span></p></div>', '')

        return html

    def get_checkpoints(self):
        soap = BeautifulSoup(self.html, 'lxml')
        tags = soap.find_all('span')

        checkpoints = {}  # словарь чекпоинтов вида чекпоинт_номер: фраза
        num_of_point = 0
        for i in tags:
            try:
                if 'background-color:#00ff00' in i['style']:  # #00ff00 - зеленый фон выделения
                    checkpoints["checkpoint_" + str(num_of_point)] = i.text
                    i.string = "{{checkpoint_" + str(num_of_point) + "}}"  # переписываем чекпоинты в рабочем шаблоне

                    num_of_point += 1
            except KeyError:
                continue

        self.interim_code = soap
        return checkpoints

    def save_interim_template(self):
        # TODO придумать генерацию имени
        interim_template_name = 'interim_template'
        interim_template_code = self.interim_code

        # сохраняем рабочий шаблон в html
        with open(interim_template_name + ".html", "w", encoding="utf-8") as file:
            file.write(str(interim_template_code))

        # сохраняем рабочий шаблон в docx

        # interim_template_doc = HtmlToDocx()
        # interim_template_doc.parse_html_file(interim_template_name + ".html", interim_template_name + ".docx")

        interim_template_doc = aw.Document(interim_template_name + ".html")
        interim_template_doc.save(interim_template_name + ".docx")

        doc = docx.Document(interim_template_name + ".docx")
        para = doc.paragraphs

        # TODO удалить вотермарки
        section = para.sections

        for i in section:
            print(i)

        for i in para:
            print(i.text)

        return interim_template_name


