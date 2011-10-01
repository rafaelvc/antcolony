#!/usr/bin/env python

import psyco
psyco.full()

import sys
import random

matprec = []

def read_matprec(system):

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

def read_mat(system, type, spliter, f):

	m = []
	fd = open(system + "_" + type + "_mat.txt")
	line = fd.readline()
	while line: 
		l1 = [ f(x) for x in line.split(spliter) if not x == "\n" ]
		if l1 == []:
			l1 = None
		m.append(l1)
		line = fd.readline()
	fd.close()
	return m

def individuos_violam_dep(solucao, mat):
       ind_dep = []
       for s in solucao:
            cont = 0
            if mat[s-1] != None:
                 for dep in mat[s-1]:
                      if dep not in solucao[:solucao.index(s)]:
                           ind_dep.append(s)
                           break
       return ind_dep

# op troca viola com outro que viola
def op_troca_x(s,mat):
	viz = [ x for x in s ]	
	vl = individuos_violam_dep(s,mat)
	t = len(vl)
	ts = len(s)
	viola_res = True
	while viola_res:
		random.seed()
		el1 = random.randrange(0,t)
		el2 = random.randrange(0,t)
		viola_res = False

		if el1 == el2:
			viola_res = True
			continue 
		r1 = s.index(vl[el1])
		r2 = s.index(vl[el2])

		if r1 == r2: 
			viola_res = True
		elif r1 < r2:
			for e in s[r1+1:r2+1]:
				if s[r1] in matprec[e-1]:
					viola_res = True
					break
			if not viola_res and matprec[s[r2]-1] != None:
				for e in s[r1+1:r2]:
					if e in matprec[s[r2]-1]:
						viola_res = True 
		 				break
		elif r2 < r1:
			for e in s[r2+1:r1+1]:
				if s[r2] in matprec[e-1]:
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

# op trova viola um com outro que nao viola
def op_troca_y(s, mat):
	viz = [ x for x in s ]	
	vl = individuos_violam_dep(s, mat)
	t = len(vl)
	ts = len(s)
	viola_res = True
	while viola_res:
		random.seed()
		el1 = random.randrange(0,t)
		viola_res = False
		r1 = s.index(vl[el1])
		r2 = random.randrange(0,ts)
		while s[r2] in vl:  
			r2 = random.randrange(0,ts)
		if r1 == r2: 
			viola_res = True
		elif r1 < r2:
			for e in s[r1+1:r2+1]:
				if s[r1] in matprec[e-1]:
					viola_res = True
					break
			if not viola_res and matprec[s[r2]-1] != None:
				for e in s[r1+1:r2]:
					if e in matprec[s[r2]-1]:
						viola_res = True 
		 				break
		elif r2 < r1:
			for e in s[r2+1:r1+1]:
				if s[r2] in matprec[e-1]:
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

def op_troca_simples(s, extra):

	# print s
	viz = [ x for x in s ]
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
#	print solucao
	for i in solucao:
#	    print "item ",  i
#	    print "violcaoes ", mat[i-1]
#	    print i
	    if mat[i-1] != None:
		    for j in mat[i-1]:
		    	e = j.split("-")
		        if int( e[0] ) not in solucao[ : solucao.index(i)+1 ]:
				custo += int(e[1])

#		print solucao[ : solucao.index(i)+1 ]
#	    print "------------------------------------"
	return custo

def fcao_custo(solucao, mat):
	dep = 0
	for i in solucao:
	   if mat[i-1] != None: 
               for j in mat[i-1]:
	           if (int(j) not in solucao[ : solucao.index(i)+1 ]):
	              dep += 1
	return dep


def pareto_local_search (op, escolha_viz, fcusto, mat1, mat2, solucao, c1_, c2_, pareto):

	iter = 0
	nr_iter = 20
	nr_vizinhos = 20
	nr_viz = 0

	pareto.append( (solucao, c1_, c2_) ) 
	# Pareto Best First
	while iter < nr_iter:
		viz = vizinhanca_solucao ( solucao , 1 , op, [] ) [0]
		c1 = fcusto( viz, mat1 )
		c2 = fcusto( viz, mat2 )
		ndominada = True
		for (s,c1_,c2_) in pareto:
			# solucao dominante, remove dominada 
			if (c1 <= c1_ and c2 < c2_) or (c2 <= c2_ and c1 < c1_):
				pareto.remove((s,c1_,c2_))
			# solucao dominada, sem chance 
			elif (c1 >= c1_ and c2 > c2_) or (c2 >= c2_ and c1 > c1_):
				ndominada = False
				break
		if ndominada:
			pareto.append((viz, c1, c2))
			solucao = viz
		else: 
			if nr_viz < nr_vizinhos: 
				nr_viz += 1 
			else:
				nr_viz = 0
				iter += 1

