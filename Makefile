

VIRTUALENV_PATH=./venv


API_REQUIREMENTS_FILE_PATH=./api/requirements.txt
DATA_PROCESSOR_REQUIREMENTS_FILE_PATH=./data_processor/requirements.txt
DATABASE_SYNC_REQUIREMENTS_FILE_PATH=./database_sync/requirements.txt

API_TEST_REQUIREMENTS_FILE_PATH=./api/requirements.test.txt

create_virtualenv:
	@echo "Creating virtualenv..."
	python3 -m venv "${VIRTUALENV_PATH}"
	@echo "Done!"


install_requirements:
	@echo "Installing requirements..."
	${VIRTUALENV_PATH}/bin/pip install -r "${API_REQUIREMENTS_FILE_PATH}" && \
	${VIRTUALENV_PATH}/bin/pip install -r "${DATA_PROCESSOR_REQUIREMENTS_FILE_PATH}" && \
	${VIRTUALENV_PATH}/bin/pip install -r "${DATABASE_SYNC_REQUIREMENTS_FILE_PATH}"
	@echo "Done!"


install_test_requirements:
	@echo "Installing requirements..."
	${VIRTUALENV_PATH}/bin/pip install -r "${API_TEST_REQUIREMENTS_FILE_PATH}"
	@echo "Done!"


run_tests:
	@echo "Running tests..."
	${VIRTUALENV_PATH}/bin/pytest
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
