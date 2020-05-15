
rule run_dynamo:
	output: 
		"data.csv"
	shell:
		"python3 dynamo.py"
rule all:
	input:
		"data.csv"
	output:
		"daje.txt"
	shell:
		"echo 'work done' >{output}"

