# Copilot instructions for Retail Sales Loader

## Project context
- This project loads a local retail CSV using Python 3.11 or later.
- Use the Python standard library. Do not add packages without a stated need.
- Keep source code in src/, sample CSV files in data/, and tests in tests/.
- Read existing code before proposing changes. Preserve public behavior unless
  the task explicitly requests a change.

## Naming conventions
- Use snake_case for Python functions, variables, and module filenames.
- Use PascalCase for classes and UPPER_SNAKE_CASE for constants.
- Use descriptive names such as load_sales and required_columns.
- Avoid vague names such as process_data, temp, or x for business logic.

## Data-loading defaults
- Use pathlib.Path for filesystem paths.
- For CSV input, use csv.DictReader with encoding="utf-8-sig" and newline="".
- Require these CSV headers: order_id, order_date, amount.
- Validate every row before returning data; report the CSV line number on errors.
- Accept dates only in canonical YYYY-MM-DD format and validate calendar dates.
- Treat amount as INR. Use decimal.Decimal for monetary values.
- Reject non-finite amounts and amounts less than or equal to zero.
- Reject blank order IDs, missing fields, and extra fields in rows.
- Return validated records in input order; raise ValueError for invalid data.
- Raise FileNotFoundError for a missing input path. Never silently skip bad rows.
- Use a path relative to the project location, not a hard-coded Windows user path.
- Default to reading inputs only. Do not overwrite source data.

## What NOT to suggest
- Do not hard-code passwords, tokens, connection strings, or real customer data.
- Do not log secrets or full customer records; report counts and safe error context.
- Do not use eval or exec to parse input.
- Do not use float for money, bare except, or empty exception handlers.
- Do not add pandas, Spark, cloud services, or a database for this local CSV task.
- Do not suggest deleting files or destructive writes as the default load pattern.
- Do not invent APIs, project files, table names, or commands.

## Verification and response
- Use unittest for automated tests. Run: python -m unittest discover -s tests -v
- Cover valid input, missing files, malformed dates, missing headers, and bad amounts.
- Explain changed files, behavior, and validation performed.
- If tests were not run, state that clearly. Do not claim a passing test result.
- If an instruction conflicts with the task or existing architecture, explain
  the conflict before proposing a change.
