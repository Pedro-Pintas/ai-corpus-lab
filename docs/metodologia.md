# Methodology

This project documents experiments in AI-assisted corpus building and text analysis.

The current workflow is based on:

1. collecting TXT and OCR-derived text sources;
2. cleaning and normalizing the text;
3. creating metadata for each document;
4. splitting long texts into sentences and chunks;
5. preparing the corpus for semantic search;
6. testing retrieval-augmented generation over historical Portuguese texts.

## Current limitations

The project is experimental.

The code is being developed iteratively and is not yet a polished software package.  
The main goal is to document a practical workflow for working with historical corpora using Python and AI systems.

## Design principles

- keep the corpus inspectable;
- preserve metadata;
- separate raw text from processed outputs;
- make each processing step reproducible;
- avoid presenting generated answers without showing retrieval context.