#		vizinhanca = vizinhanca_solucao( solucao , nr_vizinhos , op, [] )
#		melhora = False
#		for viz in vizinhanca:
#			c1 = fcusto( viz, mat1 )
#			c2 = fcusto( viz, mat2 )
#			ndominada = True
#			for (s,c1_,c2_) in pareto:
				# solucao dominante, remove dominada 
#				if (c1 <= c1_ and c2 < c2_) or (c2 <= c2_ and c1 < c1_):
#					pareto.remove((s,c1_,c2_))
				# solucao dominada, sem chance 
#				elif (c1 >= c1_ and c2 > c2_) or (c2 >= c2_ and c1 > c1_):
#					ndominada = False
#					break
#			if ndominada:
#				if pareto and (viz,c1,c2) not in pareto: 
#					pareto.append((viz, c1, c2))
#					melhora = True 
#					iter = 0
#				else:
#					melhora = False
#				solucao = viz
#				c1_ = c1
#				c2_ = c2
#		if not melhora: 
#			iter += 1


def hill_climbing_(op, escolha_viz, solucao, custo1, mat1, fcusto):

	iter = 0
	nr_iter = 10
	nr_vizinhos = 20
	while iter < nr_iter:
		melhora = False
		vizinhanca = vizinhanca_solucao( solucao , nr_vizinhos , op, [] )
		for viz in vizinhanca:
			c = fcusto( viz, mat1 )
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


def inicial_aleatoria(mat):
	
	tamanho_solucao = len(matprec)
	solucao = []
	t = 0
        i = 0
	independentes = []
	for prec in matprec:
		i += 1
		if prec == None:
			independentes.append(i)

	while len(independentes) > 1:
		random.seed()
		r = random.randrange(0,len(independentes))
		solucao.append( independentes[r] )
		independentes.remove( independentes[r] )
	solucao.append( independentes[0] )
	t = len(solucao)	
	restantes = [ i for i in range(1,tamanho_solucao+1) if i not in solucao ] 		
	t_restantes = len(restantes)
	while t_restantes > 0:
		tem_preced = True
		random.seed()
		r = random.randrange(0,t_restantes)
		# print solucao, "-", restantes, r, t_restantes
		for pre in matprec[restantes[r]-1]:
			# print pre
			if pre not in solucao:
				tem_preced = False
				break
		if tem_preced: 
			solucao.append( restantes[r] )
			restantes.remove( restantes[r] )
			t_restantes -= 1
	return solucao


def inicial_gulosa(mat):
	s = gera_solucao_gulosa(mat)
	solucao = op_troca_simples(s, '')
	return solucao

def ins_pendente(solucao,pendentes):

	remove_p = []
	for p in pendentes:
		restricao = False
		for prec in matprec[p-1]:
			if prec not in solucao:
				restricao = True
				break
		if not restricao:
			solucao.append(p)
			remove_p.append(p)

	for p in remove_p: 
		pendentes.remove(p)

	return pendentes

def gera_solucao_gulosa(mat):

	t = len(mat)
	solucao = []
	pendentes = []
	elemens = [ (len(mat[i]),i+1) for i in range(0,t) ]
	
	while elemens != []:

		menor_dep = 100 
		for e in elemens:
			if e[0] <= menor_dep:
				menor_dep = e[0]
				elemen = e[1]

		# verifica se nao viola restricao 
		restricao = False
		if matprec[elemen-1] != None: #nao tem restricao
			for prec in matprec[elemen-1]: 
				if not prec in solucao:
					restricao = True
					break
		if restricao: 
			# tenta inserir pendentes 
			pendentes = ins_pendente(solucao,pendentes)
			pendentes.append(elemen)	
		else:
			solucao.append(elemen)

		# elemen ja faz parte da solucao entao remove
		# ou esta na lista de pendentes
		elemens.remove ( (menor_dep, elemen) )
	
	while pendentes != []:
		pendentes = ins_pendente(solucao,pendentes)

	return solucao

