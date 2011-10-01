/* class cpop {
	 public:
	   cpop(cmap* city_map);
           ~cpop();
         void build(int end_count);
         void rebuild(int end_count);
         void kill_off(int to_survive);
         float publish(int generation);
         void output_pub();
         private:
	 float a;
           list<ccity*> sol;
	   list<row*> table;
           cmap* m; 
};


inline bool compd(const ccity* s1, const ccity* s2) {
	  return (s1->distance < s2->distance);
}

cpop::cpop(cmap* city_map) {
	  m = city_map;
}

cpop::~cpop() {
	  for (list<ccity*>::iterator i=sol.begin(); i!=sol.end(); i++)
		      delete (*i);
}

void cpop::build(int end_count) {
	  int alive = 0;
	    while (alive < end_count) {
		        ccity* cs = new ccity(m);
			    cs->create_rand_sol();
			        sol.push_back(cs);
				    alive++;
				      }
}


void cpop::rebuild(int end_count) {
	  list<ccity*> old(sol);
	    int survivors = sol.size();
	      int to_vary = end_count - survivors;
	        list<ccity*>::iterator iter = old.begin();
		  while (to_vary) {
			      ccity* cs = new ccity(m);
			          cs->copy(*(*iter));
				      cs->create_vari_sol();
				          sol.push_back(cs);
					      iter++;
					          if (iter == old.end())
							        iter = old.begin();
						      to_vary--;
						        }
}

void cpop::kill_off(int to_survive) {
	  for (list<ccity*>::iterator i=sol.begin(); i!=sol.end(); i++)
		      (*i)->calc_distances();
	    sol.sort(compd);
	      list<ccity*>::iterator iter=sol.begin();
	        for (int t=0; t<to_survive; t++)
			    iter++;
		  int size = sol.size() - to_survive;
		    while (size) {
			        delete (*iter);
				    iter = sol.erase(iter);
				        size--;
					  }
}

float cpop::publish(int generation) {
	  while (!table.empty()) {
		      row *destroy = table.front();
		          delete destroy->solution;
			      delete destroy;
			          table.pop_front();
				    }
	    for (list<ccity*>::iterator i=sol.begin(); i!=sol.end(); i++) {
		        struct row *crow = new row;
			    crow->generation = generation;
			        crow->total_distance = (*i)->distance;
				    crow->solution = new list<int>((*i)->sol);
				        table.push_back(crow);
					  }
	      return sol.front()->distance;
}

void cpop::output_pub() {
	  ofstream file;
	    file.open("pub.out", ios::out);
	      for (list<row*>::iterator i=table.begin(); i!=table.end(); i++) {
		          file << (*i)->generation << " " << (*i)->total_distance << " ";
			      for (list<int>::iterator l=(*i)->solution->begin(); l !=(*i)->solution->end(); l++) {
				            file << (*l) << " ";
					        }
			          file << endl;
				    }
	        file.close();
} */

