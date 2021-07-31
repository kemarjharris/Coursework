package adapter.newmodule;
import adapter.oldmodule.Student;

public interface Classlist extends Iterable<Student> {
  public String getSession();
  public String getCourseNumber();
  public String getCourseName();
  public void addStudent(Student student);
  public Iterable<Student> getStudents();
}
