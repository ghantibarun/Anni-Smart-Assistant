setup:
	pip install -r requirements.txt

run:
	python main.py

test:
	python -m pytest tests/ -v

format:
	black .

clean:
	powershell -NoProfile -Command "Get-ChildItem -Path . -Directory -Recurse -Force -ErrorAction SilentlyContinue | Where-Object Name -In '__pycache__','.pytest_cache' | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue"