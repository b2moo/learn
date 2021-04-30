from maximal_cubes import *
import z3
import mondec
import json
import importlib

def load_smt(fname):
	"""Load formula from SMT2 file"""
	target_vector = parse_smt2_file(fname)
	
	# iterate the vector and from it build a AND formula
	formula = z3.And([form for form in target_vector])

	var = z3util.get_vars(formula)

	def lambda_model(value):
		"""The mondec algorithm requires a lambda function as an input, instantiating
		the formula with any list of free variables.
		Note that substitue() may have an overhead (direct lambda specification
		may be faster)
		"""
		return substitute(formula, *((vname, value[i]) for (i, vname) in enumerate(var)))
	return (formula, var, lambda_model)

def load_python(mname, params):
	"""Load from python file in the benchmark subdir"""
	module = importlib.import_module('benchmarks.' + mname)

	var = module.build_variables(*params)
	def lambda_model(value):
		return module.build_formula(*params, value)
	
	form = lambda_model(var)
	return (form, var, lambda_model)

def run_exp(model, max_cube = True, u = False, b = False, o = True, md=False):
	
	formula, var, lambda_model = model

	print("Variables: %r" % var)
	print("Formula: %r" % formula)
	
	start = time.time()
	if md:
		result = mondec.mondec(lambda_model, var)
	elif max_cube:
		teacher = Teacher(var, formula)
		learner = Learner_max_cubes(var, unary = u, binary = b, optimized = o)
		result = learner.learn(teacher)
	else:
		teacher = Teacher(var, formula)
		learner = Learner_trial_and_overshoot(var, unary = u, binary = b)
		result = learner.learn(teacher, formula)	
	end = time.time()
	print("Res: %r" % result)
	print("Total time needed: ", end - start)
	return result

if __name__ == '__main__':
	if len(sys.argv) < 3:
		print("Usage: %s [overshoot-u|overshoot-b|max-u|max-b|max-o|mondec] [filename.smt2|pythonmodule.py extraparams]")
		sys.exit(0)

	fname = sys.argv[2]
	
	m1 = False
	u1 = False
	b1 = False
	o1 = False
	md = False
	if sys.argv[1] == "overshoot-u":
		u1 = True
	elif sys.argv[1] == "overshoot-b":
		b1 = True
	elif sys.argv[1] == "max-u":
		m1 = True
		u1 = True
	elif sys.argv[1] == "max-b":
		m1 = True
		b1 = True
	elif sys.argv[1] == "max-o":
		m1 = True
		o1 = True
	elif sys.argv[1] == "mondec":
		md= True
	else:
		print("Unknown solver: %s" % sys.argv[1])
		sys.exit(1)
	if fname.endswith('.py'):
		mname = fname[:-3]
		# parse rest of args as json
		args = [json.loads(s) for s in sys.argv[3:]]
		model = load_python(mname, args)
	else:
		model = load_smt(fname)
	run_exp(model, max_cube = m1, u = u1, b = b1, o = o1, md=md)
