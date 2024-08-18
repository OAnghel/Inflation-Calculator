# src/main.py
from src.calculator import DollarConverter

def main():
    converter = DollarConverter()
    
    try:
        amount = float(input("Enter the amount in dollars: "))
        from_year = int(input("Enter the starting year: "))
        to_year = int(input("Enter the year to convert to: "))
        
        converted_amount = converter.convert(amount, from_year, to_year)
        
        print(f"${amount} in {from_year} is equivalent to ${converted_amount:.2f} in {to_year}.")
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
