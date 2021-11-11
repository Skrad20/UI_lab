def style_upload() -> str:
    file = open(r'style\style_window.css')
    result = file.read()
    file.close()
    return result
