run:
	@uvicorn store.main:app --reload --port 8080

test:
	@poetry run pytest -s -rx

test-matching:
	@poetry run pytest -s -rx -k $(K) --pdb store ./tests/
