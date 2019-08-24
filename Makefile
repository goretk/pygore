APP = pygore

SHELL = /bin/bash
DIR = $(shell pwd)

REPO_URL=https://joakimkennedy.keybase.pub/gore-test

NO_COLOR=\033[0m
OK_COLOR=\033[32;01m
ERROR_COLOR=\033[31;01m
WARN_COLOR=\033[33;01m
MAKE_COLOR=\033[33;01m%-20s\033[0m
PYTHON=python3
BUILD_OPTS=bdist_wheel
LIBGORE_FILES={libgore.so,libgore.dll,libgore.dylib}
LIBGORE_URL=https://api.github.com/repos/goretk/libgore/releases/latest

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
	@rm -rfv build/ dist/ pygore.egg-info/ pygore/$(LIBGORE_FILES) dltmp

.PHONY: deploy_local
deploy_local: ## Deploy local libgore files
	@cp -v $(LIBGORE)/$(LIBGORE_FILES) pygore/.

.PHONY: upload
upload: ## Upload package to pypi
	@twine upload dist/*

.PHONY: download
download: ## Download latest release of libgore
	@mkdir -p dltmp
	@curl -sL `curl -s $(LIBGORE_URL) | grep browser_download_url | cut -d '"' -f 4 | grep linux` | bsdtar -xvf - -C dltmp
	@curl -sL `curl -s $(LIBGORE_URL) | grep browser_download_url | cut -d '"' -f 4 | grep darwin` | bsdtar -xvf - -C dltmp
	@curl -sL `curl -s $(LIBGORE_URL) | grep browser_download_url | cut -d '"' -f 4 | grep windows` | bsdtar -xvf - -C dltmp
	@cp -v dltmp/*/$(LIBGORE_FILES) pygore/.

.PHONY: fetch_data
fetch_data: ## Fetch test resources
	@mkdir -p test/resources
	@curl -o test/resources/golden -# -L $(REPO_URL)/gold-linux-amd64-1.12.0

.PHONY: test
test: ## Run tests
	@$(PYTHON) -m unittest discover -v -s test -t .
