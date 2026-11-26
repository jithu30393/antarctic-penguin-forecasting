install:
	python3 -m pip install -r requirements.txt
frontend:
	cd frontend && npm install

test:
	python scripts/run_all_tests.py

demo:
	python scripts/run_demo.py
