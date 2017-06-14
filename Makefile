STACK="apikernos"
IMAGE="apikernos_tester"

help:           ## Show this help.
	@fgrep -h "##" $(MAKEFILE_LIST) | grep -ie '(up|down|dev)' -ive 'fgrep' | awk -F '[:#]' 'BEGIN {OFS=":"} {print $$1,$$4}'

up: stack	## Deploy a new stack or update an existing stack

down: kill-server	## Remove the stack

dev: test	## Deploy an development environment with a tester container

# Brings the backend services up using Docker Stack
stack:
	@docker stack deploy -c docker-compose.yml $(STACK)

# Builds the Docker image used for running tests
test-image:
	@docker build -t "dppascual/$(IMAGE)" -f api/test/Dockerfile .

# Runs unit tests in Docker
test: test-image
	@echo "Deploying development environment"
	@echo "Pass"

kill-server: kill-stack
	@containers=$$(docker ps -a -q --filter name=$(STACK))
	@if [[ -n "$(container)" ]]; then docker rm -f $(containers); fi

kill-stack:
	@if [[ -n $$(docker stack ls | grep -i $(STACK)) ]]; then \
		docker stack rm $(STACK); \
	else \
		echo "The stack is not running"; \
	fi

