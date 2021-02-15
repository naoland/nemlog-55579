version:
	@which python
	@python -V
init:
	python3 -m venv venv
	./venv/bin/python -m pip install --update pip
	./venv/bin/python -m pip install -r requirements.txt
run:
	./venv/bin/python ./flow-mix.py
test:
	@echo 'not yet ...'