dep:
	if [ ! -d "env" ];then python3 -m venv env;fi
	env/bin/pip install -r requirements.txt

proto:
	env/bin/python -m grpc_tools.protoc -Ial-proto --python_out=. --grpc_python_out=. al-proto/protocol.proto

run:
	env/bin/python main.py

image:
	docker build -t codealife/al-cis .

check-format:
	env/bin/pycodestyle $$(ls | grep '.*.py' | grep -v '.*pb2.*')

autoformat:
	env/bin/autopep8 -ia $$(ls | grep '.*.py' | grep -v '.*pb2.*')

docker-push:
	echo "${DOCKER_PASSWORD}" | docker login -u "${DOCKER_USERNAME}" --password-stdin
	docker push codealife/al-cis:latest
