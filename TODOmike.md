Interdiction.py: 
Write the following functions:
	- get_cover - basically just has to run .optimize on MRG and retrieve the current best cover and the objective value (so we can check if we have to keep interdicting)
	- get_kappa - i think for this one we have to clear out the KAP model and redefine it everytime, because it has a completely different number of vars and stuff depending on the cover we are getting the kappa value for

	- once we wrote those a bit we'll write the main callback loop in solve() together
	
