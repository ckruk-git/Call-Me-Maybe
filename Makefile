install:
	python -m pip install pygame flake8 mypy

run:
	python main.py

debug:
	python -m pdb main.py

clean:
	rm -rf __pycache__ .mypy_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +

lint:
	flake8 . 
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
lint-strict:
	flake8 .
	mypy . --strict

.PHONY: install run debug clean lint lint-strict
