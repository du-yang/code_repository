import xlwt
from collections import defaultdict

def result():
    w = xlwt.Workbook()
    sheet = w.add_sheet('sheet1')

    with open('./data/1.0.1') as f1:
        data1 = [line for line in f1]
    with open('./data/1.1.0') as f2:
        data2 = [line for line in f2]
    assert len(data1)==len(data2)
    datalen = len(data1)

    j=0
    for i in range(datalen):
        # if i>50:break
        # if data1[i]!=data2[i] and data1[i].split()[:-1]==data2[i].split()[:-1]:
        if data1[i]!=data2[i] and data1[i].split()[:-1]==data2[i].split()[:-1]:
            try:
                sheet.write(j, 0, data1[i])
                sheet.write(j, 1, data2[i])
                print(str(i)+':'+data1[i])
                print(str(i)+':'+data2[i])
                j+=1
            except ValueError as e:
                print(e)
    w.save('compare.xls')

def test():
    w = xlwt.Workbook()
    sheet = w.add_sheet('sheet1')
    sheet.write(0, 0, 'uquery')
    sheet.write(0, 1, 'HKUST1.0.1')
    sheet.write(0, 2, 'score')
    sheet.write(0, 3, 'HKUST1.0.1')
    sheet.write(0, 4, 'score')


    with open('./data/1.0.1') as f1:
        data1 = [line for line in f1]
    with open('./data/1.1.0') as f2:
        data2 = [line for line in f2]

    data_dict1 = defaultdict(list)
    data_dict2 = defaultdict(list)
    final_data = defaultdict(list)


    for i,line in enumerate(data1):
        print(i)
        item = line.strip('\n').split('\t')
        data_dict1[item[0]].append(item[1:])
    for i,line in enumerate(data2):
        print(i)
        item = line.strip('\n').split('\t')
        data_dict2[item[0]].append(item[1:])



    for it in data_dict1:
        items = sorted(data_dict1[it],key=lambda x:float(x[-1]),reverse=True)
        print('---'+it+'---')
        print(items[0])
        final_data[it].append(items[0])

    for it in data_dict2:
        items = sorted(data_dict2[it], key=lambda x: float(x[-1]), reverse=True)
        print('---' + it + '---')
        print(items[0])
        final_data[it].append(items[0])
    # print(data_dict)
    final_data
    ii = 1
    for key in final_data:
        if final_data[key][0][0]!=final_data[key][1][0]:
            sheet.write(ii, 0, key)
            sheet.write(ii, 1, final_data[key][0][0])
            sheet.write(ii, 2, final_data[key][0][1])
            sheet.write(ii, 3, final_data[key][1][0])
            sheet.write(ii, 4, final_data[key][1][1])
            ii+=1

    w.save('HKUSTdifferent.xls')



if __name__ == '__main__':
    # result()
    test()
    # data = [['王 鹏 大 神 是 哪位 680', '3'], ['王 鹏 到底 是 谁 啊 10', '5'], ['王 鹏 大 神 是 哪位 779', '0']]
    # data = sorted(data,key=lambda x:float(x[-1]),reverse=True)
    # print(data)