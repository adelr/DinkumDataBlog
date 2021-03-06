'''
Taken from http://vincent-lunot.com/post/toward-publishing-jupyter-notebooks-with-hugo/

Adel: Modified to read the configuration from a yaml file
'''


from nbconvert import MarkdownExporter
from nbconvert.preprocessors import Preprocessor
from pathlib import Path
from traitlets.config import Config

import sys

import yaml

import nbformat
import re

# here I customize some functions of the fabfile.py of the hugo_jupyter package

class CustomPreprocessor(Preprocessor):
    """Remove blank code cells and unnecessary whitespace."""

    def preprocess(self, nb, resources):
        """
        Remove blank cells
        """
        for index, cell in enumerate(nb.cells):
            if cell.cell_type == 'code' and not cell.source:
                nb.cells.pop(index)
            else:
                nb.cells[index], resources = self.preprocess_cell(cell, resources, index)
        return nb, resources

    def preprocess_cell(self, cell, resources, cell_index):
        """
        Remove extraneous whitespace from code cells' source code
        """
        if cell.cell_type == 'code':
            cell.source = cell.source.strip()

        return cell, resources


def doctor(string: str) -> str:
    """Get rid of all the wacky newlines nbconvert adds to markdown output and return result."""
    post_code_newlines_patt = re.compile(r'(```)(\n+)')
    inter_output_newlines_patt = re.compile(r'(\s{4}\S+)(\n+)(\s{4})')

    post_code_filtered = re.sub(post_code_newlines_patt, r'\1\n\n', string)
    inter_output_filtered = re.sub(inter_output_newlines_patt, r'\1\n\3', post_code_filtered)

    return inter_output_filtered

def make_yaml_header(**kwargs):

    header = '---\n'

    for key, value in kwargs.items():
        if type(value) in [str, int , float ] :
            header += '{} : {}\n'.format(key, value)
        else:
            header += '{}: \n'.format(key)
            for item in value:
                header += '  - {}\n'.format(item)

    header += '---\n'

    return header


def notebook_to_markdown( path, date, slug, **kwargs ):
    """
    Convert notebook to Markdown format

    Args:
        path: str, path to notebook
        date: datestring in YYYY-MM-DD format
        slug: str, front-matter parameter, used to compose adress of blogpost
        kwargs: str, float, int, list, tuple, other front-matter parameters recommended to pass title

    """
    path_nb = Path(path)
    path_out = path_nb.parents[1] / 'static'/ date.split('-')[0] / date.split('-')[1] / slug
    path_post = path_nb.parents[1] / 'content/post/' / ( date + '-' + slug + '.md' )


    assert path_nb.exists()
    assert path_post.parent.exists()
    assert bool( re.match('[0-9]{4}-[0-1][0-9]-[0-3][0-9]', date) ), 'Incorrect date format, need YYYY-MM-DD'

    # convert notebook to .md----------------------------------------------------

    with Path(path).open() as fp:
        notebook = nbformat.read(fp, as_version=4)

    c = Config()
    c.MarkdownExporter.preprocessors = [CustomPreprocessor]
    markdown_exporter = MarkdownExporter(config=c)

    markdown, resources = markdown_exporter.from_notebook_node(notebook)
    md = doctor(markdown)

    yaml = make_yaml_header(  date = date
                             , slug = slug
                             , mathjax= 'ture'
                             , **kwargs)

    md = yaml + md

    with path_post.open('w') as f:
        f.write(md)
    # write outputs as png --------------------------------------------------------

    if 'outputs' in resources.keys():
        if not path_out.exists():
            path_out.mkdir(parents=True)
        for key in resources['outputs'].keys():
            with (path_out / key).open('wb') as f:
                f.write( resources['outputs'][key] )



if __name__ == "__main__":

    nb_path = sys.argv[1]

    src_dir = Path(f'./notebooks')

    path = src_dir/f"{nb_path}.ipynb"
    yaml_path = src_dir/f"{nb_path}.yml"

    try:
        with open(yaml_path, 'r') as ymlfile:
            cfg = yaml.load(ymlfile)
    except Exception as e:
        print(f"Cannot load {yaml_path}", e)

    notebook_to_markdown(path = path,
                         date = cfg['date'],
                         slug = cfg['slug'],
                         title = cfg['title'],
                         author = 'Adel',
                         categories = ['Python','blogging'],
                         tags = cfg['tags'],
                         summary = cfg['summary'],
                         thumbnailImagePosition = 'left',
                         thumbnailImage = './static/img/avatar-icon.png'
                         )
