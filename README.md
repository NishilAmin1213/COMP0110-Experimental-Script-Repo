## README - COMP0110-Experimental-Script-Repo
A Benchmark Suite for Evaluating LLMs on Real-World Source Code Migration (Java 8 to Java 11)

MSc Software Systems Engineering Research Project (24/25)

### Python Version
This project was developed in Python 3.10.0 on Windows 11 and has not been tested in other environments

### Environment Variables
When running 'prompting_pipeline.py' the Mistral API Key is required under the 'MISTRAL_API_KEY' environment variable

### External Dependencies
The project has a number of external dependencies that can be installed via pip
* mistralai
* numpy
* matplotlib
* tree-sitter-java==0.23.2
```
pip install mistralai numpy matplotlib tree-sitter-java==0.23.2
```

There is also one external dependency that must be installed via the github link
* codebleu==0.7.1
```
pip install git+https://github.com/k4black/codebleu.git
```
This is because of dependency resolution issues that arise when installing codebleu from pip (as 0.7.1 is not available via pip and 0.7.0 does not have a compatible and available tree-sitter-java version)

### Python Files
#### prompting_pipeline.py
This python file uses the following dataset pickle files to prompt the LLM with the input functions and calculate codebleu results for each function. It requires the following pickle files:
* secondary_dataset.pkl
* same_param_functions_dataset.pkl
* different_param_functions_dataset.pkl
This python file will generate the following result datasets:
* secondary_mistral_results.pkl
* mistral_results_same.pkl
* mistral_results_diff.pkl
Lines 130-135 have been commented out and therefore when running this python script, only the secondary dataset will be processed to save time and mistral tokens. These lines can be commented if you wish to run the pipeline on the original dataset

#### build_secondary_dataset.py
This python file will build the secondary dataset pickle files using the 'secondary_functions.json' as an input. The output will be 'secondary_dataset.pkl'. 

#### output_averaged_results.py
This python file will compute and output the average codebleu statistics for the secondary dataset using 'secondary_mistral_results.pkl'. It will also generate a bar chart 'Keyword Removal Bars.svg' to depict the keyword removal success visually. 
It requires 'secondary_mistral_results.pkl' however in the presence of 'mistral_results_same.pkl' and 'mistral_results_diff.pkl' as well it can be run across the initial dataset by uncommenting line 229

#### calculate_dataset_statistics.py
This dataset will display statistics for the secondary dataset using 'secondary_dataset.pkl'. It will generate the pie chart 'Term Distribution - Secondary Dataset.svg' and box plot 'Function Length Boxplot - Secondary Dataset.svg'. 
It requires 'secondary_dataset.pkl' however in the presence of 'same_param_functions_dataset.pkl' and 'different_param_functions_dataset.pkl' as well, lines 206 to 223 can be uncommented to generate statistics and diagrams for the initial dataset

#### deprecated_terms.py & utils.py
These two files are not to be run on their own and are used by the other python files, so will be required when running the other python files in this project

#### Notes
All the supporting datasets and results have been included in this repository so there is no specific order to run these python files. 

In the case that the pkl files are not downloaded locally you can still run the entire project over the secondary dataset. 

'utils.py', 'deprecated_terms.py' and 'secondary_functions.json' will still be needed and the files should be run as-is in the following order:
* build_secondary_dataset.py
* prompting_pipeline.py
* output_averaged_results
* calcualte_dataset_statistics