def vizinhanca_solucao(s, nrvizinhos, op, mat):
	
	nr_iter = 100
	vizinhanca = []
	
	while nrvizinhos > 0:
		iter = 0
		while iter < nr_iter:
			# 2-opt operator
			viz = op(s, mat)
			viz = op(viz, mat)
			if viz not in vizinhanca:
				vizinhanca.append( viz )
				iter = nr_iter
			else:
				iter += 1
		nrvizinhos -= 1
	return vizinhanca	

#####################================= ACO ===================

## Pareto SET: 
def pareto_addnd(solucao, custo1, custo2, pareto):

	for (s,c1,c2) in pareto:
		# solucao dominante, remove dominada 
		if (custo1 <= c1 and custo2 < c2) or (custo1 < c1 and custo2 == c2):
			pareto.remove((s,c1,c2))
		# solucao dominada ou igual - sem chance 
		elif (custo1 >= c1 and custo2 >= c2):
			return False
	pareto.append((solucao,custo1,custo2))
	return True


## Path relink:
def path_relink(s1, s2, custo1, custo2, matprec):

	# movimentos para deixar a solucao s1 igual s2
	j = 0
	c = custo2
	for i in s1: 
		if i != s2[j]:
			movimentos.append( (s1.index(s2[j]), j) )
		j += 1
	s = s1
	k = 0
	while movimentos:	
		(i,j) = movimentos[k]
		t = s[i]
		s[i] = s[j] 
		s[j] = t
		c = fcao_custo (s)
		if c < custo2:
			#aplica busca local e sai
			#mercado 
			pass
		elif c > custo1:
			s = s1	
		else:
			s1 = s
		k += 1
		movimentos = movimentos[k:]
	

