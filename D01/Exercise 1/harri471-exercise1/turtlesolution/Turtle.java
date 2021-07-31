package turtlesolution;

/**
 * A Turtle with a name.
 * @author anya
 */
public class Turtle {
  private String name;
  
  /**
   * Creates a new Turtle with the given name.
   * @param name name of the new Turtle
   */
  public Turtle(String name) {
    this.name = name;
  }
  
  /**
   * Returns the name of this Turtle.
   * @return the name of this Turtle
   */
  public String getName() {
    return name;
  }

  @Override
  public String toString() {
    return getName();
  }  
}
