class SolverModifyer(object):
	def __init__(self,solverproto):
		self.__solverproto = solverproto
		self.__solver_param={}
		self.__get_solver_param()
		
		for key in self.__solver_param.keys():
			setattr(self,key,self.__solver_param[key])

	def creat_solver(self):
		return self.__solverproto


	def __get_solver_param(self):

		for line in open(self.__solverproto):
			self.__solver_param[line.strip().split(":")[0]]=line.strip().split(":")[1]

	def save(self):
		with open(self.__solverproto,"w") as sp:
				for key in self.__solver_param.keys():
					sp.write(":".join([key,self.__solver_param[key]]))
					if key!=self.__solver_param.keys()[-1]:
						sp.write("\n")
		sp.close()
	

	def __getattribute__(self,item):
		
		return object.__getattribute__(self, item)



	def __getattr__(self,item):

		setattr(self,item, getattr(self,item))