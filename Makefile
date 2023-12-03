FORMATTER = black
LINTER = ruff
TYPE_CHECKER = mypy

.PHONY: code
code: code/format code/lint code/type

.PHONY: code/lint
code/lint:
	$(LINTER) --fix ./

.PHONY: code/format
code/format:
	$(FORMATTER) ./

.PHONY: code/type
code/type:
	$(TYPE_CHECKER) ./