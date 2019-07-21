APP = pygore

SHELL = /bin/bash
DIR = $(shell pwd)

NO_COLOR=\033[0m
OK_COLOR=\033[32;01m
ERROR_COLOR=\033[31;01m
WARN_COLOR=\033[33;01m
MAKE_COLOR=\033[33;01m%-20s\033[0m
PYTHON=python3
BUILD_OPTS=bdist_wheel
LIBGORE=$(GOPATH)/src/github.com/goretk/libgore
LIBGORE_FILES={libgore.so,libgore.dll}

.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo -e "$(OK_COLOR)==== $(APP) [$(VERSION)] ====$(NO_COLOR)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(MAKE_COLOR) : %s\n", $$1, $$2}'

.PHONY: build
build: ## Build pip package
	@echo -e "Building $(OK_COLOR)[$(APP)] package $(NO_COLOR)"
	@$(PYTHON) ./setup.py $(BUILD_OPTS)

.PHONY: clean
clean: ## Remove folders created by build
	@rm -rfv build/ dist/ pygore.egg-info/ pygore/$(LIBGORE_FILES)

.PHONY: deploy_local
deploy_local: ## Deploy local libgore files
	@cp -v $(LIBGORE)/$(LIBGORE_FILES) pygore/.

.PHONY: upload
upload: ## Upload package to pypi
	@twine upload dist/*