def run_acobicriteria(mat1, mat2, matprec):
	
	#Parametros
	nrformigas = 40
	beta = 1
	alfa = 1
	# beta = 4 
	# alfa = 2 
	maxit = 80
	txevaporacao = 0.05
	# tmin = 0.05
	tmin = 0.0001


	ts = len(mat1)

	#Inicializa feromonio 
	matferomonio1 = [ [ tmin for i in range(0,ts) ] for i in range(0,ts) ]
	matferomonio2 = [ [ tmin for i in range(0,ts) ] for i in range(0,ts) ]

	#Classes iniciais
	cl = classes_iniciais(matprec)

	pareto = []
	solucoes_ = []
	solucoes_local_ = []

	for it in range(0,maxit):

		pareto_local = []
		random.seed()
		for f in range(0,nrformigas):
			
			# Initial fesiable vector piece 
			solucao = []
			classe = cl[ random.randrange(0, len(cl)) ]
			solucao.append(classe)
			restantes = [ i for i in range(1,ts+1) if i != classe ] 

			# Path constructions by ant n 
			lks = []
			while restantes != []: 	
				(proxima,(custo1,custo2)) = proxima_classe(classe, solucao, restantes, mat1, mat2, matprec, matferomonio1, matferomonio2, alfa, beta, f+1, nrformigas)	
				solucao.append(proxima)
				restantes.remove(proxima)
				classe = proxima

			# PATH relink strategy 
			# bi objective pcao path relink 
			# iteration best e ligada com alguma solucao do conjunto de pareto, duas maneiras:
			# 1 - it best com relacao a f1(f2) em direcao da melhor solucao com relacao f2(f1) de pareto
			# 2 - ligar uma iteration bet com com uma solucao randomica de pareto
			# duas estrategias de ligacao: 
			# LCS longest common substring (somente solucao que aumentam o lcs em direcao a x2 sao consideradas)
			# Hamming distance (deve diminuir a distrancia, ou seja diferencas entre x1 x2)
			# (somente solucao que sao no dominadas por todas as vizinhacas sao consideradas) pare reduzir os caminhos entre x1 e x2
			# random agregation para selecionar por qual das nao dominadas segguir
			# aplica busca local em PR e atualiza o conjunto pareto
			
			y = (f) / (nrformigas - 1)
			if (y > (random.randrange(0,101) / 100.0)):
				hill_climbing_ (op_troca_simples, "best_all", None, fcao2_custo, mat1, mat2, solucao, pareto_local, 1, solucoes_local_)
			else:
				hill_climbing_ (op_troca_simples, "best_all", None, fcao2_custo, mat1, mat2, solucao, pareto_local, 0, solucoes_local_)

		#Trail update (evaporation) both objectives 
		for i in range(0, ts):
			for j in range (0,ts):
				if matferomonio1[i][j] <= tmin: 
					 matferomonio1[i][j] = tmin
				else:
					matferomonio1 [i][j] = (1 - txevaporacao)*matferomonio1[i][j]
				if matferomonio2[i][j] <= tmin: 
					 matferomonio2[i][j] = tmin
				else:
					 matferomonio2 [i][j] = (1 - txevaporacao)*matferomonio2[i][j]
		# Trail update by local pareto set 
		l = len(pareto_local)
		# for (s,c1,c2) in pareto_local:
		#	for i in range(0,ts-1):	
		#		matferomonio1 [s[i]-1][s[i+1]-1] += (1.0/l)
		#		matferomonio2 [s[i]-1][s[i+1]-1] += (1.0/l)
		# Update global pareto set 	
		for (s,c1,c2) in pareto_local: 
			if (s1,c1,c2) not in pareto: 
				if pareto_addnd(s, c1, c2, pareto):
					for i in range(0,ts-1):	
						matferomonio1 [s[i]-1][s[i+1]-1] += (1.0/l)
						matferomonio2 [s[i]-1][s[i+1]-1] += (1.0/l)


	
	custo1_ = []
	custo2_ = []
	solucoes = []
	print pareto 
	print "PARETO: "
	for (s,c1,c2) in pareto:
		custo1_.append(c1)
		custo2_.append(c2)
		solucoes.append(s)
	print custo1_
	print custo2_
	print solucoes
	
	custo1_ = []
	custo2_ = []
	print "SOLUCOES: "
	for (c1,c2) in solucoes_:
		custo1_.append(c1)
		custo2_.append(c2)
	print custo1_
	print custo2_
	
	custo1_ = []
	custo2_ = []
	print "LOCAL:" 
	for (c1,c2) in solucoes_local_:
		custo1_.append(c1)
		custo2_.append(c2)
	print custo1_
	print custo2_


def run_paco(mat1, mat2, matprec):
	
	#P-ACO Parameters 
	nrformigas = 45
	# beta = 4.0
	# alfa = 2.0
	alfa = 1.0
	beta = 1.0
	maxit = 80
	txevaporacao = 0.05
	# tmin = 0.05
	t0 = 1.0
	tmin = 0.00001
	q0 = 0.75
	
	# Initialize pheromones
	ts = len(mat1)
	matferomonio1 = [ [ t0 for i in range(0,ts) ] for i in range(0,ts) ]
	matferomonio2 = [ [ t0 for i in range(0,ts) ] for i in range(0,ts) ]

	# Initial partial fesiable solution
	cl = classes_iniciais(matprec)

	pareto = []
	solucoes_ = []
	solucoes_local_ = []

	s1_best_it = []
	s1_second_best_it = [] 
	s2_best_it = []
	s2_second_best_it = [] 
	c1_best_it = 1000 #infinite 
	c1_second_best_it = 1000
	c2_best_it = 1000
	c2_second_best_it = 1000

	for it in range(0,maxit):

		for f in range(0,nrformigas):
		
			random.seed()
			# Initial fesiable vector piece 
			solucao = []
			classe = cl[ random.randrange(0, len(cl)) ]
			solucao.append(classe)
			restantes = [ i for i in range(1,ts+1) if i != classe ] 
		
			# Path constructions by ant n 
			lks = []
			w = random.randrange(0.0,101.0) / 100.0
			while restantes != []: 	
				(proxima,(custo1,custo2)) = proxima_classe_(classe, solucao, restantes, mat1, mat2, matprec, matferomonio1, matferomonio2, alfa, beta, f+1, nrformigas, q0, w)	
				solucao.append(proxima)
				restantes.remove(proxima)

				# Local Pheromone Update by edge drop down (visita)
				# matferomonio1[classe-1][proxima-1] = (1 - txevaporacao)*(matferomonio1[classe-1][proxima-1]) + (txevaporacao * tmin)
				# matferomonio2[classe-1][proxima-1] = (1 - txevaporacao)*(matferomonio2[classe-1][proxima-1]) + (txevaporacao * tmin)
			# Local Pheromone Update by path construction 
			for s in range(0,ts-1):	
				matferomonio1[solucao[s]-1][solucao[s+1]-1] = (1 - txevaporacao)*(matferomonio1[solucao[s]-1][solucao[s+1]-1]) + (txevaporacao * tmin)
				matferomonio2[solucao[s]-1][solucao[s+1]-1] = (1 - txevaporacao)*(matferomonio2[solucao[s]-1][solucao[s+1]-1]) + (txevaporacao * tmin)
			#	if matferomonio1[solucao[s]-1][solucao[s+1]-1] < tmin:
			#		matferomonio1[solucao[s]-1][solucao[s+1]-1] = tmin
			#	if matferomonio2[solucao[s]-1][solucao[s+1]-1] < tmin:
			#		matferomonio2[solucao[s]-1][solucao[s+1]-1] = tmin
			# Local Search  - slide from objective 1 to 2

			# Each ant takes some objective 
