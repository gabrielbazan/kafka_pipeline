

VIRTUALENV_PATH=./venv


API_REQUIREMENTS_FILE_PATH=./api/requirements.txt
REDUCER_REQUIREMENTS_FILE_PATH=./reducer/requirements.txt
DATABASE_SYNC_REQUIREMENTS_FILE_PATH=./database_sync/requirements.txt


create_virtualenv:
	@echo "Creating virtualenv..."
	python3 -m venv "${VIRTUALENV_PATH}"
	@echo "Done!"


install_requirements:
	@echo "Installing requirements..."
	${VIRTUALENV_PATH}/bin/pip install -r "${API_REQUIREMENTS_FILE_PATH}" && \
	${VIRTUALENV_PATH}/bin/pip install -r "${REDUCER_REQUIREMENTS_FILE_PATH}" && \
	${VIRTUALENV_PATH}/bin/pip install -r "${DATABASE_SYNC_REQUIREMENTS_FILE_PATH}"
	@echo "Done!"


run_tests:
	@echo "Running tests..."
	./run_unit_tests.sh
	@echo "Done!"


install_git_hooks:
	pre-commit install


run_git_hooks:
	pre-commit run --all-files


up:
	docker compose build && docker compose up


down:
	docker compose down


rm:
	docker compose rm --volumes --force
