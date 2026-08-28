def balindromes(star: int, end: int) -> int:
    """
    Function to find all palindromic numbers in a given range.

    Parameters:
    star (int): The starting number of the range.
    end (int): The ending number of the range.

    Returns:
    list: A list of palindromic numbers within the specified range.
    """
    palindromic_numbers = []

    for num in range(star, end + 1):
        if str(num) == str(num)[::-1]:  # Check if the number is a palindrome
            palindromic_numbers.append(num)

    return palindromic_numbers
