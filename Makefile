init:
	pip install -r requirements.txt

test:
	py.test tests

save:
	pip freeze > requirements.txt

.PHONY: init test
