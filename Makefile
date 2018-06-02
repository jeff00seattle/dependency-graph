#   Makefile
#
# license   http://opensource.org/licenses/MIT The MIT License (MIT)
#

PYTHON3 := $(shell which python3)
REQ_FILE := requirements.txt

install-requirements: $(REQ_FILE)
	@echo "======================================================"
	@echo install-requirements
	@echo "======================================================"
	$(PYTHON3) -m pip install --upgrade -r $(REQ_FILE)

start:
	@echo "======================================================"
	@echo start
	@echo "======================================================"
	$(PYTHON3) tasks-manager.py

list:
	cat Makefile | grep "^[a-z]" | awk '{print $$1}' | sed "s/://g" | sort