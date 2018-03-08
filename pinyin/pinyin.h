/*
 * pinyin.h
 * Copyright (C) 2018 app <app@VM_127_30_centos>                   
 *
 */ 

#ifndef PINYIN_H                                                 
#define PINYIN_H 

#include <iostream>
#include <string>
#include <vector>
#include <map>
//#include "tf_model.h"


using namespace std;
//using namespace tensorflow;

class TfPredict;

class WordCorrect{
public:
    WordCorrect();
    ~WordCorrect();
    bool Init();
    void CorrectByPronounce(const string& raw_s,string& corrected_s);
private:
    void S2pinyin(const string& raw_s,vector<string>& pinyin_vec);
    void Pinyin2Id(const string& raw_s,vector<int>& id_vec);
    void SplitString(const string & raw_s,vector<string>& string_vec);
    void VectorPad(vector<int>&);
private:
    map<string,int> word2id;
    map<int,string> id2word;
    map<string,string> word2pinyin;
    map<string,int> pinyin2id;
    static size_t vec_dim;
    TfPredict* TFModel;
};

#endif /* !PINYIN_H */
