version:
	@which python
	@python -V
init:
	python3 -m venv venv
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install -r requirements.txt
run:
	./venv/bin/python ./flow.py
copy:
	cp ./dist/flow.dot.png ~/storage/downloads
test:
	@echo 'not yet ...'