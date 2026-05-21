def calculate_payoff_time(principal, annual_interest_rate, monthly_payment, paid_off_amount=0):
    """
    Calculate months to pay off a loan with compound interest.
    
    Parameters:
    - principal: Total loan amount (e.g., $6,700)
    - annual_interest_rate: APR as decimal (e.g., 0.10 for 10%)
    - monthly_payment: Amount you can pay each month
    - paid_off_amount: How much has already been paid off (e.g., $1,000)
    
    Returns:
    - Dictionary with payoff details
    """
    
    monthly_interest_rate = annual_interest_rate / 12
    
    # Adjust remaining balance based on what's already paid off
    remaining_principal = principal - paid_off_amount
    
    # Ensure we don't go negative
    if remaining_principal <= 0:
        return {
            'months': 0,
            'total_paid': paid_off_amount,
            'total_interest': 0,
            'years_months': "0 months",
            'payment_schedule': [],
            'error': None,
            'already_paid_off': paid_off_amount,
            'original_principal': principal,
            'remaining_principal': 0,
            'total_loan_cost': principal,
            'total_interest_paid': 0,
            'interest_as_percentage': 0
        }
    
    # Edge case: If monthly payment is less than interest accrued, loan never gets paid off
    if monthly_payment <= remaining_principal * monthly_interest_rate:
        return {
            'months': float('inf'),
            'total_paid': None,
            'total_interest': None,
            'error': "Monthly payment is too low to cover interest. Loan will never be paid off.",
            'already_paid_off': paid_off_amount,
            'original_principal': principal,
            'remaining_principal': remaining_principal
        }
    
    months = 0
    balance = remaining_principal
    total_interest_paid = 0
    payment_schedule = []
    
    while balance > 0:
        # Calculate interest for this month
        interest_this_month = balance * monthly_interest_rate
        
        # Add interest to balance
        balance += interest_this_month
        total_interest_paid += interest_this_month
        
        # Make payment (but don't go below zero)
        payment = min(monthly_payment, balance)
        balance -= payment
        
        months += 1
        
        # Store monthly data for detailed breakdown
        payment_schedule.append({
            'month': months,
            'payment': payment,
            'interest_paid': interest_this_month,
            'principal_paid': payment - interest_this_month,
            'remaining_balance': balance
        })
        
        # Safety break (prevents infinite loop)
        if months > 1200:  # 100 years
            return {
                'months': float('inf'),
                'total_paid': None,
                'total_interest': None,
                'error': "Loan is taking too long to pay off. Consider higher monthly payments.",
                'already_paid_off': paid_off_amount,
                'original_principal': principal,
                'remaining_principal': remaining_principal
            }
    
    total_paid_from_remaining = remaining_principal + total_interest_paid
    total_paid_overall = paid_off_amount + total_paid_from_remaining
    total_interest_overall = total_interest_paid  # Interest is only on the remaining balance
    
    # Calculate total loan cost (original principal + total interest)
    total_loan_cost = principal + total_interest_overall
    interest_percentage = (total_interest_overall / principal) * 100 if principal > 0 else 0
    
    return {
        'months': months,
        'total_paid': round(total_paid_overall, 2),
        'total_interest': round(total_interest_overall, 2),
        'years_months': f"{months // 12} years, {months % 12} months" if months >= 12 else f"{months} months",
        'payment_schedule': payment_schedule,
        'error': None,
        'already_paid_off': paid_off_amount,
        'original_principal': principal,
        'remaining_principal': round(remaining_principal, 2),
        'remaining_interest': round(total_interest_overall, 2),
        'total_loan_cost': round(total_loan_cost, 2),  # OTD price + total interest
        'total_interest_paid': round(total_interest_overall, 2),
        'interest_as_percentage': round(interest_percentage, 2)
    }


