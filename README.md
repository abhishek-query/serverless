
# Serverless Platform Drivers (using Demisto)

Descrption of what we're doing and why goes here.

## Testing

You can run this code in your terminal by doing the following:

Install `asdf` using your OS package manager or follow the instructions [here](http://asdf-vm.com/guide/getting-started.html)

Next, install these plugins for asdf
```
$ asdf plugin add python
$ asdf plugin-add poetry https://github.com/asdf-community/asdf-poetry.git
```

Make sure ~/.asdf/shims is added to your $PATH in your shell's startup scripts
```
$ $SHELL -c 'echo $PATH'
```

It won't be added to the path in your current shell, so either open a new terminal, or
```
$ export PATH=""~/.asdf/shims:$PATH"
```

Now change directories to this repository:
```
$ cd serverless
```

Install the version of Python and poetry we're using
```
$ asdf install
```

Install required Python packages
```
$ poetry install
```

 Run the test
```
$ export PYTHONPATH=.:./Packs/Base/Scripts/CommonServerPython:./Packs/ApiModules/Scripts
$ poetry run python lambda_function.py
```
