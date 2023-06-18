run:
	poetry shell
	draft
clean:
	find . | grep -E "(__pycache__|\.pyc|.pytest_cache)" | xargs rm -rf
reset: clean
	rm -rf config/
test:
	poetry run pytest -v

