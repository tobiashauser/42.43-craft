run:
	hatch run draft --help
clean:
	find . | grep -E "(__pycache__|\.pyc)" | xargs rm -rf
reset: clean
	hatch env prune
