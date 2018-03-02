import xlrd


def getNum():
    book = xlrd.open_workbook("HKUSTdifferent.xls",formatting_info=True)
    sheet = book.sheet_by_index(0)
    rows, cols = sheet.nrows, sheet.ncols
    print(rows,cols)
    j=0
    for i in range(1,rows):
        xfx = sheet.cell_xf_index(i, 3)
        xf = book.xf_list[xfx]

        bg = xf.background.pattern_colour_index
        if bg == 10:j+=1
    print(j)
        # print(sheet.cell(i,1).background.pattern_colour_index)




if __name__ == '__main__':
    getNum()