#			solucoes_local_ = []
#			y = (f) / (nrformigas - 1)
#			if (y > (random.randrange(0,101) / 100.0)):
#				hill_climbing_ (op_troca_simples, "best_first", None, fcao2_custo, mat1, mat2, solucao, pareto, 1, solucoes_local_)
#			else:
#				hill_climbing_ (op_troca_simples, "best_first", None, fcao2_custo, mat1, mat2, solucao, pareto, 0, solucoes_local_)

			# Local Search  - one local search a objective
#			(better1, c1, n1) = hill_climbing_ (op_troca_simples, "best_all", None, fcao2_custo, mat1, mat2, solucao, pareto, 1, solucoes_local_)
#			(better2, c2, n2) = hill_climbing_ (op_troca_simples, "best_all", None, fcao2_custo, mat1, mat2, solucao, pareto, 0, solucoes_local_)

			pareto_local = []
			pareto_local_search (op_troca_simples, "best_first", fcao2_custo, mat1, mat2, solucao, custo1, custo2, pareto_local)

			# Local search by w - poor results  
			#if w > 0.5:   
			#	(solucao, custo1) = hill_climbing_(op_troca_simples, "best_first", solucao, custo1, mat1, fcao2_custo)
			#	custo2 = fcao2_custo(solucao, mat2)
			#else: 
			#	(solucao, custo2) = hill_climbing_(op_troca_simples, "best_first", solucao, custo2, mat2, fcao2_custo)
			#	custo1 = fcao2_custo(solucao, mat1)

			#One local search by objective
			# (s1, c1) = hill_climbing_(op_troca_simples, "best_first", solucao, custo1, mat1, fcao2_custo)
			# c2 = fcao2_custo(s1, mat2)
			# (s2, c2_) = hill_climbing_(op_troca_simples, "best_first", solucao, custo2, mat2, fcao2_custo)
			# c1_ = fcao2_custo(s2, mat1)
			
			# if c1 <= c1_: 
			#	better_local_c1 = c1
			#	better_s1 = s1
			#else:
			#	better_local_c1 = c1_
			#	better_s1 = s2

			#if c2 <= c2_:
			#	better_local_c2 = c2
			#	better_s2 = s1
			#else:
			#	better_local_c2 = c2_
			#	better_s2 = s2


			# Get betters of local search pareto (Used for local_pareto_serach)
			better_local_c1 = 1000
			better_local_c2 = 1000
			better_s1 = []
			better_s2 = []
			for (s,c1,c2) in pareto_local:
				if c1 < better_local_c1: 
					better_local_c1 = c1
					better_s1 = s 
				if c2 < better_local_c2: 
					better_local_c2 = c2
					better_s2 = s
			
			# Used for local search by w
			# if it == 0: 
			#	better_s1 = solucao
			#	better_s2 = solucao 
			# better_local_c1 = custo1
			# better_local_c2 = custo2 
			
			# Check the best and second best iteration for each objective 			
			# Objective 1
			if better_local_c1 < c1_best_it: 
				if it == 0:
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
				if it == 0: 
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
			# Iteration Best and Second Iteration Best for both Objectives
			for i in range(0, ts):
		   		for j in range (0,ts):
					# Objective 1 
					matferomonio1[i][j] *= (1 - txevaporacao)
					if matferomonio1[i][j] < tmin: 
						 matferomonio1[i][j] = tmin
					# edge i,j is in both it and sec it best
					if ( s1_best_it.index(i+1)+1 < ts and 
						s1_best_it[ s1_best_it.index(i+1)+1 ] == j+1 and 
						  s1_second_best_it and s1_second_best_it.index(i+1)+1 < ts and
						    s1_second_best_it [ s1_second_best_it.index(i+1)+1 ] == j+1 ): 
						matferomonio1[i][j] += 15
					# edge i,j just in it best
					elif  s1_best_it.index(i+1)+1 < ts and s1_best_it[ s1_best_it.index(i+1)+1 ] == j+1: 
						matferomonio1[i][j] += 10
					# edge i,j just in sec it best
					elif s1_second_best_it and (s1_second_best_it.index(i+1)+1) < ts and s1_second_best_it [ s1_second_best_it.index(i+1)+1 ] == j+1: 
						   matferomonio1[i][j] += 5
					# Objective 2
					matferomonio2[i][j] *= (1 - txevaporacao)
					if matferomonio2[i][j] < tmin: 
						 matferomonio2[i][j] = tmin
					# edge i,j is in both it and sec it best
					if ( s2_best_it.index(i+1)+1 < ts and 
						s2_best_it[ s2_best_it.index(i+1)+1 ] == j+1 and 
						    s2_second_best_it and  s2_second_best_it.index(i+1)+1 < ts and
							s2_second_best_it [ s2_second_best_it.index(i+1)+1 ] == j+1 ): 
						matferomonio2[i][j] += 15
					# edge i,j just in it best
					elif  s2_best_it.index(i+1)+1 < ts and s2_best_it[ s2_best_it.index(i+1)+1 ] == j+1: 
						matferomonio2[i][j] += 10
					# edge i,j just in sec it best
					elif s2_second_best_it and s2_second_best_it.index(i+1)+1 < ts and s2_second_best_it [ s2_second_best_it.index(i+1)+1 ] == j+1: 
						matferomonio2[i][j] += 5

			#Update Global Pareto set (used for local pareto search)
			for (s,c1,c2) in pareto_local:
				pareto_addnd(s, c1, c2, pareto)

			# Used for local search by w
			# pareto_addnd(solucao, custo1, custo2, pareto )

			# Used for both local search for both objectives
 			# pareto_addnd(s1, c1, c2, pareto)
 			# pareto_addnd(s2, c1_, c2_, pareto)

		print it



	custo1_ = []
	custo2_ = []
	print "PARETO: "
	for (s,c1,c2) in pareto:
		custo1_.append(c1)
		custo2_.append(c2)
	print custo1_
	print custo2_
	print pareto
	
