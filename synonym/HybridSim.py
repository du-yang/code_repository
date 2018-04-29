# -*- coding: utf-8 -*-
"""
@author: allendu
@desc: 融合word2vec和同义词词林和知网的相似度计算方法
"""
from synonym.hownet.hownet import HownetSim
from synonym.cilin.cilin import CilinSim
from synonym.w2v.w2v import W2vSim


class HybridSim():
    def __init__(self):
        self.cilin_hownet = CilinHownet()
        self.w2v = W2vSim()

    def sim(self,w1,w2):
        ch_score = self.cilin_hownet.sim(w1,w2)
        w2v_score = self.w2v.sim(w1,w2)
        if ch_score!=-1 and w2v_score!=-1:
            return 0.59*ch_score+0.41*w2v_score
        elif ch_score != -1 and w2v_score == -1:
            return ch_score
        elif ch_score == -1 and w2v_score != -1:
            return w2v_score
        else:
            return -1


class CilinHownet():
    '''
    混合相似度计算策略。使用了词林与知网词汇量的并集。扩大了词汇覆盖范围。
    '''
    ci_lin = CilinSim()  # 实例化词林相似度计算对象
    how_net = HownetSim()  # 实例化知网相似度计算对象
    Common = ci_lin.vocab & how_net.vocab
    A = how_net.vocab - ci_lin.vocab
    B = ci_lin.vocab - how_net.vocab

    @classmethod
    def sim(cls, w1, w2):
        lin = cls.ci_lin.sim(w1, w2) if w1 in cls.ci_lin.vocab and w2 in cls.ci_lin.vocab else 0
        how = cls.how_net.sim(w1, w2) if w1 in cls.how_net.vocab and w2 in cls.how_net.vocab else 0

        if w1 in cls.Common and w2 in cls.Common:  # 两个词都被词林和知网共同收录。
            # print('两个词都被词林和知网共同收录。', end='\t')
            # print(w1, w2, '词林改进版相似度：', lin, end='\t')
            # print('知网相似度结果为：', how, end='\t')
            return lin * 0.7 + how * 0.3

        if w1 in cls.A and w2 in cls.A:  # 两个词都只被知网收录。
            return how
        if w1 in cls.B and w2 in cls.B:  # 两个词都只被词林收录。
            return lin

        if w1 in cls.A and w2 in cls.B:  # 一个只被词林收录，另一个只被知网收录。
            # print('触发策略三，左词为知网，右词为词林')
            same_words = cls.ci_lin.code_word[cls.ci_lin.word_code[w2][0]]
            if not same_words:
                return 0.2
            all_sims = [cls.how_net.sim(word, w1) for word in same_words]
            # print(same_words, all_sims, end='\t')
            return max(all_sims)

        if w2 in cls.A and w1 in cls.B:
            # print('触发策略三，左词为词林，右词为知网')
            same_words = cls.ci_lin.code_word[cls.ci_lin.word_code[w1][0]]
            if not same_words:
                return 0.2
            all_sims = [cls.how_net.sim(word, w2) for word in same_words]
            # print(w1, '词林同义词有：', same_words, all_sims, end='\t')
            return max(all_sims)

        if w1 in cls.A and w2 in cls.Common:
            # print('策略四（左知网）：知网相似度结果为：', how)
            same_words = cls.ci_lin.code_word[cls.ci_lin.word_code[w2][0]]
            if not same_words:
                return how
            all_sims = [cls.how_net.sim(word, w1) for word in same_words]
            # print(w2, '词林同义词有：', same_words, all_sims, end='\t')
            return 0.6 * how + 0.4 * max(all_sims)

        if w2 in cls.A and w1 in cls.Common:
            # print('策略四（右知网）：知网相似度结果为：', how)
            same_words = cls.ci_lin.code_word[cls.ci_lin.word_code[w1][0]]
            if not same_words:
                return how
            all_sims = [cls.how_net.calc(word, w2) for word in same_words]
            # print(same_words, all_sims, end='\t')
            return 0.6 * how + 0.4 * max(all_sims)

        if w1 in cls.B and w2 in cls.Common:
            # print(w1, w2, '策略五（左词林）：词林改进版相似度：', lin)
            same_words = cls.ci_lin.code_word[cls.ci_lin.word_code[w1][0]]
            if not same_words:
                return lin
            all_sims = [cls.how_net.calc(word, w2) for word in same_words]
            # print(w1, '词林同义词有：', same_words, all_sims, end='\t')
            return 0.6 * lin + 0.4 * max(all_sims)

        if w2 in cls.B and w1 in cls.Common:
            # print(w1, w2, '策略五（右词林）：词林改进版相似度：', lin)
            same_words = cls.ci_lin.code_word[cls.ci_lin.word_code[w2][0]]
            if not same_words:
                return lin
            all_sims = [cls.how_net.calc(word, w1) for word in same_words]
            # print(w2, '词林同义词有：', same_words, all_sims, end='\t')
            return 0.6 * lin + 0.4 * max(all_sims)

        # print('对不起，词语可能未收录，无法计算相似度！')
        return -1

if __name__ == '__main__':
    hs = HybridSim()
    print(hs.sim("汽车","轿车"))
