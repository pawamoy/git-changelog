.DEFAULT_GOAL := help
SHELL := bash
DUTY := $(if $(VIRTUAL_ENV),,pdm run) duty
export PDM_MULTIRUN_VERSIONS ?= 3.8 3.9 3.10 3.11 3.12

args = $(foreach a,$($(subst -,_,$1)_args),$(if $(value $a),$a="$($a)"))
check_quality_args = files
docs_args = host port
release_args = version
test_args = match

BASIC_DUTIES = \
	changelog \
	check-api \
	check-dependencies \
	clean \
	coverage \
	docs \
	docs-deploy \
	format \
	release \
	vscode

QUALITY_DUTIES = \
	check-quality \
	check-docs \
	check-types \
	test

.PHONY: help
help:
	@$(DUTY) --list

.PHONY: lock
lock:
	@pdm lock -G:all

.PHONY: setup
setup:
	@bash scripts/setup.sh

.PHONY: check
check:
	@pdm multirun duty check-quality check-types check-docs
	@$(DUTY) check-dependencies check-api

.PHONY: $(BASIC_DUTIES)
$(BASIC_DUTIES):
	@$(DUTY) $@ $(call args,$@)

.PHONY: $(QUALITY_DUTIES)
$(QUALITY_DUTIES):
	@pdm multirun duty $@ $(call args,$@)
