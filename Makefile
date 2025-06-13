all: 
	python src/main.py

initvenv:
	@echo "Creating virtual environment..."
	python3 -m venv venv
	@echo "Virtual environment created."

activate:
	@echo "Activating virtual environment..."
	source venv/bin/activate
	@echo "Virtual environment activated."

teste:
	python src/teste.py

clean:
	@echo "Cleaning up..."
	rm -rf venv
	rm -rf __pycache__
	rm -rf *.pyc
	@echo "Cleanup complete."
