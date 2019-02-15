dep:
	if [ ! -d "env" ];then virtualenv env;fi
	env/bin/pip install -r requirements.txt

proto:
	env/bin/python -m grpc_tools.protoc -Ial-proto --python_out=protobuffer --grpc_python_out=protobuffer al-proto/protocol.proto

run:
	env/bin/python main.py

image:
	docker build -t al-cis .

check-format:
	env/bin/pycodestyle *.py

autoformat:
	env/bin/autopep8 -ia *.py
