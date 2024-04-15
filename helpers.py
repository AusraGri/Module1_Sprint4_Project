"""Quite useless helpers now. But I wanted to colorize all MENU options and
    Error / Program messages / User input for the nicer look and more convient interactions, but...
    Lacking of time....
    """
class Sep:
    def __init__(self) -> None:
        pass
        
    def line(self, number) -> None:
        print(f"{"-" * number}")
        
    def dots (self, number) -> None:
        print(f"{"." * number}")
    
    def bold (self, number) -> None:
        print(f"{"=" * number}")
    
    def wall (self, number) -> None:
        print(f"{"|" * number}")

        
def colorizer(text) -> None:
    pass
