RPackageRepo
============

Utility for building a R package repository.

This is analogous to write_PACKAGES in R: http://stat.ethz.ch/R-manual/R-devel/library/tools/html/writePACKAGES.html

It's written in Python for future work including automation of package installation from a Jenkins build

This Python utility script builds the PACKAGES file required for creating an internal R package repository

It locates the DESCRIPTION file in the package and writes this to the main PACKAGES file.

You will need to create a directory structure as follows:

```
    ├── bin
    └── src
      └── contrib
      ├── PACKAGES
      └── Package_x.y.tar.gz
      └── Package_x.y.zip
```

This works with both tar.gz and zip files and was tested with Python 2.6.

