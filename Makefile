PYTHON = python3
POETRY = poetry
CHECKSTYLE = flake8
TEST = pytest
PYTHON_FILES = $(shell find . -name "*.py")
MAIN_FILES = $(shell find . -name "main.py")

install-pypi:
	pip3 install craft-documents
install:
	poetry build
	pip install dist/craft_documents-0.1.1-py3-none-any.whl
uninstall:
	pip3 uninstall craft-documents
publish:
	make release
	poetry build
	poetry publish
	make debug
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
	trash ~/.config/draft/
release:
	sed -i '' 's/tests.common.test_common_Configuration/craft_documents.configuration.Configuration/' $(MAIN_FILES)
	sed -i '' 's/tests.new.test_Compiler/craft_documents.new.Compiler/' craft_documents/new/Subcommands.py
debug:
	sed -i '' 's/craft_documents.configuration.Configuration/tests.common.test_common_Configuration/' $(MAIN_FILES)
	sed -i '' 's/craft_documents.new.Compiler/tests.new.test_Compiler/' craft_documents/new/Subcommands.py
