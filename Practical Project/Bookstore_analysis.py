import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

class Bookstore:
    def __init__(self, inv_file="inventory.csv", sales_file="sales.csv"):
        self.inv_file = inv_file
        self.sales_file = sales_file
        self.inventory_df = self.load_data(inv_file, ["Title", "Author", "Genre", "Price", "Quantity"])
        self.sales_df = self.load_data(sales_file, ["Date", "Title", "Quantity_Sold", "Total_Revenue"])
    
    def load_data(self, filepath, default_columns):
        """Safely loads data and fixes old column names."""
        try:
            df = pd.read_csv(filepath)
            # THIS LINE FIXES THE ERROR: Replaces spaces with underscores in column names
            df.columns = df.columns.str.replace(' ', '_')
            return df
        except (FileNotFoundError, pd.errors.EmptyDataError):
            return pd.DataFrame(columns=default_columns)
        except Exception as e:
            print(f"[Error] Could not load {filepath}: {e}")
            return pd.DataFrame(columns=default_columns)
            
    def save_data(self):
        """Saves the current data back to the CSV files."""
        self.inventory_df.to_csv(self.inv_file, index=False)
        self.sales_df.to_csv(self.sales_file, index=False)
        print("\n-> Data saved successfully to CSV files.")
    
    def add_book(self, Title, Author, Genre, Price, Quantity):
        if Price <= 0 or Quantity <= 0:
            print("-> Price and Quantity must be greater than 0.")
            return

        if Title in self.inventory_df["Title"].values:
            idx = self.inventory_df.index[self.inventory_df["Title"] == Title][0]
            self.inventory_df.loc[idx, "Quantity"] += Quantity
            print(f"-> Book '{Title}' already exists. Stock increased by {Quantity}.")
        else:
            self.inventory_df.loc[len(self.inventory_df)] = [Title, Author, Genre, Price, Quantity]
            print(f"-> Added new book: '{Title}' by {Author}.")
    
    def update_inventory(self, title, quantity):
        if quantity <= 0:
            print("-> Quantity should be positive!")
            return

        if title in self.inventory_df["Title"].values:
            idx = self.inventory_df.index[self.inventory_df["Title"] == title][0]
            self.inventory_df.loc[idx, "Quantity"] += quantity
            print(f"-> Stock updated successfully for '{title}'.")
        else:
            print(f"-> Cannot update: Book '{title}' not found.")
        
    def record_sale(self, title, quantity):
        if quantity <= 0:
            print("-> Quantity must be positive!")
            return

        if title in self.inventory_df["Title"].values: 
            idx = self.inventory_df.index[self.inventory_df["Title"] == title][0]
            stock = self.inventory_df.loc[idx, "Quantity"]
            price = self.inventory_df.loc[idx, "Price"]
            
            if quantity > stock:
                print(f"-> Not enough stock for '{title}'. Only {stock} copies left!")
                return
            
            self.inventory_df.loc[idx, "Quantity"] -= quantity
            Total_Revenue = price * quantity
            
            date_str = datetime.now().strftime('%Y-%m-%d')
            self.sales_df.loc[len(self.sales_df)] = [date_str, title, quantity, Total_Revenue]
            
            print(f"-> Sold {quantity} copies of '{title}' for ${Total_Revenue:.2f}.")
        else:
            print(f"-> Cannot sell '{title}'. Book not found in inventory.")

    def generate_report(self):
        print("\n" + "="*40)
        print("          BOOKSTORE REPORT")
        print("="*40)
        
        total_books = len(self.inventory_df)
        total_stock = self.inventory_df["Quantity"].sum() if not self.inventory_df.empty else 0
        total_revenue = self.sales_df["Total_Revenue"].astype(float).sum() if not self.sales_df.empty else 0
        total_sold = self.sales_df["Quantity_Sold"].astype(int).sum() if not self.sales_df.empty else 0

        print(f"Total Unique Books:      {total_books}")
        print(f"Total Stock Available:   {total_stock}")
        print(f"Total Units Sold:        {total_sold}")
        print(f"Total Revenue Generated: ${total_revenue:.2f}")
        
        if not self.sales_df.empty:
            print("\n--- Top Best-Selling Books ---")
            top_books = self.sales_df.groupby('Title')['Quantity_Sold'].sum().sort_values(ascending=False).head(5)
            print(top_books.to_string())
        print("="*40)

    def visualize_data(self):
        """Generates a 2x2 dashboard of sales and inventory visualizations."""
        
        # 1. Safety Check: Ensure there is data to plot
        if self.sales_df.empty:
            print("\n-> Not enough sales data to generate visualizations. Please record some sales first.")
            return
            
        print("\n-> Generating visual dashboard... Close the popup window to return to the menu.")

        # 2. Merge Data: Combine sales and inventory to link Genre/Price to Sales
        # We merge on 'Title' so every sale knows the Genre and Price of that book
        merged_df = pd.merge(self.sales_df, self.inventory_df, on="Title", how="inner")
        
        # 3. Ensure Data Types are correct for plotting
        merged_df['Quantity_Sold'] = merged_df['Quantity_Sold'].astype(int)
        merged_df['Total_Revenue'] = merged_df['Total_Revenue'].astype(float)
        merged_df['Price'] = merged_df['Price'].astype(float)
        merged_df['Date'] = pd.to_datetime(merged_df['Date'])

        # 4. Set up the Matplotlib Figure (A 2x2 Grid)
        sns.set_theme(style="whitegrid") # Sets a clean background
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Bookstore Performance Dashboard', fontsize=18, fontweight='bold')
        
        # --- PLOT 1: Bar Chart (Total Sales by Genre) ---
        sales_by_genre = merged_df.groupby('Genre')['Quantity_Sold'].sum().reset_index()
        sns.barplot(
            data=sales_by_genre, x='Genre', y='Quantity_Sold', 
            ax=axes[0, 0], hue='Genre', palette='viridis', legend=False
        )
        axes[0, 0].set_title('Total Unit Sales by Genre', fontsize=12, fontweight='bold')
        axes[0, 0].set_ylabel('Total Units Sold')
        axes[0, 0].set_xlabel('')
        
        # --- PLOT 2: Line Graph (Sales Trends Over Time) ---
        sales_trend = merged_df.groupby('Date')['Total_Revenue'].sum().reset_index()
        sns.lineplot(
            data=sales_trend, x='Date', y='Total_Revenue', 
            marker='o', ax=axes[0, 1], linewidth=2
        )
        axes[0, 1].set_title('Daily Revenue Trends', fontsize=12, fontweight='bold')
        axes[0, 1].set_ylabel('Total Revenue ($)')
        axes[0, 1].set_xlabel('')
        axes[0, 1].tick_params(axis='x', rotation=45) # Angle dates so they fit
        
        # --- PLOT 3: Pie Chart (Revenue Share by Genre) ---
        revenue_by_genre = merged_df.groupby('Genre')['Total_Revenue'].sum()
        axes[1, 0].pie(
            revenue_by_genre, labels=revenue_by_genre.index, 
            autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel')
        )
        axes[1, 0].set_title('Revenue Share by Book Genre', fontsize=12, fontweight='bold')
        
        # --- PLOT 4: Heatmap (Correlation: Price vs. Sales Volume) ---
        # Group by title to get total sales volume and average price per book
        book_stats = merged_df.groupby('Title').agg({
            'Price': 'mean',
            'Quantity_Sold': 'sum'
        })
        # Calculate the mathematical correlation between the two columns
        corr_matrix = book_stats[['Price', 'Quantity_Sold']].corr()
        sns.heatmap(
            corr_matrix, annot=True, cmap='coolwarm', 
            vmin=-1, vmax=1, ax=axes[1, 1], square=True, fmt=".2f"
        )
        axes[1, 1].set_title('Correlation: Price vs. Sales Volume', fontsize=12, fontweight='bold')
        
        # 5. Clean up layout and display
        plt.tight_layout()
        plt.show()


