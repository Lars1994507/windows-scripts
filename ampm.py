from datetime import datetime, timedelta

def parse_time(time_str):
    """Parse a time string like '8am' or '1pm' into a datetime object."""
    time_str = time_str.lower().strip()
    
    # Check if it ends with am or pm
    if time_str.endswith('am'):
        hour = int(time_str[:-2])
        minute = 0
        # 12am is 0:00
        if hour == 12:
            hour = 0
        suffix = 'AM'
    elif time_str.endswith('pm'):
        hour = int(time_str[:-2])
        minute = 0
        # 12pm is 12:00
        if hour != 12:
            hour += 12
        suffix = 'PM'
    else:
        # Try to parse with colon format like "8:30am"
        if 'am' in time_str:
            time_part = time_str.split('am')[0]
            suffix = 'AM'
        elif 'pm' in time_str:
            time_part = time_str.split('pm')[0]
            suffix = 'PM'
        else:
            raise ValueError("Please include 'am' or 'pm' in the time")
        
        if ':' in time_part:
            hour, minute = map(int, time_part.split(':'))
        else:
            hour = int(time_part)
            minute = 0
        
        # Convert 12-hour to 24-hour format
        if suffix == 'AM':
            if hour == 12:
                hour = 0
        else:  # PM
            if hour != 12:
                hour += 12
    
    return hour, minute

def calculate_time_difference():
    """Main function to calculate time difference between AM and PM times."""
    print("=" * 50)
    print("TIME DIFFERENCE CALCULATOR")
    print("=" * 50)
    print("This calculator finds the hours and minutes between an AM time and a PM time.")
    print("\nExamples of valid formats:")
    print("  • 8am, 1pm")
    print("  • 8:30am, 1:45pm")
    print("  • 12am, 12pm")
    print("=" * 50)
    
    while True:
        try:
            # Get AM time
            while True:
                am_time = input("\nEnter the AM time (e.g., 8am or 8:30am): ").strip()
                try:
                    am_hour, am_minute = parse_time(am_time)
                    
                    # Validate it's an AM time
                    if am_time.lower().endswith('am') or 'am' in am_time.lower():
                        break
                    else:
                        print("Please enter a valid AM time (should end with 'am')")
                except ValueError as e:
                    print(f"Error: {e}")
            
            # Get PM time
            while True:
                pm_time = input("Enter the PM time (e.g., 1pm or 1:45pm): ").strip()
                try:
                    pm_hour, pm_minute = parse_time(pm_time)
                    
                    # Validate it's a PM time
                    if pm_time.lower().endswith('pm') or 'pm' in pm_time.lower():
                        break
                    else:
                        print("Please enter a valid PM time (should end with 'pm')")
                except ValueError as e:
                    print(f"Error: {e}")
            
            # Use a reference date (today)
            base_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            
            # Create datetime objects for both times on the same day
            time1 = base_date.replace(hour=am_hour, minute=am_minute)
            time2 = base_date.replace(hour=pm_hour, minute=pm_minute)
            
            # If time2 is earlier than time1, add one day (for overnight scenarios)
            # But since it's AM to PM, this shouldn't happen as PM > AM on same day
            # We'll keep the logic for safety
            if time2 < time1:
                time2 += timedelta(days=1)
            
            # Calculate difference
            difference = time2 - time1
            total_minutes = difference.total_seconds() / 60
            
            # Extract hours and minutes
            hours = int(total_minutes // 60)
            minutes = int(total_minutes % 60)
            
            # Display results
            print("\n" + "=" * 50)
            print("RESULTS:")
            print("=" * 50)
            print(f"From: {format_time(am_hour, am_minute)} AM")
            print(f"To:   {format_time(pm_hour, pm_minute)} PM")
            print("-" * 50)
            
            if hours == 0 and minutes == 0:
                print("⚠️  The times are the same!")
            elif hours == 0:
                print(f"Time difference: {minutes} minute(s)")
            elif minutes == 0:
                print(f"Time difference: {hours} hour(s)")
            else:
                print(f"Time difference: {hours} hour(s) and {minutes} minute(s)")
            
            print(f"Total minutes: {int(total_minutes)} minutes")
            print("=" * 50)
            
            # Ask if user wants to calculate another time
            another = input("\nWould you like to calculate another time? (yes/no): ").strip().lower()
            if another not in ['yes', 'y']:
                print("\nThank you for using the Time Difference Calculator!")
                break
                
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")
            print("Please try again.\n")

def format_time(hour, minute):
    """Format 24-hour time to 12-hour readable format."""
    if hour == 0:
        display_hour = 12
        period = "am"
    elif hour < 12:
        display_hour = hour
        period = "am"
    elif hour == 12:
        display_hour = 12
        period = "pm"
    else:
        display_hour = hour - 12
        period = "pm"
    
    if minute == 0:
        return f"{display_hour}{period}"
    else:
        return f"{display_hour}:{minute:02d}{period}"

if __name__ == "__main__":
    calculate_time_difference()