The tests are written using the [behave](https://behave.readthedocs.io/en/latest/) framework
and Python 3.10+ on Windows 10.

User stories can be found in the [user stories](/features) folder, and the tests are in the [features](/features/steps/) folder.

To test the code, first install the dependencies:
```powershell
# Optional: create a virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```


Then in the root directory, run the tests:
```powershell
# run all tests
behave

# run the test with stdout
behave --no-capture

# test a specific feature
behave features/example.feature

# test a specific scenario (first one in the file)
behave features/example.feature:1
```

Alternatively, you can run the tests in VSCode by installing the [Behave VSC](https://marketplace.visualstudio.com/items?itemName=jimasp.behave-vsc) extension.

