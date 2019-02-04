proto:
	python -m grpc_tools.protoc -Ial-proto --python_out=. --grpc_python_out=. al-proto/protocol.proto
