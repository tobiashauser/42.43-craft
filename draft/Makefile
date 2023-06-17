run:
	hatch run draft
clean:
	find . | grep -E "(__pycache__|\.pyc)" | xargs rm -rf
reset: clean
	hatch env prune
