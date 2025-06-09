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