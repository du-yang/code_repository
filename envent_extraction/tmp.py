from ngrams import freqPhrase
import jieba
import re


def main():
    with open("rawdata.txt",encoding="utf8") as f:
        line_data = [line.strip() for line in f if line.strip()]
        seg_data = [list(jieba.cut(line)) for line in line_data]

    data_format = {"headline":line_data[0],"content":line_data[1:],"seg_content":seg_data[1:]}

    nm = freqPhrase(minCount=4,threshold=0.5)
    ngram_finder = nm.combine2words

    # key_word = find_key_word(ngram_finder,data_format)
    find_key_word(ngram_finder,data_format)
    # print(key_word)
    # find_key_word_by_rex(data_format)
    for line in data_format["content"]:
        match_result = re.match(',(.*?)收获.*',line)
        try:
            print(match_result.group(1))
        except Exception as e:
            pass


def find_key_word_by_rex(data_dict):
    import re
    data = data_dict["content"]
    data = ''.join(data)
    headline = data_dict["headline"]
    for interval_len in range(2,len(headline)):
        for i in range(len(headline)-interval_len):
            word = headline[i:i+interval_len+1]
            finded_num = len(re.findall(word,data))
            print(word,finded_num)


def find_key_word(ngram_finder,data_dict):
    seg_data = data_dict["seg_content"]
    ngrams = ngram_finder(seg_data)
    ngrams = sorted(ngrams.items(), key=lambda a: a[1][0], reverse=True)
    ngram_result = [''.join(line[0]) for line in ngrams]
    for word in ngram_result:
        print(word)

        # if word in data_dict["headline"]:
        #     return word
    return None


if __name__ == '__main__':
    main()
        # find_key_word
    # import jieba.posseg as jse
    # print(jse.cut("每日优鲜获得创立以来最大一笔融资金额5亿美元"))