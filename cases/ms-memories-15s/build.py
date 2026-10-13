import pathlib
d=pathlib.Path(__file__).parent
(d/'comp.html').write_text((d/'comp.src.html').read_text().replace('__FONT__',(d/'font.b64').read_text().strip()))
print('comp.html built')
