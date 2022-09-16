# include <iostream>
# include <string.h>
# include <vector>
#include "../elastic-coco-dleft/elastic/ElasticSketch.h"
#include "../elastic-coco-dleft/dleft/dleft.h"

using namespace std;
vector<TUPLES> ab_fs;
int main(){
    TUPLES item(234,212,345,43,2);
    ab_fs.push_back(item);
    cout<<ab_fs[0].srcIP()<<endl;
    item.clear();
    cout<<ab_fs[0].srcIP()<<endl;
    cout<<item.srcIP()<<endl;

    return 0;
}
