/*
 * tf_model.h
 * Copyright (C) 2018 app <app@VM_127_30_centos>
 *
 */

#ifndef TF_MODEL_H
#define TF_MODEL_H

#include "tensorflow/core/public/session.h"
#include "tensorflow/core/platform/env.h" 
#include <vector>

using namespace tensorflow;
using namespace std;

class TfPredict{
    public:
        TfPredict();
        ~TfPredict();
        void Predict(const vector<int>&,vector<int>&);
    private:
        Session* session_;
        Status status;
        static int vec_dim_;
}; 

#endif /* !TF_MODEL_H */