#	custo1_ = []
#	custo2_ = []
#	print "SOLUCOES: "
#	for (c1,c2) in solucoes_:
#		custo1_.append(c1)
#		custo2_.append(c2)
#	print custo1_
#	print custo2_
	
#	custo1_ = []
#	custo2_ = []
#	print "LOCAL:" 
#	for (c1,c2) in solucoes_local_:
#		custo1_.append(c1)
#		custo2_.append(c2)
#	print custo1_
#	print custo2_

def proxima_classe_(classe, solucao, restantes, mat1, mat2, matprec, matfer1, matfer2, alfa, beta, a, ants, q0, w):
	
	lk_candidatas = []
	prob_candidatas = []
	soma_pij = 0
	escolhido = 0

	candidatas = []
	for c in restantes:
		if matprec[c-1] != None:
			restricao = False
			for p in matprec[c-1]:
				if p not in solucao:
					restricao = True
					break
			if not restricao:
				candidatas.append(c)
		else:
			candidatas.append(c)
 	
	# y = (a - 1) / (ants - 1)
	# w[0] = y 
	# w[1] = 1 - y
	fer1 = fer2 = 0.0

	for c in candidatas:
		fer1 += matfer1[classe-1][c-1]
		fer2 += matfer2[classe-1][c-1]
	maxarg = 1000 # infinito 
	custo_p1 = fcao2_custo(solucao, mat1)
	custo_p2 =  fcao2_custo(solucao, mat2)
	if custo_p1 == 0.0:
		custo_p1 = 1.0
	if custo_p2 == 0.0:
		custo_p2 = 1.0
	maxarg = 0.0
	for c in candidatas:
		custo = custo_p1
		custo2 = custo_p2
		# Calcula o custo de insercao da candidata para objetivo 1
		if mat1[c-1] != None:
			for cc in mat1[c-1]: 
				e = cc.split("-")
				if int(e[0]) not in solucao:
					custo += int(e[1])
		# Calcula o custo de insercao da candidata para objetivo 2
		if mat2[c-1] != None:
			for cc in mat2[c-1]: 
				e = cc.split("-")
				if int(e[0]) not in solucao:
					custo2 += int(e[1])
		
		# w [0] = random.randrange(0.0,101.0) / 100.0
		# w [1] = 1.0 - w[0]
		# arg = (w[0] * ((fer1 ** alfa ) * (1.0 / custo ** beta))) + (w[1] * ((fer2 ** alfa) * (1.0 / custo2 ** beta)))
		arg = (w * ((fer1 ** alfa ) * (1.0 / custo ** beta))) + ((1.0-w) * ((fer2 ** alfa) * (1.0 / custo2 ** beta)))
		soma_pij += arg
		prob_candidatas.append(arg)
		lk_candidatas.append((custo, custo2))
		if arg > maxarg:
			escolhido = c
			maxarg = arg 	

	# escolhido via argmax
	q = random.randrange(0.0,101.0) / 100.0
	if ( q <= q0 ):
		return (escolhido, lk_candidatas[candidatas.index(c)])

	prob_candidiatas = [ pij / soma_pij for pij in prob_candidatas ]
	random.seed()
	while True: 
		res = 0 
		for pij in prob_candidatas: 
			r = (random.randrange (0,1000)) / 1000.0 
			if r <= pij:
				return (candidatas[res], lk_candidatas[res])
			res += 1 		


