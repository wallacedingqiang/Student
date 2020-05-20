//document.write("<script language=javascript src='jquery-3.2.1.slim.min.js'></script>");
function print_course_list(course_list){
    $("table").empty();
    $("table").append("<tr>" +
                            "<th>#</th>" +
                            "<th>Course</th>" +
                            "<th>Teacher</th>" +
                            "<th>CourseID</th>" +
                            "<th>Class</th>" +
                        "</tr>");
    for(var i=0;i<course_list.length;i++)
    {
        $("table").append("<tr>" +
                                "<td><input type=checkbox name="+course_list[i].name+" onclick=add_course(this)></td>" +
                                "<td>"+course_list[i].name+"</td>" +
                                "<td>"+course_list[i].teacher+"</td>" +
                                "<td>"+course_list[i].id+"</td>" +
                                "<td>"+course_list[i].class_room+"</td>" +
                           "</tr>");
    }
}
function course(id,name,teacher,class_room) {
    this.id=id;
    this.name=name;
    this.teacher=teacher;
    this.class_room=class_room;
}

function add_course(checked_ele) {
    if(checked_ele.checked){
        checked_course.push($(checked_ele).attr("name"));
    }
    else{
        checked_course.splice(jQuery.inArray($(checked_ele).attr("name")),1);
    }
}