# --- MENU INTERFACE ---
    def main_menu():
        my_bookstore = Bookstore()
        while True:
            print("\n" + "-"*30)
            print("  INVENTORY MANAGEMENT SYSTEM")
            print("-"*30)
            print("1. Add a New Book")
            print("2. Update Inventory (Add Stock)")
            print("3. Record a Sale")
            print("4. Generate Store Report")
            print("5. Visualisation")
            print("6. Save and Exit")
            choice = int(input("\nEnter your choice (1-5): "))
            match choice:
                case 1:
                    print("\n-- Add a New Book --")
                    title = input("Enter Book Title: ")
                    author = input("Enter Author: ")
                    genre = input("Enter Genre: ")
                    try:
                        price = float(input("Enter Price: $"))
                        quantity = int(input("Enter Initial Quantity: "))
                        my_bookstore.add_book(title, author, genre, price, quantity)
                    except ValueError:
                        print("-> Error: Price must be a number and Quantity must be a whole number.")
                case 2:
                    print("\n-- Update Inventory --")
                    title = input("Enter Book Title to update: ")
                    try:
                        quantity = int(input("Enter number of books to add to stock: "))
                        my_bookstore.update_inventory(title, quantity)
                    except ValueError:
                        print("-> Error: Quantity must be a whole number.")
                case 3:
                    print("\n-- Record a Sale --")
                    title = input("Enter Book Title sold: ")
                    try:
                        quantity = int(input("Enter number of copies sold: "))
                        my_bookstore.record_sale(title, quantity)
                    except ValueError:
                        print("-> Error: Quantity must be a whole number.")
                case 4:
                    my_bookstore.generate_report()
                case 5:
                    my_bookstore.visualisation()
                case 6:
                    my_bookstore.save_data()
                    print("Exiting program. Have a great day!")
                    break
                
                case _:
                    print("-> Invalid choice. Please enter a number between 1 and 5.")

    if __name__ == "__main__":
        main_menu()