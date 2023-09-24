# KARTAL: Web Application Vulnerability Hunting Using Large Language Models

This repository contains all files used in the research of KARTAL, a novel method for web application vulnerability detection using finetuned large language models.
You can view the published paper on (https://aaltodoc.aalto.fi/handle/123456789/122780)[https://aaltodoc.aalto.fi/handle/123456789/122780].

## Directory Structure

- data/ (contains datasets in CSV format)
- prompt-templates/ (contains prompt template files for data generation)
- src/
  - benchmark/ (contains benchmarking code for LLMs)
  - data-generation/ (contains data generation and cleaning code)
  - plotting/ (contains plotting code)

## Requirements

To run the KARTAL project, you need the following:

- Python 3.10+
- PyTorch 2

or

- Docker 20+

## How to Run

For data generation using the `prompter.py` script you will need to create a `.env` file. Use the `.env-example`file as the template and fill in the required values. You can get them from the respective LLM API dashboard.

### Native

1. Install Python 3.10+ on your system.
2. (Optional) Create virtual environment using `python3 -m venv env`
3. Install the required Python packages by running the following command:

```shell
pip install -r requirements.txt
```

3. Run experiments or data generation scripts located in the `src/` directory.

### Docker

1. Build the Docker image by running :

```shell
docker build -t kartal .
```

2. Run the Docker container using the built image and specify the Python file to run:

```shell
docker run --gpus all -it kartal python src/benchmark/{file_name}.py
```

Replace `{file_name}` with the path to your desired Python file within the `src/` directory.

## Citation
@article{Sakaoglu2023,
title={{KARTAL: Web Application Vulnerability Hunting Using Large Language Models}},
author={Sakaoglu, Sinan},
year={2023},
language={English},
pages={85+8},
keywords={vulnerability detection, large language models, web applications, application security, AI, broken acccess ontrol},
url={http://urn.fi/URN:NBN:fi:aalto-202308275121}
} 

## License

Copyright 2023 Sinan Sakaoglu

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