def compare_payment_scenarios(principal, interest_rate, paid_off_amount=0):
    """
    Compare multiple payment amounts to see the difference.
    Asks user for payment scenarios to compare.
    """
    print("\n" + "="*80)
    print(f"LOAN DETAILS: ${principal:,.2f} at {interest_rate:.1%} APR")
    if paid_off_amount > 0:
        remaining = principal - paid_off_amount
        print(f"ALREADY PAID OFF: ${paid_off_amount:,.2f} (Remaining balance: ${remaining:,.2f})")
    print("="*80)
    
    # Ask user what payment amounts they want to compare
    print("\nLet's compare different monthly payment scenarios.")
    print("Enter payment amounts separated by spaces (e.g., 200 300 400 500)")
    payment_input = input("Payment amounts to compare: $")
    
    # Parse the input
    payment_options = [float(x.strip()) for x in payment_input.split()]
    
    if not payment_options:
        print("No valid payment amounts entered. Using default: 200, 300, 400, 500")
        payment_options = [200, 300, 400, 500]
    
    print(f"\n{'Monthly':<12} {'Payoff':<12} {'Total':<14} {'Interest':<14} {'Total Loan':<14} {'Interest %':<10}")
    print(f"{'Payment':<12} {'Time':<12} {'Paid':<14} {'Paid':<14} {'Cost':<14} {'of Principal':<10}")
    print("-"*80)
    
    results = []
    for payment in payment_options:
        result = calculate_payoff_time(principal, interest_rate, payment, paid_off_amount)
        if result['error']:
            print(f"${payment:<11.2f} {'NEVER':<12} {result['error'][:40]}")
        else:
            print(f"${payment:<11.2f} {result['years_months']:<12} ${result['total_paid']:<13,.2f} ${result['total_interest']:<13,.2f} ${result['total_loan_cost']:<13,.2f} {result['interest_as_percentage']:<9.1f}%")
        results.append(result)
    
    return results


def show_extra_payment_analysis(principal, interest_rate, monthly_payment, paid_off_amount=0):
    """
    Show how extra payments help pay off the loan faster.
    """
    print("\n" + "="*70)
    print("HOW EXTRA PAYMENTS HELP")
    print("="*70)
    
    base_result = calculate_payoff_time(principal, interest_rate, monthly_payment, paid_off_amount)
    
    if base_result['error']:
        print(f"\n❌ With ${monthly_payment}/month: {base_result['error']}")
        return
    
    print(f"\n📊 BASELINE SCENARIO (${monthly_payment}/month):")
    print(f"   Payoff time: {base_result['years_months']}")
    print(f"   Total interest: ${base_result['total_interest']:,.2f}")
    print(f"   Total loan cost: ${base_result['total_loan_cost']:,.2f} (Principal + Interest)")
    print(f"   Interest is {base_result['interest_as_percentage']:.1f}% of principal")
    
    # Ask user what extra amounts they want to see
    print("\nEnter extra monthly payment amounts to see savings (separated by spaces)")
    print("Example: 50 100 150 200")
    extra_input = input("Extra amounts to analyze: $")
    
    if extra_input.strip():
        extra_payments = [float(x.strip()) for x in extra_input.split()]
    else:
        extra_payments = [50, 100, 150, 200]
        print(f"Using defaults: {extra_payments}")
    
    print("\n" + "-"*80)
    print(f"{'Extra':<10} {'New Payment':<15} {'Time Saved':<15} {'Interest Saved':<18} {'New Loan Cost':<15}")
    print("-"*80)
    
    for extra in extra_payments:
        new_payment = monthly_payment + extra
        new_result = calculate_payoff_time(principal, interest_rate, new_payment, paid_off_amount)
        if not new_result['error']:
            months_saved = base_result['months'] - new_result['months']
            interest_saved = base_result['total_interest'] - new_result['total_interest']
            years_saved = f"{months_saved // 12}y {months_saved % 12}m" if months_saved >= 12 else f"{months_saved}m"
            print(f"+${extra:<9.2f} ${new_payment:<14.2f} {years_saved:<15} ${interest_saved:<17,.2f} ${new_result['total_loan_cost']:<14,.2f}")
    
    print("\n💡 Tip: Even small extra payments make a big difference over time!")


def show_total_loan_cost_breakdown(principal, interest_rate, monthly_payment, paid_off_amount=0):
    """
    Show detailed breakdown of total loan cost including OTD price and interest.
    """
    result = calculate_payoff_time(principal, interest_rate, monthly_payment, paid_off_amount)
    
    if result['error']:
        print(f"\n❌ {result['error']}")
        return
    
    print("\n" + "="*70)
    print("💰 TOTAL LOAN COST BREAKDOWN")
    print("="*70)
    
    remaining_principal = principal - paid_off_amount
    
    print(f"\n📋 ORIGINAL LOAN TERMS:")
    print(f"   Out-the-door (OTD) price:     ${principal:,.2f}")
    print(f"   Interest rate:                 {interest_rate:.1%} APR")
    print(f"   Monthly payment:               ${monthly_payment:,.2f}")
    
    print(f"\n📊 CURRENT STATUS:")
    print(f"   Already paid off:              ${paid_off_amount:,.2f}")
    print(f"   Remaining principal:           ${remaining_principal:,.2f}")
    
    print(f"\n💰 TOTAL COST BREAKDOWN:")
    print(f"   Original OTD price:            ${principal:,.2f}")
    print(f"   Total interest to be paid:     ${result['total_interest']:,.2f}")
    print(f"   ─────────────────────────────────────")
    print(f"   TOTAL LOAN COST:               ${result['total_loan_cost']:,.2f}")
    print(f"   (What you'll pay in total)")
    
    print(f"\n📈 INTEREST ANALYSIS:")
    print(f"   Interest as % of principal:    {result['interest_as_percentage']:.1f}%")
    print(f"   Average interest per month:    ${result['total_interest'] / result['months']:,.2f}" if result['months'] > 0 else "   N/A")
    
    # Show comparison to principal
    interest_pct_of_otd = (result['total_interest'] / principal) * 100
    print(f"   You're paying {interest_pct_of_otd:.1f}% extra on top of OTD price")
    
    # Calculate cost per $100 borrowed
    cost_per_100 = (result['total_loan_cost'] / principal) * 100
    print(f"   Cost per $100 borrowed:        ${cost_per_100:.2f}")
    
    print("\n" + "="*70)


