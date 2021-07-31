package adapter.newmodule;

import java.util.Iterator;

import adapter.oldmodule.Student;

public class ClasslistAdapter implements Classlist {

    private adapter.oldmodule.Classlist adapter;

    public ClasslistAdapter(adapter.oldmodule.Classlist adapter) {
        this.adapter = adapter;
    }

    @Override
    public String getSession() {
        return adapter.getSession();
    }

    @Override
    public String getCourseNumber() {
        return adapter.getCourseNumber();
    }

    @Override
    public String getCourseName() {
        return adapter.getCourseName();
    }

    @Override
    public void addStudent(Student student) {
        adapter.addStudent(student);
    }

    @Override
    public Iterable<Student> getStudents() {
        return this;
    }

    @Override
    public Iterator<Student> iterator() {
        return adapter.getStudents().asIterator();
    }
    
}
