#include "aco.hpp"
#include <list> 
#include <fstream> 
#include <string>
#include <algorithm> 
#include <cstdlib>
#include <cmath>

using namespace std;

aco::aco(const string system)
	: pareto(), matprec(), mat2(), matfer1(), matfer2()
{

	nr_formigas = 40;
	alfa = 1.0;
	beta = 1.0; 
	maxit = 80;
//	txevaporacao = 0.1;
	txevaporacao = 0.05;
	t0 = 1.0;
	tmin = 0.00001;
//	q0 = 0.4;
 	q0 = 0.75;

	best_1.c1 = best_1.c2 = best_2.c1 = best_2.c2 = 0; 
	sbest_1.c1 = sbest_1.c2 = sbest_2.c1 = sbest_2.c2 = 0; 

	string file = system;
	file.append("_attribute_mat.txt");
	read_mat( file.c_str(), mat1);

	file = system;
	file.append("_method_mat.txt");
	read_mat( file.c_str(), mat2);

	file = system;
	file.append("_precedent_mat.txt"); 
	read_mat( file.c_str(), matprec); 

	// Initialize pheromone matrix;
	tam_solucao = mat1.size();
	for (int i=0; i < tam_solucao; i++) {
		vector<float> v;
		for (int j=0; j < tam_solucao; j++) 
			v.push_back(t0);
		matfer1.push_back(v);
		matfer2.push_back(v);
	}
}

aco::~aco(){}

void aco::paco() {

	vector <int> cl = classes_iniciais();
	vector <int> solucao,restantes,s1, s2;
	int proxima, classe, r;

	for (int it=0; it < maxit; it++ )  {

		best_1.c1 = best_1.c2 = best_2.c1 = best_2.c2 = 0; 
		sbest_1.c1 = sbest_1.c2 = sbest_2.c1 = sbest_2.c2 = 0; 

		float q = (rand() % 10) / 10.0;
		float w = (rand() % 10) / 10.0;
		for (int f=1; it <= nr_formigas; it++ )  {
			
			classe = cl[ rand() % cl.size() ];
			solucao.push_back(classe);
			for (int i = 1; i <= tam_solucao ; i ++) {
				if (i != classe)
					restantes.push_back(i);
			}	
			r = tam_solucao - 1; 
			while (r > 0) {
				proxima = proxima_classe_(classe, solucao, restantes, w, q);
				solucao.push_back(proxima);
				remove(restantes.begin(), restantes.end(), proxima);
				restantes.resize(--r);
				// Local Pheromone Update - Ant crosses i,j edge  
				// matfer1[classe-1][proxima-1] = (1.0 - txevaporacao)*(matfer1[classe-1][proxima-1]) + (txevaporacao * t0);
				// matfer2[classe-1][proxima-1] = (1.0 - txevaporacao)*(matfer2[classe-1][proxima-1]) + (txevaporacao * t0);
				if (matfer1[classe-1][proxima-1] < tmin)
					matfer1[classe-1][proxima-1] = tmin;
				if (matfer2[classe-1][proxima-1] < tmin)
					matfer2[classe-1][proxima-1] = tmin;
				classe = proxima;
			}

			// Local Pheromone Update - Ant crosses i,j edge  
			for (int i = 0; i < tam_solucao - 1; i++) { 
				matfer1[i][i+1] = (1.0 - txevaporacao)*(matfer1[i][i+1]) + (txevaporacao * tmin);
				matfer2[i][i+1] = (1.0 - txevaporacao)*(matfer2[i][i+1]) + (txevaporacao * tmin);
			}


			/* for (int j = 0; j < tam_solucao; j++) 
				cout << solucao[j] << ",";
			cout << endl;*/

			// Local Search  - one local search a objective
			int c1 = fcusto(solucao,mat1);
			int c2 = fcusto(solucao,mat2);
			hill_climbing ( s1, solucao, c1, 1, mat1 );
			hill_climbing ( s2, solucao, c2, 1, mat2 );

			// Gloal Pheromone Update
			//// Evaporaton of pheromone tracks
			for (int i = 0; i < tam_solucao; i++) {
				for (int j = 0; j < tam_solucao; j++) {
					 matfer1[i][j] *= (1.0 - txevaporacao);
					 matfer2[i][j] *= (1.0 - txevaporacao);
					 if (matfer1[i][j] < tmin)
						matfer1[i][j] = tmin;
					 if (matfer2[i][j] < tmin)
						matfer2[i][j] = tmin;

				}
			}
			//// Update pheromone matrix 1 
			if (!update_best1(solucao, c1, c2)) 
				update_second_best1(solucao, c1, c2);
			if (it > 0) {
			for (int i = 0; i<tam_solucao-1; i++) {
				for (int j = 0; j<tam_solucao-1; j++) {
					if (best_1.s[j] == s1[i] && best_1.s[j+1] == s1[i+1])
			 			matfer1[s1[i]-1][s1[i+1]-1] += (10.0 * txevaporacao); 
					if (sbest_1.s[j] == s1[i] && sbest_1.s[j+1] == s1[i+1])
				 		matfer1[s1[i]-1][s1[i+1]-1] += (5.0 * txevaporacao); 
				}
			}
			}
			//// Update pheromone matrix 2
			if (!update_best2(solucao, c1, c2)) 
				update_second_best2(solucao, c1, c2);
			if (it > 0) {
			for (int i = 0; i<tam_solucao-1; i++) {
				for (int j = 0; j<tam_solucao-1; j++) {
					if (best_2.s[j] == s2[i] && best_2.s[j+1] == s2[i+1])
			 			matfer2[s2[i]-1][s2[i+1]-1] += (10.0 * txevaporacao); 
					if (sbest_2.s[j] == s2[i] && sbest_2.s[j+1] == s2[i+1])
			 			matfer2[s2[i]-1][s2[i+1]-1] += (5.0 * txevaporacao); 
				}
			}
			}

			c1 = fcusto(s1,mat1);
			c2 = fcusto(s1,mat2);
			pareto_add(s1, c1, c2);
			c1 = fcusto(s2,mat1);
			c2 = fcusto(s2,mat2);
			pareto_add(s2, c1, c2);

			solucao.resize(0);
		}
		cout << it << endl;	
	}

	for (int i = 0; i < pareto.size(); i++) {
		cout << fcusto(pareto[i].s, mat1)  << " - " << fcusto(pareto[i].s,mat2) << endl;
		for (int j = 0; j < pareto[i].s.size(); j++) {
			 cout << pareto[i].s[j] << ",";
		}
		cout << endl;

	}
		


}

