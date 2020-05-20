numbers=[0,1,2,3] 

rule all:
	input: 
		expand("simulation_{number}.png", number=numbers),
		"lyapunov_exp.png",
		"lyapunov_exp.dat",
	output:
		"simulation_results.log"
	shell:
		"cat 'lyapunov_exp.dat' > {output}"



rule create_images:
	input:
		expand("simulation_{number}.csv", number=numbers) 
	output:
		"simulation_{number}.png"
	script:
		"image_creator.py"

rule calculate_lyapunov:
	input:
		expand("simulation_{number}.csv", number=numbers) 
	output:
		"lyapunov_exp.png",
		"lyapunov_exp.dat"
	script:
		"lyapunov.py"

rule generate_data:
	input:
		"input_values.txt"
	output:
		expand("simulation_{number}.csv", number=numbers)
	script:
		"dynamo.py"
	






