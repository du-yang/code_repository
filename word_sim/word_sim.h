/*
 * word_sim.h
 * Copyright (C) 2018 app <app@VM_36_54_centos>
 *
 */

#ifndef WORD_SIM_H
#define WORD_SIM_H

#include <iostream>
#include <string>
#include <vector>
#include <map>

using namespace std;


class WordSim{
public:
    WordSim();
    //~WordSim();
    bool Init();
    double score(string word1,string word2);
    double dotProduct(vector<double>& v1,vector<double>& v2);
    double norm2(vector<double>& vec);
private:
    map<string,vector<double> > word2vec;
};

#endif /* !WORD_SIM_H */
