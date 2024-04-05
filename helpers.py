class Sep:
    def __init__(self) -> None:
        pass
        
    def line(self, number) -> None:
        print(f"{"-" * number}")
        
    def dots (self, number) -> None:
        print(f"{"." * number}")
    
    def bold (self, number):
        print(f"{"=" * number}")
    
    def wall (self, number):
        print(f"{"|" * number}")

        
        
        
        
# p = Sep()
# p.line(20)
# p.dots(20)
# p.bold(20)
# p.wall(20)
