package turtlesolution;

import java.util.Iterator;

/**
 * An Iterable collection of Turtles.
 * @author anya
 */
public class Turtles implements Iterable<Turtle> {

  public static final String TURTLE_NAME = "Turtle on ";

  @Override
  public Iterator<Turtle> iterator() {
    return new Iterator<Turtle>() {
      @Override
      public boolean hasNext() {
        return true;
      }

      @Override
      public Turtle next() {
        return new Turtle(TURTLE_NAME);
      }
    };
  }

}
