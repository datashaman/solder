CREDCTL := fl-credential-ctl credential.conf
MONCTL := fl-monitor-ctl monitor.conf
LOG_HOME := ./logs

ifdef URL
	FLOPS = -u $(URL) $(EXT)
else
	FLOPS = $(EXT)
endif

ifdef REPORT_HOME
	REPORT = $(REPORT_HOME)
else
	REPORT = reports
endif

all: test

test: start test stop

bench: start bench stop

start:
	mkdir -p $(REPORT) $(LOG_HOME)
	$(MONCTL) restart
	# $(CREDCTL) restart

stop:
	$(MONCTL) stop
	# $(CREDCTL) stop

test:
	fl-run-test -d --debug-level=3 --simple-fetch test_Users.py Users.test_table $(FLOPS)

bench:
	fl-run-bench --simple-fetch test_Users.py Users.test_table -c 1:5:10:15:20:30:40:50 -D 45 -m 0.1 -M .5 -s 1 $(FLOPS)
	fl-build-report --html -o $(REPORT)

clean:
	find . "(" -name "*~" -or  -name ".#*" -or  -name "*.pyc" ")" -print0 | xargs -0 rm -f
