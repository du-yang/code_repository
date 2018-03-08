#include <vector>
#include <iostream>
#include "editdist.h"


int main(void)
{
    vector<string> v1,v2;
    v1.push_back("我");
    v1.push_back("shs");
    v2.push_back("我");
    v2.push_back("ia");
    v2.push_back("23");
    v2.push_back("我");
    //string str1 = "sailn";
    //string str2 = "failing";
    Distance dist;
    int r = dist.EditDist(v1, v2);
    cout << "the dis is : " << r << endl;

    return 0;
}
