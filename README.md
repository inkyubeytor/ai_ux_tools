# Integrating a new dataset

Dataset integrations are placed in the `dataset` directory. Each one subclasses 
class `Dataset` from `dataset/dataset.py`, implementing the `retrieve_document`
method, which returns a list of all `Element` strings in a single document of 
the dataset, given the document name, and the `list_documents` method, which 
lists all available documents in a dataset. Dataset integrations are imported
into the `datasets` dictionary in `dataset/datasets.py` to allow access to 
other components of the pipeline.

# Summarization

The summarizers are placed in the `summarizer` directory. Each one subclasses 
class `Summarizer` from `summarizer/summarizer.py`, implementing the 
`summarize_element` method. Summarizers are imported into the `summarizers`
dictionary in `summarizer/summarizers.py` to allow access to other components of
the pipeline.

To summarize a dataset, use the top level `run_summary.py` script. The syntax is
as follows:
```
python run_summarizer.py [dataset_type] [dataset_dir] [summarizer_type] [output_dir]
```
Example (Windows):
```
python run_summarizer.py test_drive C:\Users\your_username\Documents\nlp-datasets\test-drive presumm C:\Users\your_username\Documents\output
```

<!---TODO: add example input and ouptut--->
Example input document:
```

```
Example output summary:
```

```

# Comparison

The comparison tools are placed in the `comparator` directory. Each one 
subclasses class `Comparator` from `comparator/comparator.py`, implementing the 
`compute_difference` method to compute pairwise differences between elements. 
Comparators are imported into the `comparators` dictionary in 
`comparator/comparators.py` to allow access to other components of the pipeline.

To compare elements at a certain index of each document in a dataset for either 
similarity or difference and return the top results, use the top level 
`run_comparison.py` script. The syntax is as follows:

```
python run_comparison.py [dataset_type] [dataset_dir] [comparison_type] [output_dir] [element_index] [num_pairs] [similar]
```
Example (Windows):
```
python run_comparison.py test_drive C:\Users\your_username\Documents\nlp-datasets\test-drive fasttext C:\Users\your_username\Documents\output 0 10 True
```

<!---TODO: add example input and ouptut--->
Example input document:
```

```
Example output summary:
```

```