bool aco::update_best1(vector<int> & solucao, int custo1, int custo2)  {	
	if (custo1 < best_1.c1 || best_1.c1 == 0) {	
		if (best_1.c1 > 0) {
			sbest_1.c1 = best_1.c1;
			sbest_1.c2 = best_1.c2;
			sbest_1.s = best_1.s;
		}
		else {
			sbest_1.c1 = custo1;
			sbest_1.c2 = custo2;
			sbest_1.s = solucao;
		}	
		best_1.c1 = custo1;
		best_1.c2 = custo2;
		best_1.s = solucao;
		return true;
	}
	return false;
}
	
bool aco::update_second_best1(vector<int> & solucao, int custo1, int custo2) 
{
	if (custo1 < sbest_1.c1) {	
		sbest_1.c1 = custo1;
		sbest_1.c2 = custo2;
		sbest_1.s = solucao;
		return true;
	}
	return false;
}

bool aco::update_best2(vector<int> & solucao, int custo1, int custo2) 
{	
	if (custo2 < best_2.c2 || best_2.c2 == 0) {	
		if (best_2.c2 > 0) {
			sbest_2.c1 = best_2.c1;
			sbest_2.c2 = best_2.c2;
			sbest_2.s = best_2.s;
		}
		else {
			sbest_2.c1 = custo1;
			sbest_2.c2 = custo2;
			sbest_2.s = solucao;
		}
		best_2.c1 = custo1;
		best_2.c2 = custo2;
		best_2.s = solucao;
		return true;
	}
	return false;
}
	
bool aco::update_second_best2(vector<int> & solucao, int custo1, int custo2) {
	if (custo2 < sbest_2.c2) {	
		sbest_2.c1 = custo1;
		sbest_2.c2 = custo2;
		sbest_2.s = solucao;
		return true;
	}
	return false;
}

bool aco::pareto_add(vector<int> & solucao, int custo1, int custo2) 
{
	vector<int> r;
	int c1,c2,i;

/*	for (i = 0; i < pareto.size(); i++) 
	{
		c1 = pareto[i].c1;
		c2 = pareto[i].c2;
		// solucao dominante, remove dominada
		if ((custo1 <= c1 && custo2 < c2) || (custo1 < c1 && custo2 == c2)) 
			r.push_back(i);
		// solucao dominada ou igual - sem change
		else if (custo1 >= c1 && custo2 >= c2)
			return false;
	}
	
	for (i = 0; i < r.size(); i++) 
		// dequeue and list have efficienty ways to remove than this 
		pareto.erase(pareto.begin()+r[i]); 
//		remove(pareto.begin(), pareto.end(), pareto[r[i]]); // optimize
//	if (i)
//		pareto.resize(pareto.size()-i); */

	pareto_s p;
	p.s = solucao;
	p.c1 = custo1;
	p.c2 = custo2;	
	pareto.push_back(p);
	return true;
}

