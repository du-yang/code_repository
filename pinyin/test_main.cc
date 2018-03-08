/*
 * test_main.cc
 * Copyright (C) 2018 app <app@VM_127_30_centos>
 *
 */

#include "tf_model.h"
#include <iostream>
#include <vector>

using namespace std;
using namespace tensorflow;


int main(){
    TfPredict TT;
    vector<int> v1;
    for(int i=0;i<54;i++){
        v1.push_back(i);
    }
    vector<int> v2;
    TT.Predict(v1,v2);
    cout<<"v2_size:"<<v2.size()<<endl;
    for(int i=0;i<v2.size();i++){
        cout<<i<<"_st:"<<v2[i]<<endl;
    }
}
