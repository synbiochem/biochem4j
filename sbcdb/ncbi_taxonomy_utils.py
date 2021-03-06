'''
SYNBIOCHEM-DB (c) University of Manchester 2015

SYNBIOCHEM-DB is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author:  neilswainston
'''
import os
import sys
import tarfile
import tempfile
import urllib


__NCBITAXONOMY_URL = 'ftp://ftp.ncbi.nih.gov/pub/taxonomy/taxdump.tar.gz'


def load(writer, array_delimiter, source=__NCBITAXONOMY_URL):
    '''Loads NCBI Taxonomy data.'''
    nodes_filename, names_filename = _get_ncbi_taxonomy_files(source)
    nodes, rels = _parse_nodes(nodes_filename, array_delimiter)
    _parse_names(nodes, names_filename, array_delimiter)

    writer.write_nodes(nodes.values(), 'Organism')
    writer.write_rels(rels, 'Organism', 'Organism')


def _get_ncbi_taxonomy_files(source):
    '''Downloads and extracts NCBI Taxonomy files.'''
    temp_dir = tempfile.gettempdir()
    temp_gzipfile = tempfile.NamedTemporaryFile()
    urllib.urlretrieve(source, temp_gzipfile.name)

    temp_tarfile = tarfile.open(temp_gzipfile.name, 'r:gz')
    temp_tarfile.extractall(temp_dir)

    temp_gzipfile.close()
    temp_tarfile.close()

    return os.path.join(temp_dir, 'nodes.dmp'), \
        os.path.join(temp_dir, 'names.dmp')


def _parse_nodes(filename, array_delimiter):
    '''Parses nodes file.'''
    nodes = {}
    rels = []

    with open(filename, 'r') as textfile:
        for line in textfile:
            tokens = [x.strip() for x in line.split('|')]
            tax_id = tokens[0]

            if tax_id != '1':
                rels.append([tax_id, 'is_a', tokens[1]])

            nodes[tax_id] = {'taxonomy:ID(Organism)': tax_id,
                             ':LABEL':
                             'Organism' + array_delimiter + tokens[2]}

    return nodes, rels


def _parse_names(nodes, filename, array_delimiter):
    '''Parses names file.'''

    with open(filename, 'r') as textfile:
        for line in textfile:
            tokens = [x.strip() for x in line.split('|')]
            node = nodes[tokens[0]]

            if 'name' not in node:
                node['name'] = tokens[1]
                node['names:string[]'] = set([node['name']])
            else:
                node['names:string[]'].add(tokens[1])

    for _, node in nodes.iteritems():
        if 'names:string[]' in node:
            node['names:string[]'] = \
                array_delimiter.join(node['names:string[]'])


def main(argv):
    '''main method'''
    load(*argv)


if __name__ == "__main__":
    main(sys.argv[1:])