int aco::proxima_classe_(int classe, vector<int> & solucao, vector<int> & restantes, float w, float q)
{
	vector<int> candidatas;
	bool restricao;

	for(int i =0; i < restantes.size(); i++) 
	{
		if ( matprec[ restantes[i]-1 ] != "" ) {
	
			restricao = false;
			vector<string> dep = splitter(matprec[restantes[i]-1],",");
			for (int j = 0; j < dep.size(); j++) {
				if (find(solucao.begin(), solucao.end(), atoi(dep[j].c_str())) == solucao.end()) 	
				{
					restricao = true;
					break;
				}
			}
			if (!restricao)
				candidatas.push_back( restantes[i] );
		}
		else
			candidatas.push_back( restantes[i] );
	}
	float fer1 = 0.0, fer2 = 0.0;
	for (int i = 0; i < candidatas.size(); i++) {
                fer1 += matfer1[classe-1][candidatas[i]-1];
                fer2 += matfer2[classe-1][candidatas[i]-1];
	}

	vector<float> prob_candidatas;
	float soma_pij=0.0, maxarg=0.0, arg;
	int escolhido, custo1 = 0, custo2 = 0;

	int c1 = fcusto(solucao, mat1);
	int c2 = fcusto(solucao, mat2);
	
	for (int i = 0; i < candidatas.size(); i++) {

		if (mat1[candidatas[i]-1] != "") {
			vector<int> s = solucao;
			s.push_back(candidatas[i]);
			custo1 = fcusto(s, mat1);
		}
		else 
			custo1 = 1.0; // custo1 = c1;

		if (mat2[candidatas[i]-1] != "") {
			vector<int> s = solucao;
			s.push_back(candidatas[i]);
			custo2 = fcusto(s, mat2);
		}
		else
			custo2 = 1.0; // custo2 = c2;
		
	       	arg = w * (pow(fer1 , alfa ) * pow((1.0 / (custo1 == 0 ? 1 : custo1) ), beta)) + (1.0-w) * (pow(fer2,  alfa) * pow((1.0 / (custo2 == 0 ? 1 : custo2) ), beta));
		soma_pij += arg;
		prob_candidatas.push_back(arg);
		if (arg > maxarg) {
			escolhido = candidatas[i];
			maxarg = arg;
		}
	}

	if (q <= q0)
		return escolhido;

	float r;
	for (int i = 0; i < prob_candidatas.size(); i++) 
		prob_candidatas[i] = prob_candidatas[i] / soma_pij;

	while (true){
		for (int i = 0; i < prob_candidatas.size(); i++) {
			r = rand() % 10000 / 10000.0;
			if (r <= prob_candidatas[i])
				return candidatas[i];
		}
	}	

}


vector<int> aco::classes_iniciais() 
{
	vector<int> iniciais;
	for (int i = 0; i < matprec.size(); i++) {
		if (matprec[i] == "")
			iniciais.push_back(i+1);
	}
	return iniciais;
}


static void print_mat(vector <string> & mat) 
{
	vector<string>::iterator it; 
	cout << "[";
	for (it = mat.begin();it != mat.end();++it)
		cout << "\"" << *it << "\"";
	cout << "]" << endl ;
}	


vector<string> aco::splitter(string & str_, const char * split) {
	int pos;
	vector<string> vet_a;
	string str = str_;
	while ( (pos = str.find_first_of(split)) != -1) {
		vet_a.push_back(str.substr(0,pos));
		str = str.substr(pos+1);
	}
	vet_a.push_back(str);
	return vet_a;
}

vector<int> aco::op_troca_simples(vector<int> & s) {

	int r,r1,r2;
	vector<int> viz = s;
	bool viola_res;
	while(viola_res) {
		r1 = rand() % tam_solucao;  
		r2 = rand() % tam_solucao; 
		viola_res = false;
		if (r1 != r2) { 
			if(r2 < r1) {
				r = r1;
				r1 = r2;
				r2 = r;
			}
		
			for (vector<int>::iterator it_s = s.begin()+(r1+1); it_s != s.begin()+(r2+1); ++it_s) { 
				if (matprec[*it_s-1] != "") { 
					vector<string> dep = splitter(matprec[*it_s-1],","); 
					for (vector<string>::iterator it_dep = dep.begin(); it_dep != dep.end(); ++it_dep) {
						if (s[r1] == atoi((*it_dep).c_str())) {
							viola_res = true;
							break;

						}
					}
				}
			}
			if (!viola_res) {
				if (matprec[s[r2]-1] != "") {
					vector<string> dep = splitter(matprec[s[r2]-1],","); 
					for (vector<int>::iterator it_s = s.begin()+r1; it_s != s.begin()+r2; ++it_s) { 
						for (vector<string>::iterator it_dep = dep.begin(); it_dep != dep.end(); ++it_dep) { 
							if (atoi((*it_dep).c_str()) == *it_s) {
								viola_res = true;
								break;
							}
						}
					}
				}
			}

		}
		else
			viola_res = true;
//		cout << r1 << "-" << r2 << endl;

	}
	int v = viz[r1];
	viz[r1] = viz[r2];
	viz[r2] = v;
	return viz;
}