def proxima_classe(classe, solucao, restantes, mat1, mat2, matprec, matfer1, matfer2, alfa, beta, a, ants):
#def proxima_classe(classe, solucao, restantes, mat, matprec, t, matfer, alfa, beta):

	# Seleciona Candidatas
	candidatas = []
	for c in restantes:
		if matprec[c-1] != None:
			restricao = False
			for p in matprec[c-1]:
				if p not in solucao:
					restricao = True
					break
			if not restricao:
				candidatas.append(c)
		else:
			candidatas.append(c)

	lk_candidatas = []
	prob_candidatas = []
	soma_pij = 0
	custo_p1 = fcao2_custo(solucao, mat1)
	custo_p2 =  fcao2_custo(solucao, mat2)

 	y = (a - 1) / (ants - 1)

	if custo_p1 == 0.0:
		custo_p1 = 1.0
	if custo_p2 == 0.0:
		custo_p2 = 1.0
	for c in candidatas:
		custo = custo_p1
		custo2 = custo_p2
		
		# Calcula o custo de insercao da candidata para objetivo 1
		if mat1[c-1] != None:
			for cc in mat1[c-1]: 
				e = cc.split("-")
				if int(e[0]) not in solucao:
					custo += int(e[1])

		# Calcula o custo de insercao da candidata para objetivo 2
		if mat2[c-1] != None:
			for cc in mat2[c-1]: 
				e = cc.split("-")
				if int(e[0]) not in solucao:
					custo2 += int(e[1])

		pij = (matfer1[classe-1][c-1] ** (alfa * y)) * (matfer2[classe-1][c-1] ** (alfa * (1.0-y)))  *  (1.0 / (1.0 * custo) ** (beta * y) ) * (1.0 / (1.0 * custo2) ** (beta * (1.0-y)))
		# print matfer1, matfer2
		soma_pij += pij
		prob_candidatas.append(pij)
		lk_candidatas.append((custo, custo2))

	# roleta
	prob_candidiatas = [ pij / soma_pij for pij in prob_candidatas ]
	random.seed()
	while True: 
		res = 0 
		for pij in prob_candidatas: 
			r = (random.randrange (0,1000)) / 1000.0 
			if r <= pij:
				return (candidatas[res], lk_candidatas[res])
			res += 1 		

