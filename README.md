# Requirements
* MacOS >=11
* Python 3.12
* [Appium driver](https://github.com/appium/appium-mac2-driver)
* [Allure](https://allurereport.org/docs/gettingstarted-installation/)

# Installation
Project preferably should be installed in [virtual environment](https://docs.python.org/3/library/venv.html).

```bash
cd test_project/
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

# Test execution
Current version of the project has hardcoded paths and requires to be run from main directory (`test_project`)

```bash
pytest tests/
```

# Report generation
`Allure` will generate interactive test report

```bash
allure serve allure-results
```

Example report was saved to `example-report/index.html`. Reference command is:

```bash
allure generate --single-file allure-results 
```
