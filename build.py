#!/usr/bin/env python3

from argparse import ArgumentParser
from pathlib import Path
from shutil import copy2
from subprocess import run
from sys import stderr

from jinja2 import (
    Environment,
    FileSystemLoader,
    select_autoescape,
)


PAGES_AND_TITLES = (
    ('index.html', ''),
    ('html5intro.html', ''),
    ('pageStructure.html', 'Structural Tags'),
    ('figures.html', '<code>&lt;figure&gt;</code>'),
    ('newInputTypes.html', 'New <code>&lt;input&gt;</code> Types'),
    ('inputWithDatalist.html', '<code>&lt;input/&gt;</code> with datalist'),
    (
        'patternValidation.html',
        '<code>&lt;input/&gt;</code> validation with <code>pattern</code>',
    ),
    ('dialog.html', '<code>&lt;dialog/&gt;</code>'),
    ('dialogJavaScript.html', '<code>&lt;dialog/&gt;<code> JavaScript'),
    ('canvas.html', '<code>&lt;canvas/&gt;</code>'),
    ('omittedHtml5Features.html', "But wait, there's more"),
    ('css.html', "CSS"),
    ('cssKeepItRelative.html', "CSS Units"),
    ('cssVariables.html', "CSS Variables"),
    ('gridLayout.html', 'Grid Layout'),
    ('flexboxLayout.html', 'Flexbox Layout'),
    ('flexboxLayout2.html', 'Flexbox Layout 2'),
    ('sassPerhaps.html', "SASS Perhaps?"),
    ('SASS-Indented.html', 'SASS Indented'),
    ('SASS-SCSS.html', 'SASS SCSS'),
    ('bulma.html', 'BULMA'),
    ('bootstrap.html', 'Bootstrap'),
    ('javascript.html', 'JavaScript'),
    ('javascriptClass.html', 'JavaScript classes'),
    ('javascriptClasses2.html', 'Other class features'),
    ('nodejs.html', 'Node.js'),
    ('nvm.html', 'Node Version Manager (NVM)'),
    ('npm.html', 'Node Package Manager (NPM)'),
    ('typescript.html', 'TypeScript'),
    ('javascriptFrameworks.html', 'JavaScript Frameworks'),
    ('htmx.html', 'HTMX'),
    ('python.html', 'Python Web Development'),
    ('references.html', 'References'),
)

DIAGRAMS = (
    ('TheBig3.dot', 'circo'),
)

LAYOUT_ENGINES = {'dot', 'circo'}


class BuildError(RuntimeError):
    pass


def nav_links(index, pages):
    context = {
        'prev_url': '',
        'next_url': ''
    }
    if index > 0:
        context['prev_url'] = pages[index - 1][0]

    if index + 1 < len(pages):
        context['next_url'] = pages[index + 1][0]

    return context


def copy_non_source_files(src_dir: Path, dest_dir: Path) -> None:
    for src_file in src_dir.iterdir():
        suffix = src_file.suffix
        if suffix in ('.html', '.dot'):
            continue
        if suffix in ('.svg', '.css'):
            copy2(src_file, dest_dir)
            continue


def render_html(src_dir: Path, dest_dir: Path) -> None:

    env = Environment(
        loader=FileSystemLoader(src_dir),
        autoescape=select_autoescape(['html', 'xml'])
    )

    for i, page_and_title in enumerate(PAGES_AND_TITLES):
        page, title = page_and_title
        src_file = src_dir / page
        if not src_file.exists():
            raise BuildError(f"{src_file} not found")

        context = {'title': title}
        context.update(nav_links(i, PAGES_AND_TITLES))

        template = env.get_template(page)
        dest_file = dest_dir / page
        with dest_file.open('w') as out_file:
            out_file.write(
                template.render(**context)
            )


def render_diagrams(src_dir: Path, dest_dir: Path) -> None:
    for diagram_tuple in DIAGRAMS:
        tuple_length = len(diagram_tuple)
        if tuple_length == 0:
            continue
        src_file = src_dir / diagram_tuple[0]
        layout_engine = 'dot' if tuple_length < 2 else diagram_tuple[1]
        if layout_engine not in LAYOUT_ENGINES:
            print(
                f"Unsupported layout engine {layout_engine}",
                file=stderr,
            )
            continue
        dest_file = dest_dir / f"{src_file.stem}.svg"
        with dest_file.open('w') as out_file:
            run(
                [layout_engine, '-Tsvg', src_file],
                stdout=out_file,
            )


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

    copy_non_source_files(src_dir, dest_dir)
    render_html(src_dir, dest_dir)
    render_diagrams(src_dir, dest_dir)


if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument('input_dir', metavar='INPUT_DIR')
    arg_parser.add_argument('output_dir', metavar='OUTPUT_DIR')
    main(arg_parser.parse_args())