def classes_iniciais(matprec):

	iniciais = []
	c = 1
	for prec in matprec: 
		if prec == None:
			iniciais.append(c)
		c += 1
	return iniciais

matprec = read_matprec("D")
# mat = read_mat("D", "dependency", ",", (lambda x: x))
mat1 = read_mat("D", "attribute", ",", (lambda x: x))
mat2 = read_mat("D", "method", ",", (lambda x: x))
# run_paco(mat1, mat2, matprec)
# run_acobicriteria(mat1, mat2, matprec)
# s = [17,1,36,31,42,5,28,18,41,27,26,30,6,8,33,9,10,14,11,12,13,15,16,20,7,19,35,45,2,3,21,22,4,25,29,37,32,34,38,39,40,43,44,23,24]

# s = [1,17,36,31,42,5,41,28,27,18,26,45,2,22,40,25,39,29,32,43,4,44,37,38,34,35,30,3,6,8,9,10,11,12,13,14,15,16,20,19,7,21,33,23,24]
# s = [17,1,36,31,41,42,5,2,22,25,32,40,4,28,29,43,18,44,27,21,26,37,34,38,39,35,30,6,3,8,9,19,10,11,33,12,13,14,7,15,16,20,45,23,24]
# s = [45,1,36,31,17,5,42,41,28,27,26,6,20,9,11,7,12,30,14,19,18,2,4,8,10,13,15,16,22,21,25,29,32,33,34,44,35,3,40,37,38,39,43,23,24]
# s = [36,1,31,42,27,17,5,41,28,26,6,7,20,30,8,10,13,15,9,11,12,14,19,45,33,16,18,35,2,3,21,37,22,25,40,44,29,38,32,4,34,39,43,23,24]
# s = [45,1,36,31,41,17,27,5,42,35,26,28,30,6,20,9,12,11,14,19,7,8,10,13,15,16,18,33,2,3,21,22,25,29,32,34,4,40,37,38,39,43,44,23,24]

# s =[42,20,1,36,16,6,18,17,25,8,33,31,14,34,2,11,12,19,44,43,28,9,39,21,27,5,26,41,7,30,32,4,29,35,22,3,37,15,38,40,10,13,45,24,23] 

s = [36,6,18,20,33,8,5,1,2,39,31,28,16,22,29,34,32,43,17,9,25,15,27,37,11,19,14,41,12,4,30,10,21,35,26,38,40,44,3,13,42,7,45,24,23]
# s = [36,6,18,31,42,20,33,28,45,2,41,1,17,9,11,19,12,27,14,5,21,32,25,34,26,29,7,22,4,8,10,13,38,40,44,16,35,39,30,3,37,15,43,23,24]
# s = [36,6,20,17,12,14,9,8,11,18,33,42,10,41,2,31,1,34,32,19,5,25,21,27,39,4,35,26,30,16,28,22,40,7,13,3,29,15,37,38,45,43,44,23,24]
# s = [17,1,36,6,20,18,8,14,11,33,12,15,2,5,43,28,41,27,40,19,31,9,34,16,42,21,32,4,38,39,29,26,7,37,30,25,35,3,44,22,10,45,13,23,24]

print fcao2_custo(s,mat1)
print fcao2_custo(s,mat2)
print individuos_violam_dep(s,matprec)

# print fcao2_custo([1, 36, 6, 20, 16, 41, 17, 33, 31, 12, 28, 8, 13, 19, 9, 14, 7, 15, 10, 11, 18, 2, 5, 32, 37, 42, 29, 39, 27, 40, 34, 43, 22, 4, 44, 21, 38, 26, 35, 30, 3, 45, 25, 23, 24], mat2)

# print fcao_custo([45,36,6,8,20,15,10,42,13,18,31,33,17,41,2,9,7,5,43,25,11,16,19,28,14,12,40,1,21,34,39,27,32,26,35,29,30,38,44,37,3,22,4,24,23], mat)
