lint:
	pre-commit run --all-files

update-isort:
	seed-isort-config

copy:
	@rsync -avz \
		--exclude 'tmp' \
		--exclude '.env' \
		--exclude '.idea' \
		--exclude '.DS_Store' \
		--exclude '.git' \
		--exclude '*.pyc' \
		--exclude '__pycache__' \
		--exclude 'bandit-report.html' \
		. srb_market_dev:/opt/blabla_bot/
