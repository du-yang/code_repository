/*
 * main.cc
 * Copyright (C) 2018 app <app@VM_127_30_centos>
 *
 */

#include "pinyin.h"
#include <iostream>
#include <string>
#include "tf_model.h"
//#include "tensorflow/core/public/session.h"
//#include "tensorflow/core/platform/env.h"

using namespace std;
//using namespace tensorflow;

int main(int argc, char *argv[]){
    WordCorrect pinyiner;

    string corrected_sent;
    string test("我在haHAH");
    pinyiner.CorrectByPronounce(test,corrected_sent);
    cout<<"原始语句为："<<test<<endl;
    cout<<"纠正语句为："<<corrected_sent<<endl;
    return 0;
}
