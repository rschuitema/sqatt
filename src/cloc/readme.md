# Cloc analysis
With the cloc analysis script you can measure:

* The lines of code per language
* The lines of code per code type
* The code volume
* The lines of code per file

## Usage

``` text
usage: cloc_analysis.py [-h] [--version] [--output OUTPUT] [--config CONFIG]
                        [--all] [--code-size] [--code-type] [--code-volume]
                        [--file-size] [--language]
                        input

positional arguments:
  input            The directory to analyze.

options:
  -h, --help       show this help message and exit
  --version        show program's version number and exit
  --output OUTPUT  The directory where to place the report.
  --config CONFIG  The configuration file to use.
  --all            Analyze all aspects.
  --code-type      Analyze the lined of code per type (production, test, third
                   party, etc).
  --code-volume    Analyze the code volume.
  --file-size      Analyze the lines of code per file.
  --language       Analyze the lines of code per language.
```


### Reports

The reports are generated in a directory specified with the "--output" option.
The default is a "reports" subdirectory in the current directory.

The reports directory can contain a "metrics" and a "profiles" subdirectory.
The metrics directory contains intermediate data that was needed to create the profiles. 
The profiles directory contains the final result.

### Filters

In a configuration file you can specify filters for the code types that you want to analyze. 
These filters are in the format of the cloc program options.
With these filters you can specify e.g. which code is considered production code or test code.

### Configuration file

It is possible to provide a configuration file in the form of an ini file. 
In this configuration file you can specify the filters, the code type and the input and report directory.

When specifying the code types you need to put the "=" at the end of the line.
This is needed by the library used to read the configuration.
