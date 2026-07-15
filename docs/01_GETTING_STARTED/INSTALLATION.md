# Installation

This guide walks you through installing PipelineModel and preparing your
development environment.

> **Status:** PipelineModel is currently under active development. The
> installation instructions below describe the intended developer
> workflow until the first public release.

## Requirements

PipelineModel targets:

-   Python 3.11 or newer
-   A modern virtual environment manager (recommended: `uv`)
-   Git (for development installs)

## Create a Virtual Environment

Using `uv` (recommended):

``` bash
uv venv
source .venv/bin/activate      # macOS/Linux
# .venv\Scripts\activate      # Windows
```

Or with the Python standard library:

``` bash
python -m venv .venv
source .venv/bin/activate
```

## Install PipelineModel

### From PyPI (future)

``` bash
pip install pipelinemodel
```

### Development Install

Clone the repository:

``` bash
git clone https://github.com/<organization>/pipelinemodel.git
cd pipelinemodel
```

Install in editable mode:

``` bash
pip install -e .
```

or with `uv`:

``` bash
uv pip install -e .
```

## Optional Dependencies

Install only the integrations you need.

Examples:

``` bash
pip install "pipelinemodel[polars]"
pip install "pipelinemodel[pandas]"
pip install "pipelinemodel[airflow]"
pip install "pipelinemodel[all]"
```

## Verify Your Installation

``` python
import pipelinemodel

print(pipelinemodel.__version__)
```

If no errors are raised, your installation is working correctly.

## Recommended Companion Packages

For most projects you will also install:

-   ContractModel
-   Polars (recommended dataframe engine)
-   Pandas (optional compatibility)
-   SQLAlchemy
-   Airflow or another orchestration plugin, when needed

PipelineModel intentionally keeps these integrations optional.

## Keeping Your Installation Updated

PyPI release:

``` bash
pip install --upgrade pipelinemodel
```

Development checkout:

``` bash
git pull
uv pip install -e .
```

## Troubleshooting

### Unsupported Python Version

Ensure you are running Python 3.11 or newer.

### Import Errors

Verify that your virtual environment is activated before installing or
running PipelineModel.

### Missing Plugin

Execution plugins are optional. Install the appropriate extra or plugin
package before attempting to use a specific execution engine.

## Next Step

Continue with **QUICKSTART.md** to build your first typed,
contract-driven pipeline.
