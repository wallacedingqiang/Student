from flask import Flask, session, flash, json
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, url_for, render_template, redirect
import pysnooper


app = Flask(__name__)  # 创建一个Flask app对象
# 数据库链接的配置，此项必须，格式为（数据库+驱动://用户名:密码@数据库主机地址:端口/数据库名称）
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:d123456@106.15.237.25:3306/test?charset=UTF8MB4'
# 跟踪对象的修改，在本例中用不到调高运行效率，所以设置为False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app=app)  # 为哪个Flask app对象创建SQLAlchemy对象，赋值为db
manager = Manager(app=app)  # 初始化manager模块


class Student(db.Model):  # 继承SQLAlchemy.Model对象，一个对象代表了一张表
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        unique=True)  # id 整型，主键，自增，唯一
    num = db.Column(db.Integer, default=20)  # 学号 整型，默认为20
    name = db.Column(db.String(20))  # 名字 字符串长度为20
    school = db.Column(db.String(50))  # 学校 字符串长度为50

    __tablename__ = 'student'  # 该参数可选，不设置会默认的设置表名，如果设置会覆盖默认的表名

    def __init__(self, num, name, school):  # 初始化方法，可以对对象进行创建
        self.num = num
        self.name = name
        self.school = school

    def __repr__(self):  # 输出方法，与__str__类似，但是能够重现它所代表的对象
        return '<Student %r,%r, %r, %r>' % (
            self.id, self.num, self.name, self.school)


# class User(db.Model):
#     __tablename__ = 'usernew'
#
#     id=db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.VARCHAR(20))
#     password = db.Column(db.VARCHAR(20))
#     #course = db.relationship('Course',secondary=selected, backref='student')
#
#     def __int__(self,name,password):
#         self.name=name
#         self.password=password



class Course(db.Model):
    __tablename__ = 'course'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.VARCHAR(20))
    teacher = db.Column(db.VARCHAR(20))
    class_room = db.Column(db.VARCHAR(20))




    def __init__(self,name,teacher,class_room):
        self.name = name
        self.teacher = teacher
        self.class_room = class_room





@app.before_first_request
def create_db():
    # Recreate database each time for demo
    db.drop_all()
    db.create_all()
    stu = Student(1,'张三', '交大')
    db.session.add(stu)
    stuother = [Student(2,'李四', '复旦'),
               Student(3,'王五', '同济'),
               Student(4,'丁六', '清华'),
               Student(5,'仲八', '北大'),
               Student(6, '蔷蔷', '巧虎')]
    db.session.add_all(stuother)

    # user=User('李四', '123456')
    # db.session.add(user)

    print(1)

    course=Course('python', '王五','2011')
    db.session.add(course)
    couother = [Course('体育', '张三','1011'),
                Course('美术', '王五','3011'),
                Course('英语', '王五','4011'),
                Course('计算机', '王五','5011'),
                Course('数学', '王五','6011')]
    db.session.add_all(couother)


    print(course)


    db.session.commit()




@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/election',methods=['GET', 'POST'])
def election():
    cou = Course.query.all()
    # sql = 'select * from course;'
    # cou = db.session.execute(sql)
    print(cou)
    return render_template('listcourse.html',cou=cou)


@app.route('/delstu', methods=['GET', 'POST'])  # 这里是删除模块，对应的页面是/delstu
def delstu():
    if request.method == 'POST':
        delnumber = request.form.get('delnumber')
        user3 = Student.query.filter_by(num=delnumber).first()
        db.session.delete(user3)
        db.session.commit()
    return render_template('delstu.html')


# 删除学员  需要从前端传递过来学员的id  查询字符串
@app.route('/delete_stu')
def delete_stu():
    # 获取学员的id
    stuid = request.args.get("stuid")
    try:
        # 防止前端传入的数据不符合
        stuid = int(stuid)
    except BaseException as e:
        flash("参数错误了")
        return redirect(url_for("userslist"))

    # 查询该学员
    try:
        stu = Student.query.get(stuid)
        # 删除该学员
        db.session.delete(stu)
        db.session.commit()

    except BaseException as e:
        flash("数据库操作失败")
        db.session.rollback()
        return redirect(url_for("userslist"))

    return redirect(url_for("userslist"))


@app.route('/addstu', methods=['GET', 'POST'])  # 这里是添加模块
def addstu():
    if request.method == 'POST':
        addnumber = request.form.get('addnumber')
        addname = request.form.get('addname')
        adddepartment = request.form.get('adddepartment')
        # if addname is not None and adddepartment and addnumber is not None:
        # # 不为空则添加
        stu = Student(num=addnumber, name=addname, school=adddepartment)
        db.session.add(stu)
        db.session.commit()
    return render_template('addstu.html')
    # 添加成功则重定向到首页


@app.route('/altstu', methods=['GET', 'POST'])  # 这里是修改模块，先要找到要修改的学号，如果找到了进行操作
def altstu():
    if request.method == 'POST':
        altnumber = request.form.get('altnumber')
        altdep = request.form.get('altdepartment')
        altname = request.form.get('altname')
        # 更新数据
        stu = Student.query.filter_by(num=altnumber).first()
        stu.num = altnumber
        stu.name = altname
        stu.school = altdep
        db.session.commit()
    return render_template('altstu.html')

@pysnooper.snoop()
@app.route('/alt_stu', methods=['GET', 'POST'])
def alt_stu():
    # 获取学员的id
    stuid = request.args.get("stuid")
    find = Student.query.filter_by(id=stuid).first()

    if request.method == 'POST':

        print(1)
        altnumber = request.form.get('altnumber')
        altdep = request.form.get('altdepartment')
        altname = request.form.get('altname')

        # 更新数据
        stu = Student.query.filter_by(num=altnumber).first()
        stu.num = altnumber
        stu.name = altname
        stu.school = altdep
        db.session.commit()

    print(2)

    return render_template('altstunew.html',find=find)
    #  return redirect(url_for("userslist"))


@app.route('/searchstu', methods=['GET', 'POST'])
def searchstu():
    if request.method == 'POST':
        number = request.form.get('number')
        if number == '':
            return '没有您要找的学号'
        else:
            find = Student.query.filter_by(num=number).first()    #filter_by类似where
            print(find)
            return render_template('searchstu.html',find=find)  # 如果找到了学号，把该学生信息传给html
    return render_template('searchstu.html')


@app.route('/studentlist', methods=['GET', 'POST'])
def userslist():
    stu = Student.query.all()
    print(stu)
    return render_template('liststudentnew.html', stu=stu)

if __name__ == '__main__':
    manager.run(Debug=True)  # 运行服务器
