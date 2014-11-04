test:
	flake8 nagademon2014 --ignore=E501,E122,E126,E128,E127
	coverage run --branch --source=nagademon2014 nagademon2014/manage.py test
	coverage report --omit=nagademon2014/maingame/test*

.PHONY: test


