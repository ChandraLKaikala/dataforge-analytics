.PHONY: install deps seed run test docs clean help

help:
	@echo "DataForge Analytics Platform — dbt + DuckDB"
	@echo ""
	@echo "Available commands:"
	@echo "  make install      - Install Python dependencies"
	@echo "  make deps         - Install dbt packages"
	@echo "  make seed         - Load reference data (seeds)"
	@echo "  make run          - Run all dbt models"
	@echo "  make test         - Run all dbt tests"
	@echo "  make docs         - Generate and serve dbt docs"
	@echo "  make clean        - Remove build artifacts and DuckDB database"
	@echo "  make dashboard    - Run Streamlit dashboard"
	@echo ""

install:
	pip install -r requirements.txt

deps:
	cd dataforge && dbt deps

seed:
	cd dataforge && dbt seed

run:
	cd dataforge && dbt run

test:
	cd dataforge && dbt test

docs:
	cd dataforge && dbt docs generate && dbt docs serve

dashboard:
	streamlit run dashboard/app.py

generate-data:
	python scripts/generate_data.py

full-setup: install generate-data deps seed run test
	@echo "✓ Full setup complete! Run 'make docs' to view lineage or 'make dashboard' to start Streamlit"

clean:
	rm -rf dataforge/target dataforge/dbt_packages dataforge/logs dataforge/*.duckdb* ~/.dbt

.DEFAULT_GOAL := help
