/*
 * main_test.cc
 * Copyright (C) 2018 app <app@VM_36_54_centos>
 *
 */

#include <iostream>
#include <vector>
#include "word_sim.h"

using namespace std;


int main(){
    string w1="我";
    string w2="是";
    WordSim ws;
    cout<<ws.score(w1,w2)<<endl;
}

