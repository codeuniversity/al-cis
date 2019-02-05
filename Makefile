dep:
	if [ ! -d "env" ];then virtualenv env;fi
	env/bin/pip install -r requirements.txt

proto:
	env/bin/python -m grpc_tools.protoc -Ial-proto --python_out=. --grpc_python_out=. al-proto/protocol.proto

run:
	env/bin/python main.py
