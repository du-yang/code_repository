/*
 * tf_model.cc
 * Copyright (C) 2018 app <app@VM_127_30_centos>
 *
 */

#include "tf_model.h"
#include <vector>
#include "tensorflow/core/public/session.h"
#include "tensorflow/core/platform/env.h"


using namespace tensorflow; 
using namespace std;


int TfPredict::vec_dim_ = 50;

TfPredict::TfPredict(){

    status = NewSession(SessionOptions(), &session_);
    if (!status.ok()) {
        std::cout << status.ToString() << endl;
    }

    GraphDef graph_def;
    status = ReadBinaryProto(Env::Default(), "./data/pinyin/pinyin_model.pb", &graph_def);
    if (!status.ok()) {
        std::cout << status.ToString() << endl;
    }

    status = session_->Create(graph_def);
    if (!status.ok()) {
        cout << status.ToString() << endl;
    }
}

TfPredict::~TfPredict(){
    session_->Close();
}

void TfPredict::Predict(const vector<int>& input_vec,vector<int>& output_vec){
    Tensor x(DT_INT32, TensorShape({1,vec_dim_}));
    auto x_map = x.tensor<int,2>();
    for (int j=0;j<vec_dim_;j++){
        x_map(0,j) = input_vec[j];
    }
    vector<std::pair<string, tensorflow::Tensor>> inputs = {
        { "x", x },
    };

    vector<tensorflow::Tensor> outputs;
    status = session_->Run(inputs, {"y"}, {}, &outputs);

    auto out = outputs[0].shaped<int,1>({vec_dim_});
    for(int i=0;i<vec_dim_;i++){
        output_vec.push_back(out(i));
    }
    //cout <<"go:"<< outputs[0].shaped<int,2>({1,50}) << "\n";
    //cout <<"go:"<< out_value << "\n";
}


