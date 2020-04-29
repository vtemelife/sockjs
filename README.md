# Vteme sockjs microservice

## Install system dependencies (Ubuntu / OSX)

### Install required services (OSX)

```
brew install pyenv
brew install postgresql
brew install rabbitmq

brew services
brew services start postgresql
brew services start rabbitmq
```

### Install required services (Ubuntu)

```
apt...
```

### Setup pyenv

Please, execute these commands to activate your pyenv (for bash just replace .zshrc with .bashrc)

```
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
eval "$(pyenv init -)"
```

## Setup environment and run project

### Clone repository and install dependencies

```
git clone git@github.com:vtemelife/sockjs.git
cd sockjs
```

### Install and activate virtual environment

```
pyenv install 3.7.4
pyenv shell 3.7.4

python -mvenv env
source env/bin/activate
```

### Activate environment:

```
cp envsets/env.dev .env
source .env
```

### Install project requirements:

```
make install
```

## Start dev server:

```
make start
```

## Run all tests:

```
make test
```

## Run one test:

```
pytest file/path/filename.py::ClassName::test_method
```
