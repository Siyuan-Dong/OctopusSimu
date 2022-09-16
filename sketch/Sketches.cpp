# include "BOBHash32.h"
// # include "params.h"
# include <iostream>
# include <string.h>
# include <vector>
#include "CU_Sketch.h"
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
namespace py = pybind11;
using namespace std;
#define COUNTER_SIZE 32 
#define MAX_HASH_NUM 16

// class CU_Sketch
// {
// public:
// 	int w, d;
// 	int* counter[MAX_HASH_NUM];
// 	int COUNTER_SIZE_MAX_CNT = (1 << (COUNTER_SIZE - 1)) - 1;
// 	BOBHash32* hash[MAX_HASH_NUM];
// 	int index[MAX_HASH_NUM];    //index of each d
// 	int thres=4000;

// public:
// 	CU_Sketch()
// 	{
// 		int _w=1000, _d=3;
// 		int hash_seed = 1000;
// 		w = _w, d = _d;

// 		for (int i = 0; i < d; i++)    //allc memory
// 		{
// 			counter[i] = new int[w];
// 			memset(counter[i], 0, sizeof(int) * w);
// 		}

// 		for (int i = 0; i < d; i++)    //init d hash functions
// 		{
// 			hash[i] = new BOBHash32(i + hash_seed);
// 		}
// 	}
// 	void Clear(){
// 		for (int i = 0; i < d; i++)    //allc memory
// 		{
// 			memset(counter[i], 0, sizeof(int) * w);
// 		}
// 	}
// 	int Insert(uint32_t flow_id)
// 	{
// 		int temp = 0, min_value = COUNTER_SIZE_MAX_CNT;;
// 		for (int i = 0; i < d; i++)
// 		{
// 			index[i] = (hash[i]->run(flow_id)) % w;
// 			temp = counter[i][index[i]];
// 			min_value = temp < min_value ? temp : min_value;
// 		}

// 		// if (min_value == COUNTER_SIZE_MAX_CNT)
// 		// 	return;
// 		if (min_value > thres)
// 			return min_value;

// 		for (int i = 0; i < d; i++)
// 		{
// 			if (counter[i][index[i]] == min_value)
// 				counter[i][index[i]] ++;
// 		}
// 		return min_value+1;
// 	}

// 	int Query(uint32_t flow_id)
// 	{
// 		int temp = 0, min_value = COUNTER_SIZE_MAX_CNT;;
// 		for (int i = 0; i < d; i++)
// 		{
// 			index[i] = (hash[i]->run(flow_id)) % w;
// 			temp = counter[i][index[i]];
// 			min_value = temp < min_value ? temp : min_value;
// 		}
// 		return min_value;
// 	}
// 	bool is_big(uint32_t flow_id){
// 		return Query(flow_id)>thres;
// 	}

// 	void Delete(uint32_t flow_id)
// 	{
// 		for (int i = 0; i < d; i++)
// 		{
// 			index[i] = (hash[i]->run(flow_id)) % w;
// 			counter[i][index[i]] --;
// 		}
// 	}

// 	~CU_Sketch()
// 	{
// 		for (int i = 0; i < d; i++)
// 		{
// 			delete[]counter[i];
// 			delete hash[i];
// 		}
// 	}
// };


class Sketches{
public:
	// CU_Sketch insketch[16],outsketch[16],coresketch[20];
	int edge_key[110],cnt_key,flag[256];
	vector<int> ab_fgs;

	// CU_Sketch insketch;
	vector<CU_Sketch> insketch;
	vector<CU_Sketch> outsketch;
	vector<CU_Sketch> coresketch;
	// CU_Sketch insketch[16],outsketch[16],coresketch[20];
	// int lala[100];
	Sketches(){
		insketch.resize(16);
		outsketch.resize(16);
		coresketch.resize(20);
		// memset(edge_key,0,sizeof(edge_key));
		// memset(flag,0,sizeof(flag));
		// cnt_key=0;
		Clear();
	}
	void Clear(){
		for(int i=0;i<16;i++){
			insketch[i].Clear();
			outsketch[i].Clear();
		}
		for(int i=0;i<20;i++) coresketch[i].Clear();
		memset(edge_key,0,sizeof(edge_key));
		memset(flag,0,sizeof(flag));
		cnt_key=0;
		ab_fgs.clear();
	}
	void update_edge_key(int flow_id){
		if(!flag[flow_id]){
			flag[flow_id]=1;
			edge_key[cnt_key++]=flow_id;
		}
		// cout<<cnt_key<<" "<<edge_key[cnt_key-1]<<endl;
	}
	int SSum(vector<CU_Sketch>& cu, int flow_id){
		int res=0;
		for(int i=0;i<16;i++){
			res+=cu[i].Query(flow_id);
		}
		return res;
	}
	int subnet(int flow_id){
		// return flow_id>>2;
		return flow_id>>10;
	}
	vector<int> ab_fg(){
		bool mark[256]={};
		int cnt_ab=0;
		cout<<"*"<<cnt_key<<endl;
		for(int i=0;i<cnt_key;i++){
			int in_sum = SSum(insketch,edge_key[i]), out_sum = SSum(outsketch,edge_key[i]);
			cout<<edge_key[i]<<" "<<in_sum<<" "<<out_sum<<endl;
			if(in_sum-out_sum>2){
				if(!mark[subnet(edge_key[i])]){
					mark[subnet(edge_key[i])]=1;
					cnt_ab++;
					ab_fgs.push_back(subnet(edge_key[i]));
				}
			}
		}
		// ab_fgs = new int[cnt_ab];
		// int tmp=0;
		// for(int i=0;i<256;i++){
		// 	if(mark[i]){
		// 		ab_fgs[tmp++]=i;
		// 	}
		// }
		return ab_fgs;
	}
	~Sketches(){
		
	}
};

PYBIND11_MODULE(Sketches, m) {
	py::class_<Sketches> sketches(m, "Sketches");
	
    
    sketches.def(py::init<>())
        .def("Clear", &Sketches::Clear)
        .def("update_edge_key", &Sketches::update_edge_key)
        .def("ab_fg", &Sketches::ab_fg)
		.def_readwrite("insketch", &Sketches::insketch)
		.def_readwrite("outsketch", &Sketches::outsketch)
		.def_readwrite("coresketch", &Sketches::coresketch);

	py::class_<CU_Sketch>(sketches, "CU_Sketch")
        .def(py::init<>())
        .def("Insert", &CU_Sketch::Insert)
        .def("Delete", &CU_Sketch::Delete)
        .def("Query", &CU_Sketch::Query);
}


// PYBIND11_MODULE(CU_Sketch, m) {
//     py::class_<CU_Sketch>(m, "CU_Sketch")
//         .def(py::init<int,int>())
//         .def("Insert", &CU_Sketch::Insert)
//         .def("Delete", &CU_Sketch::Delete)
//         .def("Query", &CU_Sketch::Query);
// }