import pathlib, base64
d=pathlib.Path(__file__).parent
enc=lambda n: base64.b64encode((d/n).read_bytes()).decode()
src=(d/'comp.src.html').read_text().replace('__FONT__',(d/'font.b64').read_text().strip())
src=src.replace('__INK__',enc('logo_ink2.png')).replace('__TMAP__',enc('logo_t2.png'))
(d/'comp.html').write_text(src)
print('comp.html built', len(src)//1024, 'KB')
