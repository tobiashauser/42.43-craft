PYTHON = python3
POETRY = poetry
CHECKSTYLE = flake8
TEST = pytest
PYTHON_FILES = $(shell find . -name "*.py")

compile:
	$(PYTHON) -m py_compile $(PYTHON_FILES)
test:
	$(PYTHON) -m doctest $(PYTHON_FILES)
checkstyle:
	$(CHECKSTYLE) $(PYTHON_FILES)
clean:
	find . -name "*.pyc" | xargs rm -f
	find . -name "__pycache__" | xargs rm -rf
