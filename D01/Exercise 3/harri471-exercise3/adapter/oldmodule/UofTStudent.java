package adapter.oldmodule;

import java.util.Date;

public class UofTStudent implements Student {

  private String stunum;
  private String[] name;
  private Date dob;
  private String email;

  public UofTStudent(String stunum, String[] name, Date dob, String email) {
    this.stunum = stunum;
    this.name = name;
    this.dob = dob;
    this.email = email;
  }

  @Override
  public String getStudentNumber() {
    return stunum;
  }

  @Override
  public String[] getName() {
    return name;
  }

  @Override
  public Date getDOB() {
    return dob;
  }

  @Override
  public String getEmail() {
    return email;
  }
  
  @Override
  public boolean equals(Object other) {
    return this.getClass().equals(other.getClass()) &&
        getName().equals(((Student)other).getName()) &&
        getDOB().equals(((Student)other).getDOB()) &&
        getEmail().equals(((Student)other).getEmail());
  }
}
