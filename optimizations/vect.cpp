#include <iostream>
#include <vector>
#include <algorithm>
#include <cstdlib>
#include <cmath>
using namespace std;

struct aaa {
	vector <int> i;
	int x;
};

class test{
	public:
	test();
	void bla(vector<aaa> & b);
//	~test();
	private:
		// vector<int> * vt;
		vector<aaa>  vt;
};

void test::bla(vector<aaa> & b) {


	cout << b.size() << "-" << endl;
}

test::test() : vt() {
//	1+1;

//	vt = new vector<int> ();
//
	bla(vt);
	cout << vt.size() << "-";
}

//test::~test() {
//	delete vt;
//}

int main() {

	vector<string> v;	
	vector<int> vet;
	vet.push_back(2);
	vet.push_back(3);
	vet.push_back(4);
	vet.push_back(5);

	string s = "";
	v.push_back(s);
	string sa = "a";
	v.push_back(sa);

	if (v[1] == "a")
		cout << "muuuuaaaa";

	for (std::vector<int>::iterator it = vet.begin(); it != vet.end(); ++it)  
		std::cout << *it <<  std::endl;
	
	if ( find(vet.begin(), vet.end(), 22) == vet.end() )
		cout << "muuaaaaa22222";

	
	return 1;

//	test t;

//	srand(0);	
	for (;;) 
	cout << (rand() % 10) / 10 << endl;
	return 0;	
	// vector<int> vet;
	vector<vector<int> > vet1;
	vet.push_back(2);
	vet.push_back(3);
	vet.push_back(4);
	vet.push_back(5);

	remove(vet.begin(), vet.end(), 3);
	vet.resize(vet.size()-1);

//	vet1[0][0] = 1;
//	vet1[0][1] = 2;

	float x = 1.0;

	cout << pow (x, 2.0);

//	std::cout << vet << std::endl; It's not implemented yet.
/*
	for (std::vector<int>::iterator it = vet.begin(); it != vet.end(); it++)  {
		std::cout << *it <<  std::endl;
	}*/

	for (int i = 0; i < vet.size(); i++) 
		cout << vet[i] <<  endl;

//	vet.erase(vet.find(vet.begin(),find.end(), 4));

}
