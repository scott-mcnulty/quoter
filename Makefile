TEST_PATH=./

.PHONY: help
help:
	@echo "    clean"
	@echo "         Cleans local files/dirs made when testing/etc."
	@echo "    up"
	@echo "         Brings up the services in docker-compose.yml."
	@echo "    down"
	@echo "         tears down the services in docker-compose.yml."
	@echo "    test"
	@echo "         Runs py.test on the tests in the tests dir."
	@echo "    docker-test"
	@echo "         Same as test but with but starts up the services in the docker-compose.yml"
	@echo "         then runs the tests."



.PHONY: clean
clean: down
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f  {} +
	rm -r docker-bind-mounts/mysql || true
	rm -r .pytest_cache || true
	rm test-results.xml || true


.PHONY: test
test:
	py.test tests --verbose --junitxml=test-results.xml --pep8 --color=yes $(TEST_PATH)


.PHONY: docker-test
docker-test: clean
	docker-compose up -d mysql;
	@echo "Sleeping for 40 seconds to allow database time to be created if needed";
	sleep 40;
	docker-compose up -d;
	py.test tests --verbose --junitxml=test-results.xml --pep8 --color=yes $(TEST_PATH) || true;
	docker-compose logs > docker-compose-test-logs.log;
	docker-compose down;


.PHONY: up
up:
	docker-compose up


.PHONY: down
down:
	docker-compose down