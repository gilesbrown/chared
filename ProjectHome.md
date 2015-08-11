Chared is a tool for detecting the character encoding of a text in a known language. The language of the text has to be specified as an input parameter so that correspondent language model can be used. The package contains [models for a  wide range of languages](http://code.google.com/p/chared/source/browse/#svn%2Ftrunk%2Fchared%2Fmodels). In general, it should be more accurate than character encoding detection algorithms with no language constraints.

## What's new ##
[Changelog](http://code.google.com/p/chared/source/browse/trunk/CHANGES)

## Installation ##
  1. Make sure you have [Python](http://www.python.org/) 2.6 or later and [lxml](http://lxml.de/) library version 2.2.4 or later installed.
  1. Download the sources:
```
wget http://chared.googlecode.com/files/chared-1.2.tar.gz
```
  1. Extract the downloaded file:
```
tar xzvf chared-1.2.tar.gz
```
  1. Install the package (you may need sudo or a root shell for the latter command):
```
cd chared-1.2/
python setup.py install
```

## Quick start ##
Detect the character encoding for a file or URL:
```
chared -m czech http://nlp.fi.muni.cz/cs/nlplab
```
Create a custom character encoding detection model from a collection of HTML pages (e.g. for Swahili):
```
chared-learn -o swahili.edm swahili_pages/*.html
```
... or if you have a sample text in Swahili (plain text, UTF-8) and want to apply language filtering on the input HTML files (recommended):
```
chared-learn -o swahili.edm -S swahili_sample.txt swahili_pages/*.html
```
For usage information see:
```
chared --help
chared-learn --help
```

## Python API ##
```
>>> import urllib2
>>> import chared.detector
>>> page = urllib2.urlopen('http://nlp.fi.muni.cz/cs/nlplab').read()
>>> cz_model_path = chared.detector.get_model_path('czech')
>>> cz_model = chared.detector.EncodingDetector.load(cz_model_path)
>>> cz_model.classify(page)
['utf_8']
```

## Acknowledgements ##
This software is developed at the [Natural Language Processing Centre](http://nlp.fi.muni.cz/en/nlpc) of [Masaryk University in Brno](http://nlp.fi.muni.cz/en) with a financial support from [PRESEMT](http://presemt.eu/) and [Lexical Computing Ltd](http://lexicalcomputing.com/), a [corpus tool](http://www.sketchengine.co.uk/) company.

## See also ##
[Unicode over 60 percent of the web](http://googleblog.blogspot.com/2012/02/unicode-over-60-percent-of-web.html) at Google blog