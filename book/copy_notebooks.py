"""
Ta koda kopira vse notebooke spletne knjige v spletno stran in pripravi stran,
ki jih poveže
"""
import os
import nbformat
import shutil

EXCLUDE_NOTEBOOKS = ['NM2016.ipynb',
                     'PiNM2016-17.ipynb',
                     'Predavanje 10b - Taylorjeve vrste.ipynb',
                     'working.ipynb']
PAGEFILE = """title: {title}
url:
save_as: {htmlfile}
Template: {template}

{{% notebook notebooks/{notebook_file} cells[{cells}] %}}
"""

INTRO_TEXT = """Ta domača stran je pripravljena na podlagi spletnega učbenika 
[Programiranje in numerične metode v ekosistemu Pythona](https://github.com/jankoslavic/pypinm), 
ki ga je pripravil Janko Slavič v obliki Jupyter notebookov.
"""


def abspath_from_here(*args):
    here = os.path.dirname(__file__)
    path = os.path.join(here, *args)
    return os.path.abspath(path)

NB_SOURCE_DIR = abspath_from_here('..')
NB_DEST_DIR = abspath_from_here('content', 'notebooks')
PAGE_DEST_DIR = abspath_from_here('content', 'pages')


def copy_notebooks():
    nblist = sorted(nb for nb in os.listdir(NB_SOURCE_DIR)
                    if nb.endswith('.ipynb') and nb not in EXCLUDE_NOTEBOOKS)
    name_map = {nb: nb.rsplit('.', 1)[0].lower() + '.html'
                for nb in nblist}

    figsource = abspath_from_here('..', 'fig')
    figdest = abspath_from_here('content', 'fig')

    if os.path.exists(figdest):
        shutil.rmtree(figdest)
    shutil.copytree(figsource, figdest)

    figurelist = os.listdir(abspath_from_here('content', 'fig'))
    figure_map = {os.path.join('fig', fig) : os.path.join('/pypinm/fig', fig)
                  for fig in figurelist}

    for nb in nblist:
        base, ext = os.path.splitext(nb)
        print('-', nb)

        content = nbformat.read(os.path.join(NB_SOURCE_DIR, nb),
                                as_version=4)

        if nb == 'NM2016.ipynb':
            cells = '1:'
            template = 'page'
            title = 'Numerične metode 2016/17'
            content.cells[2].source = INTRO_TEXT
        else:
            cells = '2:'
            template = 'booksection'
            title = content.cells[0].source.split('<b>')[1].split('</b>')[0]
            if title == '':
            #if not title.startswith('<font size="7" color="f00e0e" face="garamond"><b>') or len(title.splitlines()) > 1:
                raise ValueError('title not found in first cell')
            title = title.lstrip('#').strip()

            # put nav below title
            content.cells[0], content.cells[1], content.cells[2] = content.cells[2], content.cells[0], content.cells[1]

        # Replace internal URLs and figure links in notebook
        for cell in content.cells:
            if cell.cell_type == 'markdown':
                for nbname, htmlname in name_map.items():
                    if nbname in cell.source:
                        cell.source = cell.source.replace(nbname, htmlname)
                for figname, newfigname in figure_map.items():
                    if figname in cell.source:
                        cell.source = cell.source.replace(figname, newfigname)

        nb_no_spaces = nb.replace(' ', '_')
        nbformat.write(content, os.path.join(NB_DEST_DIR, nb_no_spaces))

        pagefile = os.path.join(PAGE_DEST_DIR, base + '.md')
        htmlfile = base.lower() + '.html'
        with open(pagefile, 'w', encoding='utf-8') as f:
            f.write(PAGEFILE.format(title=title,
                                    htmlfile=htmlfile,
                                    notebook_file=nb_no_spaces,
                                    template=template,
                                    cells=cells))

if __name__ == '__main__':
    copy_notebooks()