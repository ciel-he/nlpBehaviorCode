import os, sys
def concatTxt(file1path,file2path,result_path,salt):
    base= '../tkData/'
    result_path = base+salt+result_path
    print(result_path)
    try:
        os.remove(result_path)
    except IOError:
        print("Error: 删除结果文件失败")

    try:
        file_1 = open(file1path, 'r', encoding='utf-8')
        file_2 = open(file2path, 'r', encoding='utf-8')
        file_new = open(result_path, 'w', encoding='utf-8')
    except IOError:
        print("Error: 合并文件失败：没有找到文件或读取文件失败")
    else :
        for line in file_1.readlines():
            file_new.write(line)
        file_1.close()


        for line in file_2.readlines():
            file_new.write(line)
        file_2.close()

        file_new.close()
        try:
            os.remove(file1path)
            os.remove(file2path)
        except IOError:
            print("Error: 删除科1科4文件失败")


    return