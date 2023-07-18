PYTHON = python3
POETRY = poetry
CHECKSTYLE = flake8
TEST = pytest
PYTHON_FILES = $(shell find . -name "*.py")
MAIN_FILES = $(shell find . -name "main.py")

draft:
	$(POETRY) shell
	$(POETRY) install
test:
	$(PYTHON) -m doctest $(PYTHON_FILES)
	$(POETRY) run $(TEST)
clean:
	find . -name "*.pyc" | xargs rm -f
	find . -name "__pycache__" | xargs rm -rf
	find . -name "*.aux" -o -name "*.fdb_latexmk" -o -name "*.fls" -o -name "*.log" -o -name "*synctex.gz" | xargs rm -f
release:
	sed -i '' 's/tests.common.test_common_Configuration/draft.configuration.Configuration/' $(MAIN_FILES)
	sed -i '' 's/tests.new.test_Compiler/draft.new.Compiler/' draft/new/Subcommands.py
debug:
	sed -i '' 's/draft.configuration.Configuration/tests.common.test_common_Configuration/' $(MAIN_FILES)
	sed -i '' 's/draft.new.Compiler/tests.new.test_Compiler/' draft/new/Subcommands.py
