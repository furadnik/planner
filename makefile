main:
	python -m coverage run -m manage test && python -m coverage report --show-miss --fail-under=100

.PHONY: main
