package turtlesolution;

import java.util.Random;

public class Main {
  /**
   * Demos the use of Turtles.
   * @param args as usual
   */
  public static void main(String[] args) {
    Random rn = new Random();
    Turtles turtles = new Turtles();

    // A for-each loop over Turtles should ALWAYS be an infinite loop,
    // where each subsequent Turtle is a NEW Turtle object with the
    // name Turtles.TURTLE_NAME.
    for (Turtle turtle: turtles) {
      System.out.print(turtle);
      if (rn.nextInt(10) < 4) {
        System.out.println("...\nEnough already!");
        return;
      }
    }
  }
}