def interactive_payment_calculator():
    """
    Run a fully interactive version where user inputs all their numbers.
    No hard-coded variables!
    """
    print("\n" + "="*60)
    print("LOAN PAYOFF CALCULATOR")
    print("="*60)
    print("\nWelcome! Let's calculate when you'll pay off your loan.")
    print("-"*40)
    
    # Get all inputs from user
    try:
        print("\n📋 STEP 1: Basic Loan Information")
        principal = float(input("   Out-the-door (OTD) price / Total loan amount: $"))
        
        paid_off = float(input("   How much have you already paid off? $"))
        
        if paid_off > principal:
            print("\n⚠️ Warning: You've paid off more than the original loan amount!")
            print("   This could mean overpayment or an incorrect entry.")
            confirm = input("   Continue anyway? (y/n): ").lower()
            if confirm != 'y':
                print("   Please restart and enter correct amounts.")
                return
        
        interest_rate_percent = float(input("   Annual interest rate (e.g., 8.5 for 8.5%): "))
        interest_rate = interest_rate_percent / 100
        
        print("\n💰 STEP 2: Payment Information")
        monthly_payment = float(input("   Your planned monthly payment: $"))
        
        print("\n📊 STEP 3: Analysis Options")
        show_cost_breakdown = input("   Show total loan cost breakdown (OTD + interest)? (y/n): ").lower() == 'y'
        do_comparison = input("   Compare different payment scenarios? (y/n): ").lower() == 'y'
        do_extra_analysis = input("   Show how extra payments help? (y/n): ").lower() == 'y'
        
        # Calculate and display main result
        print("\n" + "-"*40)
        print("📈 YOUR PAYOFF SUMMARY")
        print("-"*40)
        
        result = calculate_payoff_time(principal, interest_rate, monthly_payment, paid_off)
        
        if result['error']:
            print(f"\n❌ {result['error']}")
            print("\n💡 Suggestions:")
            print("   • Increase your monthly payment")
            print("   • Make bi-weekly payments instead of monthly")
            print("   • Negotiate a lower interest rate")
            print("   • Make a lump sum payment if possible")
        else:
            remaining = principal - paid_off
            
            print(f"\n✅ LOAN PAYOFF ANALYSIS")
            print(f"   Original OTD price:          ${result['original_principal']:,.2f}")
            print(f"   Already paid off:            ${result['already_paid_off']:,.2f}")
            print(f"   Remaining balance:           ${result['remaining_principal']:,.2f}")
            print(f"   ─────────────────────────────")
            print(f"   Time to pay off (from now):  {result['years_months']}")
            print(f"   Total remaining interest:    ${result['total_interest']:,.2f}")
            print(f"   Total paid (overall):        ${result['total_paid']:,.2f}")
            print(f"   TOTAL LOAN COST (OTD + int): ${result['total_loan_cost']:,.2f}")
            
            # Show total loan cost breakdown if requested
            if show_cost_breakdown:
                show_total_loan_cost_breakdown(principal, interest_rate, monthly_payment, paid_off)
            
            # Show a few months of payment schedule
            print("\n📅 FIRST 3 MONTHS BREAKDOWN (starting now):")
            print(f"{'Month':<8} {'Payment':<12} {'Interest':<12} {'Principal':<12} {'Balance Left':<12}")
            print("-"*56)
            if result['payment_schedule']:
                for month_data in result['payment_schedule'][:3]:
                    print(f"{month_data['month']:<8} ${month_data['payment']:<11.2f} ${month_data['interest_paid']:<11.2f} ${month_data['principal_paid']:<11.2f} ${month_data['remaining_balance']:<11.2f}")
            
            # Show estimated payoff date
            from datetime import datetime, timedelta
            today = datetime.now()
            payoff_date = today + timedelta(days=result['months'] * 30.44)  # Average days per month
            print(f"\n📅 Estimated payoff date: {payoff_date.strftime('%B %Y')}")
            
            # Show total interest as percentage
            print(f"\n💡 DID YOU KNOW?")
            print(f"   You're paying {result['interest_as_percentage']:.1f}% of the OTD price in interest.")
            print(f"   That's like adding ${result['total_loan_cost'] - principal:,.2f} to your purchase price!")
        
        # Run comparison if requested
        if do_comparison and not result['error']:
            compare_payment_scenarios(principal, interest_rate, paid_off)
        
        # Run extra payment analysis if requested
        if do_extra_analysis and not result['error']:
            show_extra_payment_analysis(principal, interest_rate, monthly_payment, paid_off)
        
        # Optional: Show savings tips
        print("\n" + "="*60)
        print("💡 MONEY-SAVING TIPS")
        print("="*60)
        print("• Round up your payment to the nearest $50 or $100")
        print("• Make one extra payment per year")
        print("• Switch to bi-weekly payments (26 half-payments = 13 full payments/year)")
        print("• Put tax refunds or bonuses toward the principal")
        print("="*60)
        
    except ValueError as e:
        print(f"\n❌ Invalid input: {e}")
        print("Please enter numeric values only.")
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Happy debt-free journey!")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
        print("Please try again.")


