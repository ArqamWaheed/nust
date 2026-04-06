class Shape {
    double calculateArea() {
        return 0;
    }

    void displayArea() {
        System.out.println("Area: " + calculateArea());
    }
}

class Circle extends Shape {
    double radius;

    Circle(double radius) {
        this.radius = radius;
    }

    void setRadius(double radius) { 
        this.radius = radius; 
    }
    double getRadius() { 
        return radius; 
    }

    double calculateArea() {
        return Math.PI * radius * radius;
    }

    double calculateArea(double r) {
        return Math.PI * r * r;
    }
}

class Square extends Shape {
    double side;

    Square(double side) {
        this.side = side;
    }

    void setSide(double side) { 
        this.side = side; 
    }
    double getSide() { 
        return side; 
    }

    double calculateArea() {
        return side * side;
    }

    double calculateArea(double s) {
        return s * s;
    }
}

class Triangle extends Shape {
    double base;
    double height;

    Triangle(double base, double height) {
        this.base = base;
        this.height = height;
    }

    void setBase(double base) { 
        this.base = base; 
    }
    double getBase() { 
        return base; 
    }

    void setHeight(double height) { 
        this.height = height; 
    }
    double getHeight() { 
        return height; 
    }

    double calculateArea() {
        return 0.5 * base * height;
    }

    double calculateArea(double b, double h) {
        return 0.5 * b * h;
    }
}

public class Task1Lab9 {
    public static void main(String args[]) {
        Circle circle = new Circle(5.0);
        Square square = new Square(4.0);
        Triangle triangle = new Triangle(6.0, 3.0);

        Shape shapes[] = { circle, square, triangle };

        int i = 0;
        while(i < shapes.length) {
            System.out.println("Shape " + (i + 1) + " area: " + shapes[i].calculateArea());
            i++;
        }

        System.out.println("Circle area with radius 7: " + circle.calculateArea(7.0));
        System.out.println("Square area with side 9: " + square.calculateArea(9.0));
        System.out.println("Triangle area with base 10 height 5: " + triangle.calculateArea(10.0, 5.0));
    }
}
