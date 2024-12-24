import tkinter as tk
from tkinter import simpledialog, messagebox

# Список для хранения товаров и продаж
products = []
sales = []


def load_sales():
    # Здесь можно загрузить данные о продажах из файла или БД
    pass


def add_product():
    product_name = simpledialog.askstring("Добавить товар", "Введите название товара:")
    product_price = simpledialog.askfloat("Добавить товар", "Введите цену товара:")
    product_quantity = simpledialog.askinteger("Добавить товар", "Введите количество на складе:")

    if product_name and product_price is not None and product_quantity is not None:
        products.append({
            'name': product_name,
            'price': product_price,
            'quantity': product_quantity
        })
        messagebox.showinfo("Успех", "Товар успешно добавлен в каталог!")
    else:
        messagebox.showwarning("Ошибка", "Все поля должны быть заполнены!")


def view_catalog():
    catalog_window = tk.Toplevel(root)
    catalog_window.title("Каталог товаров")
    catalog_window.geometry("400x300")

    catalog_text = tk.Text(catalog_window, wrap=tk.WORD)
    catalog_text.pack(fill=tk.BOTH, expand=True)

    if not products:
        catalog_text.insert(tk.END, "Каталог пуст.")
    else:
        for product in products:
            catalog_text.insert(tk.END,
                                f"{product['name']} - {product['price']} руб. (На складе: {product['quantity']})\n")


def create_order():
    order_window = tk.Toplevel(root)
    order_window.title("Создать заказ")
    order_window.geometry("400x300")

    order_text = tk.Text(order_window, wrap=tk.WORD)
    order_text.pack(fill=tk.BOTH, expand=True)

    order_items = []
    total_price = 0

    while True:
        product_name = simpledialog.askstring("Создать заказ", "Введите название товара (или 'стоп' для завершения):")
        if product_name == 'стоп':
            break

        # Поиск товара в каталоге
        product = next((p for p in products if p['name'] == product_name), None)

        if product:
            quantity = simpledialog.askinteger("Создать заказ", "Введите количество:")
            if quantity and quantity <= product['quantity']:
                order_items.append({'product': product, 'quantity': quantity})
                total_price += product['price'] * quantity
                product['quantity'] -= quantity  # Уменьшение количества на складе
                order_text.insert(tk.END, f"{product['name']} x {quantity} = {product['price'] * quantity} руб.\n")
            else:
                messagebox.showwarning("Ошибка", "Недостаточное количество на складе или неправильное количество.")
        else:
            messagebox.showwarning("Ошибка", "Товар не найден.")

    sales.append({'order': order_items, 'total_price': total_price})
    order_text.insert(tk.END, f"\nИтоговая сумма: {total_price} руб.\n")
    messagebox.showinfo("Успех", "Заказ успешно создан!")


def view_sales():
    sales_window = tk.Toplevel(root)
    sales_window.title("Список продаж")
    sales_window.geometry("400x300")

    sales_text = tk.Text(sales_window, wrap=tk.WORD)
    sales_text.pack(fill=tk.BOTH, expand=True)

    if not sales:
        sales_text.insert(tk.END, "Продаж пока нет.")
    else:
        for i, sale in enumerate(sales, start=1):
            sales_text.insert(tk.END, f"\nПродажа #{i}:\n")
            for item in sale["order"]:
                product, quantity = item["product"], item["quantity"]
                sales_text.insert(tk.END, f"{product['name']} x {quantity} = {product['price'] * quantity} руб.\n")
            sales_text.insert(tk.END, f"Итоговая сумма: {sale['total_price']} руб.\n")


# Главное окно программы
root = tk.Tk()
root.title("Магазин: Система управления продажами")
root.geometry("400x300")

load_sales()

tk.Label(root, text="Добро пожаловать в систему управления продажами!", font=("Arial", 14), wraplength=300).pack(
    pady=10)

tk.Button(root, text="Добавить товар в каталог", command=add_product).pack(fill=tk.X, pady=5)
tk.Button(root, text="Просмотреть каталог товаров", command=view_catalog).pack(fill=tk.X, pady=5)
tk.Button(root, text="Создать заказ", command=create_order).pack(fill=tk.X, pady=5)
tk.Button(root, text="Просмотреть все продажи", command=view_sales).pack(fill=tk.X, pady=5)
tk.Button(root, text="Выйти", command=root.quit).pack(fill=tk.X, pady=5)

root.mainloop()
