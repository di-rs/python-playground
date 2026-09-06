from pydantic import BaseModel, ValidationError


class Computer(BaseModel):
    brand: str
    ram_gb: int
    hard_drive_gb: int


if __name__ == "__main__":
    laptop = Computer(brand="apple", ram_gb=16, hard_drive_gb=512)
    print(laptop)

    try:
        bad = Computer(brand="apple", ram_gb="thirty two", hard_drive_gb=512)
    except ValidationError as e:
        print(e)
