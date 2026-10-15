# Copilot Custom Instructions — Ready-to-Test Lab

## Requirements
- Python 3.11 or later. No pip packages are required.
- VS Code, plus GitHub Copilot access to test AI responses.
- Git only if you want to commit the project.

The loader and tests run without Copilot or an internet connection.

## Open on Windows
1. Right-click the ZIP and select Extract All.
2. In VS Code select File > Open Folder.
3. Open the extracted retail-sales-loader folder containing this README.
   Do not open only an individual file or the outer ZIP folder.
4. Select your Python 3.11+ interpreter if prompted.
5. Open Terminal > New Terminal. Run all commands below from this folder.

## Run the included reference implementation
python --version
python src/sales_loader.py

Expected output:
Loaded records: 3
Total amount (INR): 2449.75

If python is not available but the Windows launcher is installed, replace
python with py -3 in the commands. Confirm it selects Python 3.11+.

## Run the included tests
python -m unittest discover -s tests -v

Expected: 11 tests, OK. Subtests cover additional invalid input values.
Tests use temporary files and leave data/sales.csv unchanged.

## Test Copilot instructions
Open .github/copilot-instructions.md and read the rules.
Open Copilot Chat in this workspace and start a new chat.
Use the prompts in docs/copilot-test-prompts.md.
Inspect response references/context for the instruction file where available,
and check the response against naming, loading and prohibited-pattern rules.
These instructions guide supported Chat/agent requests; they do not affect
inline suggestions while typing and are not an enforced security boundary.

This ZIP already contains reference code. To test generation from scratch,
make a separate copy of the project, remove src/sales_loader.py from that copy,
then request a proposed loader in Copilot Chat. Keep tests for validation.
Save the generated loader, run the tests, and compare actual behavior.
Do not treat similarity to the existing code alone as proof of instruction use.

## Find the files
Ctrl+P in VS Code > type .github/copilot-instructions.md > Enter.
Use Explorer to open data/sales.csv, src/sales_loader.py, or tests/.
Right-click a file > Reveal in File Explorer to locate it on Windows.

## Peer review
Complete docs/peer-review.md with the actual prompts, observed references,
code findings and tests you ran. Submit using your normal team process.
The packaged template is blank; no peer review has been performed.

## Optional local Git commit
This ZIP does not include Git history. Run:
git init
git add .github README.md .gitignore src data tests docs tutorial.html
git diff --cached
git commit -m "Add Copilot custom instructions lab"

If Git requests identity, configure your own user.name and user.email first.
The commit is local. This project does not configure or push to a remote.

## Tutorial
Open tutorial.html in your browser for the full 60-minute guide.

## Scope
This is a local CSV validation training project, not a production ETL system.
No credentials, external services, VS Code settings overrides, or pip packages
are included. Keep your existing project policies when adapting instructions.