def quick_calculation_mode():
    """
    A quick mode that asks for just the essentials.
    """
    print("\n" + "="*60)
    print("QUICK CALCULATION MODE")
    print("="*60)
    
    try:
        print("\nEnter your loan details:")
        principal = float(input("   OTD price / Loan amount: $"))
        paid_off = float(input("   Already paid: $"))
        interest_rate = float(input("   Interest rate (%): ")) / 100
        monthly_payment = float(input("   Monthly payment: $"))
        
        result = calculate_payoff_time(principal, interest_rate, monthly_payment, paid_off)
        
        if result['error']:
            print(f"\n❌ {result['error']}")
        else:
            remaining = principal - paid_off
            print(f"\n✅ QUICK SUMMARY:")
            print(f"   Remaining balance:        ${remaining:,.2f}")
            print(f"   Payoff time:              {result['years_months']}")
            print(f"   Total interest to pay:    ${result['total_interest']:,.2f}")
            print(f"   TOTAL LOAN COST (OTD+int): ${result['total_loan_cost']:,.2f}")
            
            # Show brief interest analysis
            interest_percentage = (result['total_interest'] / principal) * 100
            print(f"   Interest is {interest_percentage:.1f}% of OTD price")
            
    except ValueError:
        print("\n❌ Invalid input. Please use numbers only.")


def main():
    """
    Main program with menu system - no hard-coded variables!
    """
    while True:
        print("\n" + "="*60)
        print("LOAN PAYOFF CALCULATOR")
        print("="*60)
        print("\nWhat would you like to do?")
        print("1. Full analysis (all options)")
        print("2. Quick calculation")
        print("3. Compare payment scenarios")
        print("4. Extra payment analyzer")
        print("5. View total loan cost breakdown")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':
            interactive_payment_calculator()
        elif choice == '2':
            quick_calculation_mode()
        elif choice == '3':
            try:
                print("\n" + "-"*40)
                principal = float(input("Original OTD price / Loan amount: $"))
                paid_off = float(input("Already paid off: $"))
                interest_rate = float(input("Interest rate (%): ")) / 100
                compare_payment_scenarios(principal, interest_rate, paid_off)
            except ValueError:
                print("❌ Invalid input. Please use numbers.")
        elif choice == '4':
            try:
                print("\n" + "-"*40)
                principal = float(input("Original OTD price / Loan amount: $"))
                paid_off = float(input("Already paid off: $"))
                interest_rate = float(input("Interest rate (%): ")) / 100
                monthly_payment = float(input("Current monthly payment: $"))
                show_extra_payment_analysis(principal, interest_rate, monthly_payment, paid_off)
            except ValueError:
                print("❌ Invalid input. Please use numbers.")
        elif choice == '5':
            try:
                print("\n" + "-"*40)
                principal = float(input("Original OTD price / Loan amount: $"))
                paid_off = float(input("Already paid off: $"))
                interest_rate = float(input("Interest rate (%): ")) / 100
                monthly_payment = float(input("Current monthly payment: $"))
                show_total_loan_cost_breakdown(principal, interest_rate, monthly_payment, paid_off)
            except ValueError:
                print("❌ Invalid input. Please use numbers.")
        elif choice == '6':
            print("\n👋 Thank you for using the Loan Payoff Calculator!")
            print("Remember: Every extra payment brings you closer to financial freedom!")
            break
        else:
            print("\n❌ Invalid choice. Please enter 1-6.")
        
        input("\nPress Enter to continue...")


# Run the main program - no hard-coded variables!
if __name__ == "__main__":
    main()