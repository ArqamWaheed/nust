class Product {
    String productId;
    String name;
    double price;
    int quantity;

    Product(String productId, String name, double price, int quantity) {
        this.productId = productId;
        this.name = name;
        this.price = price;
        this.quantity = quantity;
    }

    void setProductId(String productId) { 
        this.productId = productId; 
    }
    String getProductId() { 
        return productId; 
    }

    void setName(String name) { 
        this.name = name; 
    }
    String getName() { 
        return name; 
    }

    void setPrice(double price) { 
        this.price = price; 
    }
    double getPrice() { 
        return price; 
    }

    void setQuantity(int quantity) { 
        this.quantity = quantity; 
    }
    int getQuantity() { 
        return quantity; 
    }

    double calcInventoryValue() {
        return price * quantity;
    }
}

class InventoryManager {
    Product products[];
    int productCount;

    InventoryManager(Product products[], int productCount) {
        this.products = products;
        this.productCount = productCount;
    }

    Product findHighestValueProduct() {
        Product highest = products[0];
        int i = 1;
        while(i < productCount) {
            if(products[i].calcInventoryValue() > highest.calcInventoryValue())
                highest = products[i];
            i++;
        }
        return highest;
    }

    double calcTotalInventoryValue() {
        double total = 0;
        int i = 0;
        while(i < productCount) {
            total = total + products[i].calcInventoryValue();
            i++;
        }
        return total;
    }

    void printInventoryReport() {
        System.out.println("========================================");
        System.out.println("   PRODUCT INVENTORY REPORT");
        System.out.println("========================================");
        int i = 0;
        while(i < productCount) {
            System.out.println("Product ID: " + products[i].getProductId());
            System.out.println("Name: " + products[i].getName());
            System.out.println("Price: Rs. " + products[i].getPrice());
            System.out.println("Quantity: " + products[i].getQuantity());
            System.out.println("Inventory Value: Rs. " + products[i].calcInventoryValue());
            System.out.println("----------------------------------------");
            i++;
        }
        System.out.println("Total Inventory Value: Rs. " + calcTotalInventoryValue());
        Product highest = findHighestValueProduct();
        System.out.println("Highest Value Product: " + highest.getName() 
                           + " (Rs. " + highest.calcInventoryValue() + ")");
        System.out.println("========================================");
    }
}

public class Task5 {
    public static void main(String args[]) {
        Product products[] = new Product[4];
        products[0] = new Product("P001", "Laptop", 85000, 10);
        products[1] = new Product("P002", "Mouse", 1500, 50);
        products[2] = new Product("P003", "Keyboard", 3500, 30);
        products[3] = new Product("P004", "Monitor", 45000, 15);

        InventoryManager manager = new InventoryManager(products, 4);
        manager.printInventoryReport();

        System.out.println();
        System.out.println("Checking individual product:");
        System.out.println("Product: " + products[0].getName());
        System.out.println("Inventory Value: Rs. " + products[0].calcInventoryValue());
    }
}
