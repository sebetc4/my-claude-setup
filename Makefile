# Drive the Claude Code directory from this repository, one domain at a time.

ROOT := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
CLAUDE_DIR ?= $(HOME)/.claude
SETUP = python3 -B "$(ROOT)tools/claude_setup.py" --claude-dir "$(CLAUDE_DIR)" $(if $(filter 1,$(FORCE)),--force)

.DEFAULT_GOAL := help
.PHONY: help list enable update disable check

help:
	@echo "Usage:"
	@echo "  make list                  every domain and its state: off, on, outdated, modified"
	@echo "  make enable  D=<domain>    install a domain into $(CLAUDE_DIR)"
	@echo "  make update  [D=<domain>]  reinstall one domain, or every enabled domain"
	@echo "  make disable D=<domain>    remove a domain"
	@echo "  make check                 run the repository checks and tests"
	@echo ""
	@echo "Options: FORCE=1 overrides conflicts; CLAUDE_DIR=<dir> targets another directory."

list:
	@$(SETUP) list

enable:
	@$(SETUP) enable $(D)

update:
	@$(SETUP) update $(D)

disable:
	@$(SETUP) disable $(D)

check:
	@python3 -B "$(ROOT)tests/check.py"
