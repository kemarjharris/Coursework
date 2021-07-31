package adapter.stats;

import java.util.Date;
import java.util.List;

import adapter.newmodule.Classlist;
import adapter.newmodule.ClasslistAdapter;
import adapter.oldmodule.Student;
import adapter.oldmodule.UofTStudent;

public class Main {
  public static void main(String[] args) {
    Student aStudent = new UofTStudent("1111111111",
        new String[] {"First", "Firsting"},
        new Date(),
        "first.firsting@utoronto.ca");
    Student bStudent = new UofTStudent("2222222222",
        new String[] {"Second", "Seconding"},
        new Date(),
        "second.seconding@utoronto.ca");
    Student cStudent = new UofTStudent("3333333333",
        new String[] {"Third", "Thirding"},
        new Date(),
        "third.thirding@utoronto.ca");
    Student dStudent = new UofTStudent("4444444444",
        new String[] {"NoEmail", "NoEmail"},
        new Date(),
        "");
    adapter.oldmodule.Classlist classlist = new adapter.oldmodule.Classlist("winter2019",
        "CSCD01", "Software Engineering 2");
    classlist.addStudent(aStudent);
    classlist.addStudent(bStudent);
    classlist.addStudent(cStudent);
    classlist.addStudent(dStudent);

    Classlist cAdapter = new ClasslistAdapter(classlist);
    List<Student> noEmails = StatsMaker.studentsWithMissingEmails(cAdapter);
    System.out.println(noEmails);
  }
}
