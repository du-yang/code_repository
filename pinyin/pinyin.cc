/*
 * pinyin.cc
 * Copyright (C) 2018 app <app@VM_127_30_centos>
 *
 */

#include <iostream>
#include <vector>
#include <map>
#include <cstdlib>
#include <fstream>
#include <sstream>
#include "pinyin.h"
#include "tf_model.h"
//#include "tensorflow/core/public/session.h"
//#include "tensorflow/core/platform/env.h" 


using namespace std;
//using namespace tensorflow;



size_t WordCorrect::vec_dim = 50;

WordCorrect::WordCorrect() {
    Init();
    TFModel = new TfPredict();
}

WordCorrect::~WordCorrect() {
    delete TFModel;
}

void WordCorrect::SplitString(const string& raw_s,vector <string>& string_vec){
    int num = raw_s.size();
    int i = 0;
    while(i < num){
        int size = 1;
        if(raw_s[i] & 0x80){
            char temp = raw_s[i];
            temp <<= 1;
            do{
                temp <<= 1;
                ++size;
            }while(temp & 0x80);
        }
        string subWord;
        subWord = raw_s.substr(i, size);
        string_vec.push_back(subWord);
        i += size;
    }
}


bool WordCorrect::Init(){
    
    ifstream in("./data/pinyin/pinyin.txt");
    if(!in.is_open()){
        cout<<"open file error"<<endl;
        return false;
    }

    string tmp_word;
    string tmp_line;
    vector<string> tmp_vec;
    stringstream s_stream;
    while(!in.eof()){
        getline(in,tmp_line);
        cout<<"line:"<<tmp_line<<endl;
        s_stream.str(tmp_line);
        while(s_stream>>tmp_word){
            tmp_vec.push_back(tmp_word);
        }
        if(tmp_vec.size()==4){
            id2word.insert(pair<int,string>(stoi(tmp_vec[1].c_str()),tmp_vec[0]));
            word2pinyin.insert(pair<string,string>(tmp_vec[0],tmp_vec[2]));
            pinyin2id.insert(pair<string,int>(tmp_vec[2],stoi(tmp_vec[3].c_str())));
        }
        tmp_vec.clear();
        s_stream.clear();
        
    }
    in.close();
    return true;
}

void WordCorrect::S2pinyin(const string& raw_s,vector<string>& pinyin_vec){
    vector<string> string_vec;
    SplitString(raw_s,string_vec);
    
    map<string,string>::iterator it;
    string tmp_pinyin;
    for(size_t i=0;i<string_vec.size();i++){
        it = word2pinyin.find(string_vec[i]);
        if(it!=word2pinyin.end()){
            pinyin_vec.push_back(it->second);
        }
        else{
            pinyin_vec.push_back("xxx");
        }
       //try{
       //    tmp_pinyin = word2pinyin.at(string_vec[i]);
       //    pinyin_vec.push_back(tmp_pinyin);
       //}catch(...){
       //    cout<<string_vec[i]<<" not in word2pinyin"<<endl;
       //    pinyin_vec.push_back("xxx");
       //}
   }
}

void WordCorrect::Pinyin2Id(const string& raw_s,vector<int>& id_vec){
    vector<string> pinyin_vec;
    S2pinyin(raw_s,pinyin_vec);

    map<string,int>::iterator it;
    for(size_t i=0;i<pinyin_vec.size();i++){
        it = pinyin2id.find(pinyin_vec[i]);
        if(it!=pinyin2id.end()){
            id_vec.push_back(it->second);
        }
        else{
            id_vec.push_back(0);
        }
        //try{
        //    tmp = pinyin2id.at(pinyin_vec[i]);
        //    id_vec.push_back(tmp);
        //}catch(int){
        //    cout<<pinyin_vec[i]<<" not in pingyin2id"<<endl;
        //    id_vec.push_back(0);
        //}
    }
}

void WordCorrect::VectorPad(vector<int>& vec){
    size_t vec_num = vec.size();
    size_t tmp;
    if(vec_num<vec_dim){
        tmp = vec_dim-vec_num;
        for(size_t i=1;i<=tmp;i++){
            vec.push_back(0);
        }
    }else{
        vec.erase(vec.begin()+vec_dim,vec.begin()+vec_num); 
    }
}

void WordCorrect::CorrectByPronounce(const string& raw_s,string& corrected_s){
    vector<int> pin_id_vec;
    Pinyin2Id(raw_s,pin_id_vec);
    VectorPad(pin_id_vec);
    cout<<"id_vec:"<<pin_id_vec.size()<<endl;
    for(auto i:pin_id_vec){
        cout<<"---"<<i<<"---"<<endl;
    }

    vector<int> word_id_vec; 
    //word_id_vec.push_back(34);
    TFModel->Predict(pin_id_vec,word_id_vec);

    for(auto i:word_id_vec){
        cout<<"---"<<i<<"---"<<endl;
    }
    
    corrected_s += "test begin ---";
    for(size_t i=0;i<word_id_vec.size();i++){
        corrected_s += id2word[word_id_vec[i]];
    }
    corrected_s += "---test end";
    //for(auto x: id_vec){
    //    cout<<"id_vec:"<<x<<endl;
    //}
    //cout<<"vec_dim:"<<vec_dim<<endl;
}
