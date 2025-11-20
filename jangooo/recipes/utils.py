import re
from fractions import Fraction

def parse_ingredient_amount(ingredient_line):
    """Parse ingredient amount from text line"""
    # Match patterns like "1 cup", "1/2 tsp", "2.5 lbs"
    pattern = r'^(\d+(?:\.\d+)?|\d+/\d+|\d+\s+\d+/\d+)'
    match = re.match(pattern, ingredient_line.strip())
    if match:
        amount_str = match.group(1)
        try:
            if '/' in amount_str:
                return float(Fraction(amount_str))
            return float(amount_str)
        except:
            return 1.0
    return 1.0

def scale_ingredient_line(ingredient_line, scale_factor):
    """Scale a single ingredient line by the given factor"""
    amount = parse_ingredient_amount(ingredient_line)
    scaled_amount = amount * scale_factor
    
    # Replace the amount in the original line
    pattern = r'^(\d+(?:\.\d+)?|\d+/\d+|\d+\s+\d+/\d+)'
    if re.match(pattern, ingredient_line.strip()):
        # Format the scaled amount nicely
        if scaled_amount == int(scaled_amount):
            scaled_str = str(int(scaled_amount))
        else:
            scaled_str = f"{scaled_amount:.1f}"
        
        return re.sub(pattern, scaled_str, ingredient_line, count=1)
    
    return ingredient_line