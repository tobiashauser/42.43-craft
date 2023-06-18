run:
	poetry shell
	draft
clean:
	find . | grep -E "(__pycache__|\.pyc)" | xargs rm -rf
reset: clean
	rm -rf config/
	rm -rf templates/

