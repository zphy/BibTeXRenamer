# BibtexRenamer

Utilities for reference management.

- bibtex_renamer takes an existing .bib library and converts it into a new .bib file with all reference keys in the same format as Google scholar (i.e. last name of first author + year + first nontrivial word of title), and some irrelevant information deleted to reduce file size.
- clean_citations takes an existing bibliography file and auxiliary output file from latex compilation, and deletes all unused citations.

## Usage example

### Usage of bibtex_renamer

Run a command of the form "python bibtex_renamer.py ORIGINAL-BIBTEX.bib" on the command line. It will generate a new file named main.bib as output.

### Usage of clean_citations

Rename the .aux file produced by latex+bibtex as "main.aux", and the input bibtex file as "main.bib". Run the command "python clean_citations.py" on the command line. This will produce a new bibtex file "clean_main.bib".

## Contributing

Feel free to contact the author with any questions or requests.

## Authors

Harry Zhou - (https://lukin.physics.harvard.edu/people/hangyun-harry-zhou)

## License

This project is licensed under the GNU GPL v3 License - see the [LICENSE.md](LICENSE.md) file for details
