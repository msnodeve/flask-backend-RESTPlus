GREEN=\033[1;32;40m
RED=\033[1;31;40m
NC=\033[0m # No Color

test:
	@bash -c "echo -e \"${GREEN}[pytest 시작]${NC}\"" 
	pipenv run pytest app/tests --cov-report=html:cov_html --cov-report=term --cov=app