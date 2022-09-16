#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <vector>
#include <unordered_map>
namespace py = pybind11;
using namespace std;
class example{
public:
    // int a;
    vector<int> a;
    unordered_map<int,int> ma;
    example(){
        ma[1]=1;
    }
    // int a[100];
};

PYBIND11_MODULE(example, m) {
    py::class_<example>(m, "example")
        .def(py::init<>())
        .def_readwrite("a", &example::a)
        .def_readwrite("ma", &example::ma);
}