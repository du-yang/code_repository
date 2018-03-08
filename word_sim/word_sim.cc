/*
 * word_sim.cc
 * Copyright (C) 2018 app <app@VM_36_54_centos>
 *
 */

#include "word_sim.h"

#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include <fstream>
#include <map>
#include <math.h>

using namespace std;


WordSim::WordSim(){
    if(Init()){
        cout<<"初始化完成"<<endl;
    }else{
        cout<<"初始化未完成"<<endl;
    };
}

bool WordSim::Init(){
    ifstream in("./data/word2vec.txt");
    if(!in.is_open()){
        cout<<"open file error"<<endl;
        return false;
    }
    
    string key_word;
    double tmp_float;
    string tmp_line;
    vector<double> tmp_vec;
    stringstream s_stream;
    while(!in.eof()){
        getline(in,tmp_line);
        s_stream.str(tmp_line);
        if(s_stream>>key_word){
            while(s_stream>>tmp_float){
                tmp_vec.push_back(tmp_float);
            }
            if(tmp_vec.size()==100){
                word2vec[key_word] = tmp_vec;
            }
        }
        //cout<<"key word"<<key_word<<"vec:"<<tmp_vec[0]<<' '<<tmp_vec[1]<<endl;
        tmp_vec.clear();
        s_stream.clear();
    }
    in.close();
    return true;
}

double WordSim::dotProduct(vector<double>& v1,vector<double>& v2){
    double result = 0;
    size_t len = v1.size();
    for(size_t i=0;i<len;i++){
        result=result+v1[i]*v2[i];
    }
    return result;
}

double WordSim::norm2(vector<double>& vec){
    double dotp = dotProduct(vec,vec);
    return sqrt(dotp);
}

double WordSim::score(string word1,string word2){
    //cout<<"input word:"<<word1<<" and "<<word2<<endl;
    vector<double> v1,v2;
    map<string,vector<double> >::iterator k;
    k = word2vec.find(word1);
    if(k!=word2vec.end()){
        v1 = k->second;
    }else{
        return 0;
    }

    k = word2vec.find(word2);
    if(k!=word2vec.end()){
        v2 = k->second;
    }else{
        return 0;
    } 

    return dotProduct(v1, v2) / (norm2(v1) * norm2(v2));
}