vector<vector<int> > aco::vizinhanca_solucao(vector<int> & s, int nr_vizinhos) {
	int nr_iter = 100;
	vector<int> viz;
	vector<vector<int> > vizinhanca;
	while (nr_vizinhos > 0) {
		int iter = 0;
		// 2-opt operator
		viz = op_troca_simples(s);
		viz = op_troca_simples(viz); 
		vector<int> v = viz ;
		vizinhanca.push_back(v); 

		/* while(iter < nr_iter) {
			// 2-opt operator
			viz = op_troca_simples(s);
			viz = op_troca_simples(viz); 
			// disallow equal neigboors
			// optimize - save changes done in a list and just allow changes which are not in that list.
			if (find(vizinhanca.begin(), vizinhanca.end(), viz) == vizinhanca.end()) {
				vector<int> v = viz ;
				vizinhanca.push_back(v);
			}
			else 
				iter++;
		} */
		nr_vizinhos--;
	}
	return vizinhanca;
}

void aco::hill_climbing(vector<int> & s, vector<int> & solucao, int custo, int escolha_viz, vector< string > &  mat) {
	
	int iter = 0, nr_iter = 10, nr_vizinhos = 20, c = 0;
	bool melhora;
	s = solucao;
	while( iter < nr_iter)
	{
	       	melhora = false;
		vector<vector<int> > vizinhanca = vizinhanca_solucao( s, nr_vizinhos );
//		cout << vizinhanca.size() << endl;
		for ( vector<vector<int> >::iterator it_viz = vizinhanca.begin(); it_viz != vizinhanca.end(); ++it_viz ) {
			c = fcusto(*it_viz, mat);
			if (c < custo) {
				custo = c;
				s = *it_viz;
				melhora = true;
				iter = 0;
				if (escolha_viz)
					break;
			}
		}
		if (!melhora)
			iter++;
	}
	//return solucao;
}


void aco::read_mat(const char * nm_file, vector< string > &  mat) {
	char line[1024];
	fstream f; 
	f.open(nm_file);
	string s;
	while(true){
		f.getline(line, 1024);
		s = line;
		if (!f.eof())
			mat.push_back(s);
		else
			break;
	}
	f.close();
} 


int  aco::fcusto(vector<int> & solucao, vector<string> & mat){ 
	int custo = 0;	
	for ( vector<int>::iterator c = solucao.begin(); 
	      c != solucao.end(); ++c ) {
		if (mat[*c-1].length() > 0) {
			vector<string> v_rest = splitter(mat[*c-1], ",");
			vector<int>::iterator its_end = find(solucao.begin(), solucao.end(), *c); // encontra classe no vetor solucao
			for ( vector<string>::iterator v_rest_it = v_rest.begin(); 
					v_rest_it != v_rest.end(); ++v_rest_it ) {
				vector<string>  e = splitter(*v_rest_it, "-");
      				int dep = atoi(e[0].c_str()); 
				if (find(solucao.begin(), its_end, dep) == its_end) // procura dependencia na frente da classe 
					custo += atoi(e[1].c_str()); //  dependencia nao esta na frente entao acrescenta no custo
			}
		}
	}
	return custo;
}

