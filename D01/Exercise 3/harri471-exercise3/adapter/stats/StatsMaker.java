package adapter.stats;

import java.util.ArrayList;
import java.util.List;

import adapter.newmodule.Classlist;
import adapter.oldmodule.Student;

public class StatsMaker {
  
  public static List<Student> studentsWithMissingEmails(Classlist classlist) {
    
    List<Student> noEmails = new ArrayList<>();
    for (Student student: classlist.getStudents()) {
      if (student.getEmail().equals("")) {
        noEmails.add(student);
      }
    }
    return noEmails;
  }
}
