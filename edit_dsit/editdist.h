/*
 * editdist.h
 * Copyright (C) 2018 app <app@VM_36_54_centos>
 *
 */

#ifndef EDITDIST_H
#define EDITDIST_H

#include <iostream>


using namespace std;

class Distance{
public:
    int EditDist(const vector<string>& v1, const vector<string>& v2);
};


#endif /* !EDITDIST_H */
