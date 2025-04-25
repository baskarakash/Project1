public class BankAccount {
    private String owner;
    private double balance;

    public BankAccount(String owner, double initialBalance) {
        this.owner = owner;
        this.balance = initialBalance;
    }

    public void deposit(double amount) {
        if (amount > 0) {
            balance += amount;
            System.out.println(owner + " deposited $" + amount);
        } else {
            System.out.println("Invalid deposit amount");
        }
    }

    public void withdraw(double amount) {
        if (amount > 0 && balance >= amount) {
            balance -= amount;
            System.out.println(owner + " withdrew $" + amount);
        } else {
            System.out.println("Invalid or insufficient balance");
        }
    }

    public void displayBalance() {
        System.out.println(owner + "'s balance: $" + balance);
    }

    public static void main(String[] args) {
        BankAccount alice = new BankAccount("Alice", 500);
        alice.displayBalance();

        alice.deposit(200);
        alice.withdraw(100);
        alice.displayBalance();

        BankAccount bob = new BankAccount("Bob", 300);
        bob.deposit(50);
        bob.withdraw(400); // Should trigger insufficient balance
        bob.displayBalance();
    }
}
