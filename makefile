all : install_req launch
install_req:
	uv sync
launch:
	cd soft_challange/soft_challange && uv run flask --app . run
