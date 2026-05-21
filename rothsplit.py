#!/usr/bin/env python3
"""
Roth IRA Contribution Splitter
80% VTI / 20% VXUS
"""

import os
import sys

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    while True:
        clear_screen()
        
        print("=" * 46)
        print("   Roth IRA Contribution Splitter")
        print("   80% VTI  /  20% VXUS")
        print("=" * 46)
        print()
        
        # Get user input
        try:
            contribution_input = input("Enter your monthly contribution amount: $")
            
            # Remove any commas or spaces
            contribution_input = contribution_input.replace(',', '').replace(' ', '')
            
            # Convert to integer
            contribution = int(contribution_input)
            
            if contribution <= 0:
                print("\n[ERROR] Please enter a positive number")
                input("\nPress Enter to try again...")
                continue
                
        except ValueError:
            print("\n[ERROR] Please enter a valid number (e.g., 200, 450, 700)")
            input("\nPress Enter to try again...")
            continue
        
        # Calculate VTI (80%) and VXUS (20%)
        vti = int(contribution * 80 / 100)
        vxus = contribution - vti  # This ensures vti + vxus = contribution
        
        # Display results
        print()
        print("=" * 46)
        print(f" Monthly Contribution: ${contribution:,}")
        print("=" * 46)
        print()
        print(f" BUY ${vti:,} of VTI  (Vanguard Total Stock Market)")
        print(f" BUY ${vxus:,} of VXUS (Vanguard Total International)")
        print()
        print("=" * 46)
        print()
        print(" Reminder: 80/20 split is for aggressive growth")
        print(" at age 25. Revisit allocation every 5-10 years.")
        print("=" * 46)
        print()
        
        # Ask if user wants to continue
        continue_choice = input("Calculate another contribution? (y/n): ").lower()
        if continue_choice not in ['y', 'yes']:
            print("\nGoodbye! Happy investing!")
            break
        
        print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        sys.exit(0)