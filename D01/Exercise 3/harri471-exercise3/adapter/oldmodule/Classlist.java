package adapter.oldmodule;

import java.util.Enumeration;
import java.util.Vector;

public class Classlist {
  private String session;
  private String courseNumber;
  private String courseName;
  private Vector<Student> students;
  
  public Classlist(String session, String courseNumber, String courseName) {
    this.session = session;
    this.courseNumber = courseNumber;
    this.courseName = courseName;
    students = new Vector<>();
  }

  public String getSession() {
    return session;
  }

  public String getCourseNumber() {
    return courseNumber;
  }

  public String getCourseName() {
    return courseName;
  }
  
  public void addStudent(Student student) {
    students.add(student);
  }

  public Enumeration<Student> getStudents() {
    return students.elements();
  }  
}
