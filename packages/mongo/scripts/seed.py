from mongo.database import get_mongo_client

NAMES = [
    "Luna",
    "Fido",
    "Fluffy",
    "Carina",
    "Spot",
    "Beethoven",
    "Baxter",
    "Dug",
    "Zero",
    "Santa's Little Helper",
    "Snoopy",
]

PET_TYPES = ["dog", "cat", "bird", "reptile"]

BREEDS = [
    "Havanese",
    "Bichon Frise",
    "Beagle",
    "Cockatoo",
    "African Gray",
    "Tabby",
    "Iguana",
]


def seed() -> None:
    with get_mongo_client() as client:
        db = client.get_database("adoption")

        db["pets"].insert_many(
            [
                {
                    "name": NAMES[index % len(NAMES)],
                    "type": PET_TYPES[index % len(PET_TYPES)],
                    "age": (index % 18) + 1,
                    "breed": BREEDS[index % len(BREEDS)],
                    "index": index,
                }
                for index in range(10_000)
            ]
        )

        print("Loaded sample data.")


if __name__ == "__main__":
    seed()
