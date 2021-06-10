# Minimal makefile for Sphinx documentation

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = docs
BUILDDIR      = build

# Put it first so that "make" without argument is like "make help".
help:
	@echo "Please use 'make target' where target is one of"
	@echo "html        to make standalone HTML files"
	@echo "ru          to make messages translation for russian language"
# $(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile html ru

DOMAIN=turing_machine
TRANSLATIONS_DIR=.

ru: $(TRANSLATIONS_DIR)/ru/LC_MESSAGES/$(DOMAIN).mo

$(DOMAIN).pot: gui.py
	pybabel extract -o $@ $^

# TODO init if no dir

$(TRANSLATIONS_DIR)/ru/LC_MESSAGES/$(DOMAIN).po: $(DOMAIN).pot
	pybabel update -D $(DOMAIN) -i $^ -d $(TRANSLATIONS_DIR) -l ru

$(TRANSLATIONS_DIR)/ru/LC_MESSAGES/$(DOMAIN).mo: ru/LC_MESSAGES/$(DOMAIN).po
	pybabel compile -D $(DOMAIN) -i $^ -o $@

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
html: Makefile
	$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
