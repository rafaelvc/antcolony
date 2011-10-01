import sys
import random

import psyco
psyco.full()

def read_matprec(system):

	matprec = []
	fd = open(system + "_precedent_mat.txt")
	line = fd.readline()
	while line: 
		l1 = [ int (x) for x in line.split(",") if not x == "\n" ]
		if l1 == []:
			l1 = None
		matprec.append(l1)
		line = fd.readline()
	fd.close()
	return matprec

def read_mat(system, type, spliter):

	m = []
	fd = open(system + "_" + type + "_mat.txt")
	line = fd.readline()
	while line: 
		l1 = [ x for x in line.split(spliter) if not x == "\n" ]
		if l1 == []:
			l1 = None
		m.append(l1)
		line = fd.readline()
	fd.close()
	return m

def op_troca_simples(s, matprec):

	# print s
	viz = []
	for x in s:
		viz.append(x)
	tam_solucao = len(s)
	viola_res = True
	while viola_res:
		random.seed()
		r1 = random.randrange(0,tam_solucao)
		random.seed()
		r2 = random.randrange(0,tam_solucao)
		viola_res = False
		if r1 == r2:
			viola_res = True
		elif r1 < r2:
			for e in s[r1+1:r2+1]:
				if matprec[e-1] != None and s[r1] in matprec[e-1]:
					viola_res = True
					break
			if not viola_res and matprec[s[r2]-1] != None:
				for e in s[r1+1:r2]:
					if e in matprec[s[r2]-1]:
						viola_res = True 
		 				break
		elif r2 < r1:
			for e in s[r2+1:r1+1]:
				if matprec[e-1] != None and s[r2] in matprec[e-1]:
					viola_res = True
					break
			if not viola_res and matprec[s[r1]-1] != None:
				for e in s[r2+1:r1]:
					if e in matprec[s[r1]-1]:
						viola_res = True
						break
	a = viz[r1]
	viz[r1] = viz[r2]
	viz[r2] = a
	return viz

def fcao2_custo(solucao, mat):
	custo = 0 
	for i in solucao:
	    if mat[i-1] != None:
		    for j in mat[i-1]:
		    	e = j.split("-")
		        if int( e[0] ) not in solucao[ : solucao.index(i)+1 ]:
				custo += int(e[1])
	return custo



def hill_climbing_(escolha_viz, solucao, custo1, mat1, matprec):

	iter = 0
	nr_iter = 10
	nr_vizinhos = 20
	while iter < nr_iter:
		melhora = False
		vizinhanca = vizinhanca_solucao( solucao , nr_vizinhos , matprec )
		for viz in vizinhanca:
			c = fcao2_custo( viz, mat1 )
			if c < custo1:
				custo1 = c
				solucao = viz
				melhora = True 
				iter = 0
				if escolha_viz == "best_first":
					break
		if not melhora:
			iter += 1
	return (solucao,custo1)

def vizinhanca_solucao(s, nrvizinhos, matprec):
	
	nr_iter = 10
	vizinhanca = []
	while nrvizinhos > 0:
		iter = 0
		while iter < nr_iter:
			# 2-opt operator
			viz = op_troca_simples(s, matprec)
			viz = op_troca_simples(viz, matprec)
			if viz not in vizinhanca:
				vizinhanca.append( viz )
				iter = nr_iter
			else:
				iter += 1
		nrvizinhos -= 1
	return vizinhanca	

def pareto_addnd(solucao, custo1, custo2, pareto, pareto_custo1, pareto_custo2):

	t = len(pareto_custo1)
	i = 0
	c1 = c2 = 0
	while i < t:
		c1 = pareto_custo1[i]
		c2 = pareto_custo2[i]
		# solucao dominante, remove dominada 
		if (custo1 <= c1 and custo2 < c2) or (custo1 < c1 and custo2 == c2):
			pareto.pop(i)
			pareto_custo1.pop(i)
			pareto_custo2.pop(i)
			t -= 1
		# solucao dominada ou igual - sem chance 
		elif (custo1 >= c1 and custo2 >= c2):
			return False
		else: 
			i += 1
	pareto.append(solucao)
	pareto_custo1.append(custo1)
	pareto_custo2.append(custo2)
	return True

def run_paco(mat1, mat2, matprec):
	
	#P-ACO Parameters 

#	estudo empirico
#	q0 = 0.98
#	alfa = 1.0
#	beta = 2.0
#	txevaporacao = 0.2
#	t0 = 1.0 # nao tem 
#	tmin = 0.00001 # nao tem 
#	maxit = 80
#	ants = 45

