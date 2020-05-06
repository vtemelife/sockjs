# Vteme sockjs microservice

Dev stack:
* asyncio
* sockjs
* rabbitmq
* redis
* docker

## Clone repository

Install git on your system https://git-scm.com/book/en/v2/Getting-Started-Installing-Git

```
git clone git@github.com:vtemelife/sockjs.git
cd sockjs
```

## Run using docker

Install docker on your system https://runnable.com/docker/getting-started/

### Activate environment:

```
cp envsets/docker_dev.env .docker.env
```

### Build and Run

```
docker-compose build
docker-compose up
```

## Run without docker

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

### Install and activate virtual environment

```
pyenv install 3.7.4
pyenv shell 3.7.4

python -mvenv env
source env/bin/activate
```

### Activate environment:

```
cp envsets/local_dev.env .env
source .env
```

### Install project requirements:

```
make install
```

### Start dev server:

```
make start
```

### Run tests:

### Run all tests:

```
make test
```

### Run one test:

```
pytest file/path/filename.py::ClassName::test_method
```