void  aco::u_test_fcusto() {

	vector<int> solucao, solucao1, solucao2,  solucao3;
	// int vet[] = {20, 21, 7, 6, 16, 2, 17, 1, 3, 4, 5, 8, 9, 18, 19, 11, 10, 13, 14, 12, 15}; //System A
	int vet[] = {45, 36, 17, 1, 6, 8, 31, 10, 12, 13, 15, 9, 20, 14, 19, 11, 16, 18, 5, 42, 28,33, 2, 27, 39, 34, 32, 4, 21, 25, 44, 26, 38, 43, 41, 35, 30, 7, 29, 3, 40, 37, 22, 24, 23};

	int vet1[]= {17, 36, 6, 16, 8, 14, 11, 13, 9, 15, 45, 10, 1, 20, 12, 19, 7, 18, 42, 33, 31,28, 2, 27, 29, 38, 21, 5, 41, 44, 39, 34, 26, 32, 40, 4, 22, 25, 35, 43, 37, 30, 3, 24, 23};

	int vet2[]= {36, 6, 17, 12, 16, 14, 11, 20, 9, 8, 13, 10, 19, 15, 18, 33, 2, 34, 5, 37, 39, 1, 42, 43, 27, 31, 32, 4, 25, 41, 38, 40, 21, 7, 26, 35, 22, 28, 44, 29, 30, 3, 45, 23, 24};

	int vet3[]={42,20,1,36,16,6,18,17,25,8,33,31,14,34,2,11,12,19,44,43,28,9,39,21,27,5,26,41,7,30,32,4,29,35,22,3,37,15,38,40,10,13,45,24,23};

	for(int i=0; i < 45; i++) {
		solucao.push_back(vet[i]);
		solucao1.push_back(vet1[i]);
		solucao2.push_back(vet2[i]);
		solucao3.push_back(vet3[i]);
	}
	cout << fcusto(solucao1, mat1) << endl;
	cout << fcusto(solucao1, mat2) << endl;
	cout << fcusto(solucao, mat1) << endl;
	cout << fcusto(solucao, mat2) << endl;
	cout << fcusto(solucao2, mat1) << endl;
	cout << fcusto(solucao2, mat2) << endl;
	cout << fcusto(solucao3, mat1) << endl;
	cout << fcusto(solucao3, mat2) << endl;

}

int main() {
	aco a("D");
	a.paco();
//	a.u_test_fcusto();
}

/*
template <class TYPE>
class debug {
	public:
		debug();
		~debug();
		static void print_mat(vector <TYPE> & mat) {
			for (vector<TYPE>::iterator it = mat.begin();it != mat.end();++it)
				cout << *it;
		}
};*/ 

/*
template <class T>
static void print_mat(vector <T> & mat) 
{
	vector<T> t;
	// vector<T>::iterator it; 

//	for (it = mat.begin();it != mat.end();++it)
//		cout << *it; 
}*/ 


/* RAND<<
 *
 * for(;;) {
		float a =  rand()/ ((1.0) * RAND_MAX); 
		printf("%f", a * 100);
		cout << a << endl;
	} */ 

/* 
 *
 *			//// Update pheromone matrix 1 
			if (update_best1(solucao, c1, c2)) {
				for (int i = 0; i<solucao.size(); i+=2) 
					 matfer1[solucao[i]-1][solucao[i+1]-1] += (10.0 * txevaporacao); 
			}
			else if (update_second_best1(solucao, c1, c2)) {
				for (int i = 0; i<solucao.size(); i+=2) 
					 matfer1[solucao[i]-1][solucao[i+1]-1] += (5.0 * txevaporacao); 
			}
			else { 
				for (int i = 0; i<solucao.size(); i+=2) {
					for (int j = 0; j<solucao.size(); j+=2) {
						if (best_1.s[j] == solucao[i] && best_1.s[j+1] == solucao[i+1])
				 			matfer1[solucao[i]-1][solucao[i+1]-1] += (10.0 * txevaporacao); 
						if (sbest_1.s[j] == solucao[i] && sbest_1.s[j+1] == solucao[i+1])
				 			matfer1[solucao[i]-1][solucao[i+1]-1] += (5.0 * txevaporacao); 
					}

				}
			}
			//// Update pheromone matrix 2
			if (update_best2(solucao, c1, c2)) {
				for (int i = 0; i<solucao.size(); i+=2) 
					 matfer2[solucao[i]-1][solucao[i+1]-1] += (10.0 * txevaporacao); 
			}
			else if (update_second_best2(solucao, c1, c2)) {
				for (int i = 0; i<solucao.size(); i+=2) 
					 matfer2[solucao[i]-1][solucao[i+1]-1] += (5.0 * txevaporacao); 
			}
			else { 
				for (int i = 0; i<solucao.size(); i+=2) {
					for (int j = 0; j<solucao.size(); j+=2) {
						if (best_2.s[j] == solucao[i] && best_2.s[j+1] == solucao[i+1])
				 			matfer2[solucao[i]-1][solucao[i+1]-1] += (10.0 * txevaporacao); 
						if (sbest_2.s[j] == solucao[i] && sbest_2.s[j+1] == solucao[i+1])
				 			matfer2[solucao[i]-1][solucao[i+1]-1] += (5.0 * txevaporacao); 
					}

				}
			} */

