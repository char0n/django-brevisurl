bootstrap:
	pip install -e . --use-mirrors
	pip install "file://`pwd`#egg=brevisurl" --use-mirrors
	./scripts/setup.sh
	python manage.py syncdb --noinput --migrate


test: bootstrap
	@echo "Running Python tests"
	python manage.py test brevisurl
	@echo ""

clean:
	rm -rf ./dist
	rm -rf ./django_brevisurl.egg-info
	rm -rf test.db
	rm -rf settings.py