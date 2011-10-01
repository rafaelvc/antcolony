#include <vector>
#include <iostream>
#include <string>


using namespace std;

struct weight {
	int a,b;
};

class xxx {
	public: 
		xxx();
		~xxx();
		void set_a(int & x);
		int get_a();
		void get_(xxx & z);
	private: 
		int a;
};

xxx::xxx(){
	cout << "Executou Construtor";
}

xxx::~xxx(){
	cout << "Executou Destrutor";
}

void xxx::set_a(int & x) {
	a =  x;
} 

int xxx::get_a() {
	return a;
}

void xxx::get_(xxx & z) {
	cout << z.get_a();
}


int main() {

	int x = 10;
	vector<weight> a;

//	xxx b;
	xxx * c = new xxx();
	c->set_a(x);
	c->get_(*c);

	string s;
	s = "Rafael";
	s = s.substr(3);
	cout << endl << s << endl;

	vector<string> a1;
	string s1 = "a";
	string s2 = "b";
		
	a1.push_back(s1);
	a1.push_back(s2);
	string s3 = a1.at(0);
	cout << s3;



}
