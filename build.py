#!/usr/bin/env python3

from argparse import ArgumentParser
from pathlib import Path
from shutil import copy2

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>A Bit of Web Development</title>
    <link rel="stylesheet" href="style.css"/>
</head>
<body>
    <NAVIGATION/>
    <CONTENT/>
</body>
</html>
"""


PAGES = (
    'index.html',
    'html5intro.html',
    'pageStructure.html',
    'figures.html',
    'forms1.html',
    'forms2.html',
    'canvas.html',
    'omittedHtml5Features.html',
    'css.html',
    'sassPerhaps.html',
    'cssVariables.html',
)

DIAGRAMS = (
    ('TheBig3.dot', 'circo'),
)


class BuildError(RuntimeError):
    pass


def build_link(href, text):
    return f'<a href="{href}">{text}</a>'


def nav_links(index, pages):
    links = []
    if index > 0:
        links.append(
            build_link(pages[index - 1], 'Previous')
        )
    if index + 1 < len(pages):
        links.append(
            build_link(pages[index + 1], 'Next')
        )
    return "\n".join(links)


def main(args):
    src_dir = Path(args.input_dir)
    if not src_dir.exists():
        raise BuildError(f"{src_dir} doesn't exist")

    if not src_dir.is_dir():
        raise BuildError(f"{src_dir} isn't a directory")

    dest_dir = Path(args.output_dir)
    if dest_dir.exists():
        if not dest_dir.is_dir():
            raise BuildError(f"{dest_dir} isn't a directory")
    else:
        dest_dir.mkdir()

    for src_file in src_dir.iterdir():
        suffix = src_file.suffix
        if suffix in ('.html', '.dot'):
            continue
        if suffix in ('.svg', '.css'):
            copy2(src_file, dest_dir)
            continue

        print(src_file)
        print(suffix)

    for i, page in enumerate(PAGES):
        src_file = src_dir / page
        if not src_file.exists():
            raise BuildError(f"{src_file} not found")

        nav_html = nav_links(i, PAGES)

        template = TEMPLATE
        with src_file.open('r') as in_file:
            template = template.replace('<CONTENT/>', in_file.read())
        template = template.replace('<NAVIGATION/>', nav_html)

        dest_file = dest_dir / page
        with dest_file.open('w') as out_file:
            out_file.write(template)



    for diagram in DIAGRAMS:
        pass






if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument('input_dir', metavar='INPUT_DIR')
    arg_parser.add_argument('output_dir', metavar='OUTPUT_DIR')
    main(arg_parser.parse_args())
