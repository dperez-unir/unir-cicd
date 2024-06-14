.PHONY: all $(MAKECMDGOALS)

build:
        docker build -t calculator-app .

run:
        docker run --rm --volume `pwd`:/opt/calc --env PYTHONPATH=/opt/calc -w /opt/calc calculator-app:latest python -B app/calc.py

server:
        docker run --rm --volume `pwd`:/opt/calc --name apiserver --network-alias apiserver --env PYTHONPATH=/opt/calc --env FLASK_APP=app/api.py -p 5000:5000 -w /opt/calc calculator-app:latest flask run --host=0.0.0.0

interactive:
        docker run -ti --rm --volume `pwd`:/opt/calc --env PYTHONPATH=/opt/calc  -w /opt/calc calculator-app:latest bash

test-unit:
        docker run --rm --volume `pwd`:/opt/calc --env PYTHONPATH=/opt/calc -w /opt/calc calculator-app:latest pytest --cov --cov-report=xml:results/coverage.xml --cov-report=html:results/coverage --junit-xml=results/unit_result.xml -m u>
        docker run --rm --volume `pwd`:/opt/calc --env PYTHONPATH=/opt/calc -w /opt/calc calculator-app:latest junit2html results/unit_result.xml results/unit_result.html

test-behavior:
        docker run --rm --volume `pwd`:/opt/calc --env PYTHONPATH=/opt/calc -w /opt/calc calculator-app:latest behave --junit --junit-directory results/  --tags ~@wip test/behavior/
        docker run --rm --volume `pwd`:/opt/calc --env PYTHONPATH=/opt/calc -w /opt/calc calculator-app:latest bash test/behavior/junit-reports.sh

test-api:
        docker network create calc-test-api || true
        docker stop apiserver || true
        docker rm --force apiserver || true
        docker run -d --rm --volume `pwd`:/opt/calc --network calc-test-api --env PYTHONPATH=/opt/calc --name apiserver --env FLASK_APP=app/api.py -p 5000:5000 -w /opt/calc calculator-app:latest flask run --host=0.0.0.0
        docker run --rm --volume `pwd`:/opt/calc --network calc-test-api --env PYTHONPATH=/opt/calc --env BASE_URL=http://apiserver:5000/ -w /opt/calc calculator-app:latest pytest --junit-xml=results/api_result.xml -m api  || true
        docker run --rm --volume `pwd`:/opt/calc --env PYTHONPATH=/opt/calc -w /opt/calc calculator-app:latest junit2html results/api_result.xml results/api_result.html
        docker stop apiserver || true
        docker rm --force apiserver || true
        docker network rm calc-test-api

test-e2e:
        docker network create calc-test-e2e || true
        docker stop apiserver || true
        docker rm --force apiserver || true
        docker stop calc-web || true
        docker rm --force calc-web || true
        docker run -d --rm --volume `pwd`:/opt/calc --network calc-test-e2e --env PYTHONPATH=/opt/calc --name apiserver --env FLASK_APP=app/api.py -p 5000:5000 -w /opt/calc calculator-app:latest flask run --host=0.0.0.0
        docker run -d --rm --volume `pwd`/web:/usr/share/nginx/html --volume `pwd`/web/constants.test.js:/usr/share/nginx/html/constants.js --volume `pwd`/web/nginx.conf:/etc/nginx/conf.d/default.conf --network calc-test-e2e --name calc->
        docker run --rm --volume `pwd`/test/e2e/cypress.json:/cypress.json --volume `pwd`/test/e2e/cypress:/cypress --volume `pwd`/results:/results  --network calc-test-e2e cypress/included:4.9.0 --browser chrome || true
        docker rm --force apiserver
        docker rm --force calc-web
        docker run --rm --volume `pwd`:/opt/calc --env PYTHONPATH=/opt/calc -w /opt/calc calculator-app:latest junit2html results/cypress_result.xml results/cypress_result.html
        docker network rm calc-test-e2e

test-e2e-wiremock:
        docker network create calc-test-e2e-wiremock || true
        docker stop apiwiremock || true
        docker rm --force apiwiremock || true
        docker stop calc-web || true
