class Product {
    String code;
    String productName;
    double unitPrice;
    int stock;

    Product(String code, String productName, double unitPrice, int stock) {
        this.code = code;
        this.productName = productName;
        this.unitPrice = unitPrice;
        this.stock = stock;
    }

    void setCode(String code) { 
        this.code = code; 
    }
    String getCode() { 
        return code; 
    }

    void setProductName(String productName) { 
        this.productName = productName; 
    }
    String getProductName() { 
        return productName; 
    }

    void setUnitPrice(double unitPrice) { 
        this.unitPrice = unitPrice; 
    }
    double getUnitPrice() { 
        return unitPrice; 
    }

    void setStock(int stock) { 
        this.stock = stock; 
    }
    int getStock() { 
        return stock; 
    }

    double calcTotalValue() {
        return unitPrice * stock;
    }
}

class InventoryManager {
    Product itemList[];
    int numItems;

    InventoryManager(Product itemList[], int numItems) {
        this.itemList = itemList;
        this.numItems = numItems;
    }

    Product findMostValuable() {
        Product best = itemList[0];
        int idx = 1;
        while(idx < numItems) {
            if(itemList[idx].calcTotalValue() > best.calcTotalValue())
                best = itemList[idx];
            idx++;
        }
        return best;
    }

    double calcGrandTotal() {
        double sum = 0;
        int idx = 0;
        while(idx < numItems) {
            sum = sum + itemList[idx].calcTotalValue();
            idx++;
        }
        return sum;
    }

    void showInventoryReport() {
        int idx = 0;
        while(idx < numItems) {
            System.out.println(itemList[idx].getCode() + ", " + itemList[idx].getProductName() 
                               + ", " + itemList[idx].getUnitPrice() + ", " + itemList[idx].getStock() 
                               + ", Value: " + itemList[idx].calcTotalValue());
            idx++;
        }
        System.out.println("Total Value: " + calcGrandTotal());
        Product best = findMostValuable();
        System.out.println("Highest: " + best.getProductName() + ", " + best.calcTotalValue());
    }
}

public class Task5 {
    public static void main(String args[]) {
        Product itemList[] = new Product[5];
        itemList[0] = new Product("W001", "Printer", 25000, 8);
        itemList[1] = new Product("W002", "Router", 4500, 25);
        itemList[2] = new Product("W003", "Tablet", 55000, 12);
        itemList[3] = new Product("W004", "Charger", 1200, 60);
        itemList[4] = new Product("W005", "Headphones", 8000, 40);

        InventoryManager manager = new InventoryManager(itemList, 5);
        manager.showInventoryReport();

        System.out.println(itemList[2].getProductName() + ", Value: " + itemList[2].calcTotalValue());
    }
}
