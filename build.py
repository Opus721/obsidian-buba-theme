"""Builds theme.css from src/theme.src.css, embedding the Inter fonts from fonts/ as data URLs.

Run: python3 build.py
"""
import base64
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
LATIN = 'U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD'
CYRILLIC = 'U+0301,U+0400-045F,U+0490-0491,U+04B0-04B1,U+2116'

faces = []
for subset, unicode_range in (('cyrillic', CYRILLIC), ('latin', LATIN)):
    for style in ('normal', 'italic'):
        with open(os.path.join(ROOT, 'fonts', f'inter-{subset}-opsz-{style}.woff2'), 'rb') as f:
            data = base64.b64encode(f.read()).decode()
        faces.append(
            "@font-face {\n  font-family: 'Buba Inter';\n"
            f"  font-style: {style};\n  font-display: swap;\n  font-weight: 100 900;\n"
            f"  src: url(data:font/woff2;base64,{data}) format('woff2-variations');\n"
            f"  unicode-range: {unicode_range};\n}}"
        )

fonts = (
    '/* Inter 4 by Rasmus Andersson, SIL Open Font License 1.1 (fonts/OFL.txt): Latin and Cyrillic, '
    'weight and optical size axes. */\n' + '\n'.join(faces)
)
with open(os.path.join(ROOT, 'src', 'theme.src.css')) as f:
    source = f.read()
with open(os.path.join(ROOT, 'theme.css'), 'w') as f:
    f.write(source.replace('@@FONTS@@', fonts))
print('theme.css', os.path.getsize(os.path.join(ROOT, 'theme.css')), 'bytes')
