import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;

class InvalidProductIdException extends Exception {
    public InvalidProductIdException(String msg) { super(msg); }
}

class OutOfStockException extends Exception {
    public OutOfStockException(String msg) { super(msg); }
}

class EmptyOrderException extends Exception {
    public EmptyOrderException(String msg) { super(msg); }
}

public class LabTask2OrderSystem {

    static class Product {
        String name;
        double price;
        int stock;
        Product(String name, double price, int stock) {
            this.name = name; this.price = price; this.stock = stock;
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        Map<Integer, Product> catalog = new HashMap<>();
        catalog.put(101, new Product("Wireless Mouse",  1500, 5));
        catalog.put(102, new Product("USB-C Cable",      800, 10));
        catalog.put(103, new Product("Mechanical Keyboard", 7500, 2));

        try {
            System.out.println("--- Product Catalog ---");
            for (Map.Entry<Integer, Product> en : catalog.entrySet()) {
                Product p = en.getValue();
                System.out.println(en.getKey() + "  " + p.name + "  Rs." + p.price + "  stock=" + p.stock);
            }

            System.out.print("Enter number of items to order: ");
            int items = sc.nextInt();
            if (items <= 0) {
                throw new EmptyOrderException("Order must contain at least one item");
            }

            double total = 0;
            for (int i = 1; i <= items; i++) {
                System.out.print("Item " + i + " product id: ");
                int pid = sc.nextInt();
                if (!catalog.containsKey(pid)) {
                    throw new InvalidProductIdException("Product id " + pid + " does not exist");
                }
                System.out.print("Item " + i + " quantity: ");
                int qty = sc.nextInt();
                Product p = catalog.get(pid);
                if (qty <= 0) {
                    throw new EmptyOrderException("Quantity for product " + pid + " must be greater than zero");
                }
                if (qty > p.stock) {
                    throw new OutOfStockException("Only " + p.stock + " units of " + p.name + " in stock, requested " + qty);
                }
                p.stock -= qty;
                total += qty * p.price;
                System.out.println("Added " + qty + " x " + p.name);
            }

            System.out.println("Order placed successfully");
            System.out.println("Total amount: Rs." + total);
        } catch (InvalidProductIdException e) {
            System.out.println("InvalidProductIdException: " + e.getMessage());
        } catch (OutOfStockException e) {
            System.out.println("OutOfStockException: " + e.getMessage());
        } catch (EmptyOrderException e) {
            System.out.println("EmptyOrderException: " + e.getMessage());
        } catch (Exception e) {
            System.out.println("Invalid input type. Please enter values in the correct format.");
        } finally {
            sc.close();
        }
    }
}
