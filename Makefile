CREDCTL := fl-credential-ctl test/credential.conf
MONCTL := fl-monitor-ctl test/monitor.conf
LOG_HOME := ./logs

ifdef URL
	FLOPS = -u $(URL) $(EXT)
else
	FLOPS = $(EXT)
endif

ifdef REPORT_HOME
	REPORT = $(REPORT_HOME)
else
	REPORT = test/report
endif

all: welder-tests

public: solder/public/scripts/weld.js
	solder/requirejs/build/build.sh solder/public/scripts/app.build.js

solder/public/scripts/weld.js: vendor/weld/lib/weld.js
	cp $^ $@

welder-tests:
	-cd vendor/welder; nosetests
	-xsltproc solder/xsl/nosetests.xsl vendor/welder/test/nosetests.xml > solder/public/tests.html

test: start test-app stop

bench: start bench-app stop

start:
	-mkdir -p $(REPORT) $(LOG_HOME)
	-$(MONCTL) restart
	-$(CREDCTL) restart

stop:
	-$(MONCTL) stop
	-$(CREDCTL) stop

test-app:
	fl-run-test -d --debug-level=3 --simple-fetch test_app.py App.test_app $(FLOPS)

bench-app:
	-fl-run-bench --simple-fetch test_app.py App.test_app -c 1:5:10:15:20:30:40:50 -D 45 -m 0.1 -M .5 -s 1 $(FLOPS)
	-fl-build-report $(LOG_HOME)/app-bench.xml --html -o $(REPORT)

clean:
	-find . "(" -name "*~" -or  -name ".#*" -or  -name "*.pyc" ")" -print0 | xargs -0 rm -f

develop: # update
	-(find vendor -mindepth 1 -maxdepth 1 | xargs -Ifoobar -t bash -c "if [ -e foobar/setup.py ]; then cd foobar; echo "foobar"; python setup.py develop; fi")
	-python setup.py develop

update:
	-git pull origin master && git submodule update
	-git submodule summary
