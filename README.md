chucky-tools
============

Chucky-tools is a modular implementation of chucky (see the <a href=http://filepool.informatik.uni-goettingen.de/publication/sec//2013-ccs.pdf>paper</a>).

Dependences
-----------

Before you start make sure the following tools are working properly on your machine:

- <a href=http://www.mlsec.org/joern>Joern</a>
- <a href=http://www.mlsec.org/sally>Sally</a>

Installation
------------

To install chucky-tools run

```
python setup.py install [--user]
```

Walkthrough
===========

The following steps explain how chucky-tools and basic command line utilities can be used together to obtain functionality similar to the original implementation of chucky. This walkthrough discribes the following steps:

- Creation of global API embedding
- Identification of sinks and sources
- Neighborhood discovery
- Lightweight tainting
- Embedding of functions
- Anomaly detection

Creation of global API embedding
--------------------------------

Take a look at the ```joern-apiembedder``` tool from https://github.com/fabsx00/joern-tools. 

Identification of sinks and sources
-----------------------------------

Take a look at https://github.com/fabsx00/joern-tools, especially the ```joern-lookup``` tool.

First, we create an input file of tab separated fields, each represening the node ID of a sink/source. The first field has to contain the ID of the sink/source under inspection (the target sink/source). The remaining fields contain IDs of reference sinks/sources, i.e sinks/sources to which the target is compared later (the limit array). For example the limit array may contain ```Parameter``` IDs of the same type and name as the target parameter. However there are no further restrictions except for the type of the sink/soure which must be the same type as the target node. Of course, the file can have multiple lines.

In short, the input file has the following format:

| target sink/source ID | list of reference sink/source IDs (limit array) |
| --------------------- | ----------------------------------------------- |

In the following section this file is refered to as ```$INPUT_FILE```.

Neighborhood discovery
----------------------

This step is about selecting sinks/sources from the limit array that belong to similar functions as the target sink/source, i.e. the neighborhood. The neighborhood is determined by the tool ```chucky-knn``` which outputs the target sink/source along with its *n* nearest neighbors. In other words, the limit array is reduced to sinks/sources in the neighborhood of the target sink/source. The ```chucky-knn``` tool is applied as follows:

```
chucky-knn $API_EMBEDDING --n-neighbors $N --file $INPUT_FILE --out $NEIGHBORHOOD_FILE
```

The tool reads the input file ```$INPUT_FILE``` and produces the output file ```$NEIGHBORHOOD_FILE```, which contains the target sink/source and its ```$N``` nearest neighbors in the following format

| target sink/source ID | neighborhood (reduced limit array) |
| --------------------- | ---------------------------------- |

Lightweight tainting
--------------------

Since all sink/source IDs are known by now, we can proceed by extract all statements that are connected to them via data dependences. Note that this is not exactly the same procedure as in the original chucky paper. This is the task of the tool ```chucky-taint```. However, the input for the taint tool requires a different format and additional information than the previous produced output. The input format of ```chucky-taint``` looks as follows:

| statement ID | identifier name |
| ------------ | --------------- |

i.e. a column containing the statement ID for each sink/source and a second column containing the identifier or name of the sink/source are required. To this end, all sink/source IDs
of the previous step are written in one column and duplicates are removed:

```
cat $NEIGHBORHOOD_FILE | tr '\t' '\n' | sort | uniq
```

Then the two new columns are appended by piping the sink/source IDs into the following command:

```
chucky-traverse --echo "statements" | chucky-traverse --echo $TRAVERSAL | chucky-demux --keys 0 1 | chucky-translate code --column=2
```

where ```$TRAVERSAL``` depends on the chosen node types for the sinks/sources, e.g. ```"statements.defines"``` for nodes of the types ```Parameter``` or ```Callee```. Since ```$TRAVERSAL``` may yield more than one node we need to *demux* each outcome in a separat line before translating the node ID with the corresponding *code* property.

Finally we point the taint tool to the columns containing the statement IDs and the identifier name. Altogether this step can be accomplished by the following pipeline:

```
cat $NEIGHBORHOOD_FILE | tr '\t' '\n' | sort | uniq | chucky-traverse --echo "statements" | chucky-traverse --echo $TRAVERSAL | chucky-demux --keys 0 1 | chucky-translate code --column=2 | chucky-taint --echo --mode=$MODE --statement=1 --identifier=2 --out $TAINT_FILE
```

where ```$MODE``` is either ```backward``` or ```forward``` for sinks or sources respectively. 
The format of the output (```$TAINT_FILE```) is as follows:

| sink/source ID | statement ID | identifier name | list of all dependent statement IDs |
| -------------- | ------------ | --------------- | ----------------------------------- |

Embedding of functions
----------------------

The last step produced a large file containing all dependent statements for each sink/source. In this step, we first discard all statements that do not contain a condition. Afterwards, the conditions are normalized and embedded.

We filter the conditions by demuxing each statement to its own line. Then, we perform a simple *match* traversal that expands the statements to their abstract syntax tree nodes and searches for nodes of type ```Condition```.

The normalization is done by the tool ```chucky-normalize``` which returns a list of features for each condition. It needs a column containing a ```Condition``` ID and a column with a identifier name whose occurences in the condition are replaced by a symbolic name (```$SYM```) in the normalization process. Afterwards, we cut off unneeded columns.

The whole pipeline of this step looks as follows:

```
cat $TAINT_FILE | chucky-demux --keys 0 1 2 | chucky-traverse --echo --column=3 "match{it.type == 'Condition'}" | cut -f 1,3,5 | chucky-normalize --echo --condition=2 --symbol=1 | cut -f 2,3 --complement > $CONDITIONS_FILE
```

and creates the output file ```$CONDITIONS_FILE``` with the following format:

| sink/source ID | list of normalized features |
| -------------- | --------------------------- |

To embed the normalized conditions we use the tools ```chucky-store``` to make a directory containing the features and ```sally``` to create a binary embedding from it:

```
chucky-store $FUNCTIONS_EMBEDDING --file $CONDITIONS_FILE
sally --config $SALLY_CONFIG_FILE --vect_embed bin --hash_file FUNCTIONS_EMBEDDING/feats.gz FUNCTIONS_EMBEDDING/data/ FUNCTIONS_EMBEDDING/embedding.libsvm
```

where ```$SALLY_CONFIG_FILE``` has the following content:

```
input = {
       input_format     = "dir";
};

features = {
       ngram_len        = 1;
       ngram_delim      = "%0a";
};

output = {
       output_format    = "libsvm";
};
```

Anomaly detection
-----------------

This step is simple. Just use the tool ```chucky-score``` as follows:

```
chucky-score $FUNCTION_EMBEDDING --file $NEIGHBORHOOD_FILE 
```

Tips
-----

If you plan to run chucky with different neighborhood sizes it is often faster to perform the neighborhood discovery in the end of the process and create an function embedding for each sink/source in ```$INPUT_FILE```.
