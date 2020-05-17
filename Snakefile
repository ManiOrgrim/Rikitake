numbers=[0,1,2,3]


rule all:
	input:
		expand("simulation_{number}.png", number=numbers)
	output:
		"simulation_0.log"
	shell:
		"echo 'job done' > {output}"
rule sim_0:
	output:
		"simulation_0.csv"
	shell:
		"python3 dynamo.py 1 2 10000 0 0 0 {output}"
rule sim_1:
	output:
		"simulation_1.csv"
	shell:
		"python3 dynamo.py 1 2 10000 0.1 0 0 {output}"
rule sim_2:
	output:
		"simulation_2.csv"
	shell:
		"python3 dynamo.py 1 2 10000 0 0.1 0 {output}"
rule sim_3:
	output:
		"simulation_3.csv"
	shell:
		"python3 dynamo.py 1 2 10000 0 0 0.1 {output}"
		
rule create_image0:
	input:
		"simulation_0.csv"
	output:
		"simulation_0.png"
	shell:
		"python3 image_creator.py {input}"

rule create_image1:
	input:
		"simulation_1.csv"
	output:
		"simulation_1.png"
	shell:
		"python3 image_creator.py {input}"

rule create_image2:
	input:
		"simulation_2.csv"
	output:
		"simulation_2.png"
	shell:
		"python3 image_creator.py {input}"
rule create_image3:
	input:
		"simulation_3.csv"
	output:
		"simulation_3.png"
	shell:
		"python3 image_creator.py {input}"
