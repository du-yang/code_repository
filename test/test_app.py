# -*- coding: utf-8 -*-
import requests
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--filepath", default="./test.txt")
arg = parser.parse_args()


class test_acc_roc():
    def __init__(self):
        with open(arg.filepath) as f:
            self.test_data = [line.strip().split('\t') for line in f]

        self.base_count = len(self.test_data)

    def getAnswerTest(self):
        correct_num = 0
        wrong_num = 0
        for entity_label, relation_label, query in self.test_data:
            URL = 'http://192.168.28.129:5000/getAnswerTest/{}'.format(query)
            # print(URL)
            pre_result = json.loads(requests.get(URL).text)
            # print(pre_result)
            if pre_result:
                entity_pre, relation_pre = pre_result
                if entity_pre == entity_label and relation_pre == relation_label:
                    correct_num += 1
                else:
                    wrong_num += 1
        print('系统整体 准确率为：{}，召回率为：{}'.format(float(correct_num / self.base_count),
                                            (float(wrong_num + correct_num) / self.base_count)))

    def getAnswerBySimTest(self):
        correct_num = 0
        wrong_num = 0
        for entity_label, relation_label, query in self.test_data:
            URL = 'http://192.168.28.129:5000/getAnswerBySimTest/{}'.format(query)
            # print(URL)
            pre_result = json.loads(requests.get(URL).text)
            # print(pre_result)
            if pre_result:
                entity_pre, relation_pre = pre_result
                if entity_pre == entity_label and relation_pre == relation_label:
                    correct_num += 1
                else:
                    wrong_num += 1
        print('基于相似性 准确率为：{}，召回率为：{}'.format(float(correct_num / self.base_count),
                                             (float(wrong_num + correct_num) / self.base_count)))

    def getAnswerByTempTest(self):
        correct_num = 0
        wrong_num = 0
        for entity_label, relation_label, query in self.test_data:
            URL = 'http://192.168.28.129:5000/getAnswerByTempTest/{}'.format(query)
            # print(URL)
            pre_result = json.loads(requests.get(URL).text)
            # print(pre_result)

            if pre_result:
                # print(pre_result[0])
                # print(pre_result[1])
                entity_pre, relation_pre = pre_result
                if entity_pre == entity_label and relation_pre == relation_label:
                    correct_num += 1
                else:
                    wrong_num += 1
        print('基于模板 准确率为：{}，召回率为：{}'.format(float(correct_num / self.base_count),
                                            (float(wrong_num + correct_num) / self.base_count)))


def main():
    test = test_acc_roc()
    test.getAnswerTest()
    test.getAnswerBySimTest()
    test.getAnswerByTempTest()


if __name__ == '__main__':
    # main()
    query = 'ashdfl'
    URL = 'http://10.39.61.54:5000/getAnswerByRex/微粒贷借款失败怎么办'
    # URL = 'http://10.39.61.16:5000/getAnswer/微粒贷借款失败怎么办'
    print(URL)
    # answer = requests.get(URL)
    answer = json.loads(requests.get(URL).text)
    # answer = requests.get(URL)
    print(answer)