#	selecao de portifolio (legeiramente melhor que flow shop)
	q0 = 0.4
	alfa = 1.0
	beta = 1.0
	txevaporacao = 0.1 
	t0 = 1.0
	tmin = 0.00001 # nao tem
#	## ants = 10
	maxit = 80
	ants = 40

	#flow shop scheduling 
	q0 = 0.75
	alfa = 1.0
	beta = 1.0
	txevaporacao = 0.05
	t0 = 1.0
	tmin = 0.00001
	maxit = 40
	ants = 20

	# Initialize pheromones
	ts = len(mat1)
	matferomonio1 = [ [ t0 for i in range(0,ts) ] for i in range(0,ts) ]
	matferomonio2 = [ [ t0 for i in range(0,ts) ] for i in range(0,ts) ]

	# Initial partial fesiable solution
	cl = classes_iniciais(matprec)

	pareto = []
	pareto_custo1 = []
	pareto_custo2= []

	s1_best_it = []
	s1_second_best_it = [] 
	s2_best_it = []
	s2_second_best_it = [] 
	c1_best_it = 1000 #infinite 
	c1_second_best_it = 1000
	c2_best_it = 1000
	c2_second_best_it = 1000

	it = 0
	while it < maxit:
	
		s1_best_it = []
		s1_second_best_it = [] 
		s2_best_it = []
		s2_second_best_it = [] 
		c1_best_it = 1000 #infinite 
		c1_second_best_it = 1000
		c2_best_it = 1000
		c2_second_best_it = 1000

		ant = 0
		while ant < ants:
		
			random.seed()
			# Initial fesiable vector piece 
			solucao = []
			r =  random.randrange(0, len(cl))
			classe = cl[r]
			solucao.append(classe)
			restantes = [ i for i in range(1,ts+1) if i != classe ] 
			t_restantes = ts-1
			# Path constructions by ant n 
			p1 = random.randrange(0.0,101.0) / 100.0
			p2 = 1.0 - p1
			q = random.randrange(0.0,101.0) / 100.0
			while t_restantes > 0: 

				# Apenas uma restante
				if t_restantes == 1:
					solucao.append(restantes[0])
					break
				
				t_candidatas = 0
				candidatas = []
				for c in restantes:
					if matprec[c-1]:
						restricao = False 
						for p in matprec[c-1]:
							if not (p in solucao):
								restricao = True
								break 
						if not restricao: 
							candidatas.append(c)
							t_candidatas += 1
					else: 
						candidatas.append(c)
						t_candidatas += 1

				# Apenas uma candidata 
				if t_candidatas == 1:
					solucao.append(candidatas[0])
					restantes.remove(candidatas[0])
					t_restantes -= 1
					continue 

				candidatas_prob = []
				total_arg = 0.0
				argmax = 0.0
				arg = 0.0
				for c in candidatas:
					# (Opcionalmente testar com custo parcial)
					custo1 = fcao2_custo_insercao(c,solucao,mat1) # custo insercao obj 1
					custo2 = fcao2_custo_insercao(c,solucao,mat2) # custo inservao obj 2
					arg = (p1 * ((matferomonio1[classe-1][c-1] ** alfa ) * (1.0 / custo1 ** beta))) + (p2 * (( matferomonio2[classe-1][c-1] ** alfa) * (1.0 / custo2 ** beta)))
					total_arg += arg
					candidatas_prob.append(arg)
					if arg > argmax:
						classe = c
						argmax = arg 
	
				# escolhido via roleta senao via argmax 
				if ( q > q0 ):
					prob_candidatas = []
					pij = 0.0
					prob_candidatas = [ pij / total_arg for pij in candidatas_prob ]
					random.seed()
					result = False
					while not result: 
						res = 0 
						for pij in prob_candidatas: 
							r = (random.randrange (0.0,1001.0)) / 1000.0
							if r <= pij:
								classe = candidatas[res]
							 	result = True	
								break
							res +=1 

				solucao.append(classe)
				restantes.remove(classe)
				t_restantes -= 1

			i = 0 
			while i < ts-1:
				matferomonio1[solucao[i]-1][solucao[i+1]-1] = (1 - txevaporacao)*(matferomonio1[solucao[i]-1][solucao[i+1]-1]) + (txevaporacao * t0)
				matferomonio2[solucao[i]-1][solucao[i+1]-1] = (1 - txevaporacao)*(matferomonio2[solucao[i]-1][solucao[i+1]-1]) + (txevaporacao * t0)
				i += 1
		        custo1 = fcao2_custo(solucao, mat1)
			custo2 = fcao2_custo(solucao, mat2)
                        (s1, c1) = hill_climbing_("best_first", solucao, custo1, mat1, matprec)
                        c2 = fcao2_custo(s1, mat2)
                        (s2, c2_) = hill_climbing_("best_first", solucao, custo2, mat2, matprec)
                        c1_ = fcao2_custo(s2, mat1)

			if c1 <= c1_:
				better_local_c1 = c1
				better_s1 = s1
			else:
			        better_local_c1 = c1_
			        better_s1 = s2

			if c2 <= c2_:
                                better_local_c2 = c2
                                better_s2 = s1
                        else:
                                better_local_c2 = c2_
                                better_s2 = s2

			# Check the best and second best iteration for each objective 			
			# Objective 1
			if better_local_c1 < c1_best_it: 
				if ant == 0:
					c1_second_best_it = better_local_c1
					s1_second_best_it = better_s1
				else: 
					c1_second_best_it = c1_best_it
					s1_second_best_it = s1_best_it
				s1_best_it = better_s1
				c1_best_it = better_local_c1
			elif better_local_c1 < c1_second_best_it: 
				c1_second_best_it = better_local_c1
				s1_second_best_it = better_s1
			# Objective 2
			if better_local_c2 < c2_best_it: 
				if ant == 0: 
					c2_second_best_it = better_local_c2
					s2_second_best_it = better_s2
				else:
					c2_second_best_it = c2_best_it
					s2_second_best_it = s2_best_it
				c2_best_it = better_local_c2
				s2_best_it = better_s2  
			elif better_local_c2 < c2_second_best_it: 
				c2_second_best_it = better_local_c2
				s2_second_best_it = better_s2 

			# Global Pheromone Update
			i = 0
			while i < ts: 
		   		j = 0
				while j < ts:
					matferomonio1[i][j] *= (1 - txevaporacao)
					if matferomonio1[i][j] < tmin: 
						 matferomonio1[i][j] = tmin
					matferomonio2[i][j] *= (1 - txevaporacao)
					if matferomonio2[i][j] < tmin: 
						 matferomonio2[i][j] = tmin
					j += 1
				i += 1
		
			# Iteration Best and Second Iteration Best for both Objectives
			i = 0
			while i < ts-1:
				j = 0
				while j < ts-1:
					# Objective 1 
					if s1[i] == s1_best_it[j] and s1[i+1] == s1_best_it[j+1]:
						matferomonio1[ s1[i]-1 ][ s1[i+1]-1 ] += (10 * txevaporacao)
					if s1[i] == s1_second_best_it[j] and s1[i+1] == s1_second_best_it[j+1]:
						matferomonio1[ s1[i]-1 ][ s1[i+1]-1 ] += (5 * txevaporacao) 
					# Objective 2
					if s2[i] == s2_best_it[j] and s2[i+1] == s2_best_it[j+1]:
						matferomonio2[ s2[i]-1 ][ s2[i+1]-1 ] += (10 * txevaporacao)
					if s2[i] == s2_second_best_it[j] and s2[i+1] == s2_second_best_it[j+1]:
						matferomonio2[ s2[i]-1 ][ s2[i+1]-1 ] += (5 * txevaporacao) 
					j += 1

				i += 1


                        # Used for both local search for both objectives
                        pareto_addnd(s1, c1, c2, pareto, pareto_custo1, pareto_custo2)
                        pareto_addnd(s2, c1_, c2_, pareto, pareto_custo1, pareto_custo2)

			ant += 1
		print it
		it += 1

	print pareto_custo1 
	print pareto_custo2
	print pareto 

def fcao2_custo_insercao(classe, solucao, mat):
	classe -= 1
	custo = 1
	if mat[classe]:
		for cc in mat[classe]: 
			e = cc.split("-")
			if not int(e[0]) in solucao:
				custo += int(e[1])
	return custo

def classes_iniciais(matprec):
	iniciais = []
	c = 1
	for prec in matprec: 
		if prec == None:
			iniciais.append(c)
		c += 1
	return iniciais


matprec = read_matprec("D")
mat1 = read_mat("D", "attribute", ",")
mat2 = read_mat("D", "method", ",")
run_paco(mat1, mat2, matprec)
