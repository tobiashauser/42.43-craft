PYTHON = python3
POETRY = poetry
CHECKSTYLE = flake8
TEST = pytest
PYTHON_FILES = $(shell find . -name "*.py")

draft:
	$(POETRY) shell
	$(POETRY) install
compile:
	$(PYTHON) -m py_compile $(PYTHON_FILES)
test:
	$(PYTHON) -m doctest $(PYTHON_FILES)
	$(POETRY) run $(TEST)
checkstyle:
	$(CHECKSTYLE) $(PYTHON_FILES)
clean:
	find . -name "*.pyc" | xargs rm -f
	find . -name "__pycache__" | xargs rm -rf
	find . -name "*.aux" -o -name "*.fdb_latexmk" -o -name "*.fls" -o -name "*.log" -o -name "*synctex.gz" | xargs rm -f
