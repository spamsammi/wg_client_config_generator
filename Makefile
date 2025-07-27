precondition:
	@uv --version 1>/dev/null || (echo "uv is not installed | sh" && exit 1)
	@wg --version 1>/dev/null || (echo "wireguard is not installed" && exit 1)

run: precondition
	uv run main.py $(args)