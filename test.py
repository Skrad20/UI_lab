from docxtpl import DocxTemplate, RichText
import logging
logging.basicConfig(
    filename="logs/log_data.log",
    level=logging.NOTSET
)
logger = logging.getLogger(__name__)

doc = DocxTemplate(r'test.docx')
rt = RichText(
    'some violet',
    color='#ff0000',
    bold=True
)
context = {
    'test_1': rt,
    'test_2': 3,
    'test': 5,
}
logger.debug('dsfgdssd')
doc.render(context)
doc.save('Generated_doc 1.docx')
