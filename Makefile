public: solder/public/scripts/weld.js
	solder/requirejs/build/build.sh solder/public/scripts/app.build.js

solder/public/scripts/weld.js: vendor/weld/lib/weld.js
	cp $^ $@

clean:
	find . -name '*.py[co]' -ls -delete

update:
	# git pull && git submodule update
	python setup.py develop
	find vendor -mindepth 1 -maxdepth 1 | xargs -n 1 -Ifoobar -t bash -c "if [ -e foobar/setup.py ]; then cd foobar; python setup.py develop; fi"
	git submodule summary
