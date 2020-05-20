from flask import Flask, request, url_for, render_template, redirect

app = Flask(__name__)

student = [["张之林", '008', "物理院"],
           ["李林", '005', "数学院"],
           ["刘想", '002', "计科院"],
           ["高风", '003', "文学院"],
           [" 杨桃 ", '001', "生科院"]]


def findnumber(Num):  # 这里定义一个查找学号的函数，方便复用
    for i in range(len(student)):
        if student[i][1] == Num:
            return i
    return -1


def save(stu):  # 定义一个保存的函数，以文本的形式把信息保存
    try:
        studentfile = open("students.txt", "w")  # 以写模式打开，并清空文件内容
    except Exception as e:
        studentfile = open("students.txt", "x")  # 文件不存在，创建文件并打开
    for info in stu:
        studentfile.write(str(info) + "\n")  # 按行存储，添加换行符
    studentfile.close()


@app.route('/')  # 这里是根目录，也就是打开链接第一个访问的页面
def index():
    save(student)
    # 这里的student=student，等号左边是要传给html文件的变量，右边是上面定义的二维列表
    return render_template('index.html', student=student)


@app.route('/delstu', methods=['GET', 'POST'])  # 这里是删除模块，对应的页面是/delstu
def delstu():
    if request.method == 'POST':
        delnumber = request.form.get('delnumber')
        if findnumber(delnumber) == -1:
            return '您输入的学号不存在'
        else:
            del student[findnumber(delnumber)]
            save(student)
            return redirect(url_for('index'))  # 如果找到了输入的学号执行删除操作，并重定向到首页
    return render_template('delstu.html', student=student)


@app.route('/addstu', methods=['GET', 'POST'])  # 这里是添加模块
def addstu():
    if request.method == 'POST':
        addnumber = request.form.get('addnumber')
        if findnumber(addnumber) != -1:
            return "您输入的学号已存在"
        else:
            addname = request.form.get('addname')
            adddepartment = request.form.get('adddepartment')
            if addname is not None and adddepartment and addnumber is not None:  # 不为空则添加
                student.append([addname, addnumber, adddepartment])
                save(student)
                # insert_db(addnumber, addname, adddepartment)
                return redirect(url_for('index'))
    return render_template('addstu.html')  # 添加成功则重定向到首页


@app.route('/altstu', methods=['GET', 'POST'])  # 这里是修改模块，先要找到要修改的学号，如果找到了进行操作
def altstu():
    if request.method == 'POST':
        altnumber = request.form.get('altnumber')
        altdep = request.form.get('altdepartment')
        altname = request.form.get('altname')
        if findnumber(altnumber) == -1:
            return '您输入的学号不存在'
        else:
            if altdep != '':  # 这里的一对单引号里什么都没有，表示如果输入框里为空，不进行修改
                student[findnumber(altdep)][2] = altdep
            if altname != '':
                student[findnumber(altname)][0] = altname
                save(student)
            return render_template('index.html', student=student)

    return render_template('altstu.html')


@app.route('/searchstu', methods=['GET', 'POST'])
def searchstu():
    if request.method == 'POST':
        number = request.form.get('number')
        if findnumber(number) == -1:
            return '没有您要找的学号'
        else:
            find = student[findnumber(number)]
            return render_template(
                'searchstu.html',
                find=find)  # 如果找到了学号，把该学生信息传给html
    return render_template('searchstu.html', student=student)


if __name__ == '__main__':
    app.run(debug=True)
