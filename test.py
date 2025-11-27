from docxtpl import DocxTemplate
import jinja2, docxtpl
print("Jinja2 version:", jinja2.__version__)
print(docxtpl.__version__) 
print("Jinja2 path:", jinja2.__file__)

doc = DocxTemplate("test.docx")  # простой шаблон с {{ hello }}
context = {"hello": "world"}
doc.render(context)
doc.save("output.docx")
print("OK")