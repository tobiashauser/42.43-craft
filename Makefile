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
release:
	sed -i '' 's/tests.common.test_common_Configuration/draft.configuration.Configuration/' draft/new/main.py
debug:
	sed -i '' 's/draft.configuration.Configuration/tests.common.test_common_Configuration/' draft/new/main.py