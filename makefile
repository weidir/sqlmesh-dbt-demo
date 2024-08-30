generate:
	python3 data/create_data.py

drop:
	python3 data/drop_data.py

run:
	cd dbt_src && dbt run

test:
	bash tests/run_tests.sh

clean:
	cd dbt_src && dbt clean

generate_run:
	make generate && make run

build:
	docker build -t "kv-test-image" -f docker/dockerfile .

build_nocache:
	docker build --no-cache -t "kv-test-image" -f docker/dockerfile .

run_docker:
	cd docker && docker run -di --name kv-test-container kv-test-image

stop_docker:
	cd docker && docker stop kv-test-container || true && docker rm kv-test-container || true	

build_run:
	make build && make stop_docker && make run_docker

plan:
	cd dbt_src && sqlmesh plan

plan_new:
	cd dbt_src && sqlmesh plan $(env) --include-unmodified

generate_plan:
	make generate && make plan

ui:
	cd dbt_src && sqlmesh ui

container_init:
	bash docker/container_init.sh

metadata:
	bash gov/initialize.sh

init_metadata:
	python3 -m pip install -r gov/requirements-gov.txt && python3 gov/create_gov_role_user_access.py && make metadata

stop_metadata:
	docker stop openmetadata_server || true && docker rm openmetadata_server || true
	docker stop openmetadata_ingestion || true && docker rm openmetadata_ingestion || true
	docker stop openmetadata_postgresql || true && docker rm openmetadata_postgresql || true
	docker stop openmetadata_elasticsearch || true && docker rm openmetadata_elasticsearch || true
	docker stop execute_migrate_all || true && docker rm execute_migrate_all || true
	# docker container prune --force