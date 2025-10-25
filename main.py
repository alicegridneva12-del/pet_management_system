import json
from typing import List, Dict


#Пользовательские исключения
class PetNotFoundError(Exception):
    """Вызывается, если питомец не найден."""
    pass

class InvalidAgeError(Exception):
    """Вызывается, если возраст некорректен."""
    pass

class DuplicatePetError(Exception):
    """Вызывается, если питомец с таким именем уже существует."""
    pass


class Pet:
    def __init__(self, name: str, species: str, age: int, owner: str):
        name = name.strip()
        species = species.strip()
        owner = owner.strip()
        
        if not name or not species or not owner:
            raise ValueError("Имя, вид и владелец не могут быть пустыми.")
        if age < 0:
            raise InvalidAgeError("Возраст не может быть отрицательным.")
        
        self.name = name
        self.species = species
        self.age = age
        self.owner = owner

    def __str__(self):
        return f"{self.name} ({self.species}), {self.age} лет, владелец: {self.owner}"

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "species": self.species,
            "age": self.age,
            "owner": self.owner
        }

    @classmethod
    def from_dict(cls, data: Dict): #Создаёт объект Pet из словаря (десериализация)
        return cls(
            name=data["name"],
            species=data["species"],
            age=data["age"],
            owner=data["owner"]
        )

class PetManager:
    def __init__(self):
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet):
        if any(p.name.strip() == pet.name.strip() for p in self.pets):
            raise DuplicatePetError(f"Питомец с именем '{pet.name}' уже существует.")
        self.pets.append(pet)

    def remove_pet(self, name: str):
        for i, pet in enumerate(self.pets):
            if pet.name == name:
                del self.pets[i]
                return
        raise PetNotFoundError(f"Питомец с именем '{name}' не найден.")

    def find_pet(self, name: str) -> Pet:
        for pet in self.pets:
            if pet.name == name:
                return pet
        raise PetNotFoundError(f"Питомец с именем '{name}' не найден.")

    def list_pets(self) -> List[Pet]:
        return self.pets

    def save_to_json(self, filename: str):
        pets_data = [pet.to_dict() for pet in self.pets]
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(pets_data, f, ensure_ascii=False, indent=4)

    def load_from_json(self, filename: str):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                pets_data = json.load(f)
                self.pets = [Pet.from_dict(data) for data in pets_data]
        except FileNotFoundError:
            self.pets = []
        except json.JSONDecodeError as e:
            print(f"Ошибка чтения JSON: {e}")
            self.pets = []

def main():
    manager = PetManager()
    json_file = "pets.json"

    manager.load_from_json(json_file)

    while True:
        print("\n" + "=" * 40)
        print("СИСТЕМА УПРАВЛЕНИЯ ПИТОМЦАМИ")
        print("=" * 40)
        print("1. Добавить питомца")
        print("2. Удалить питомца")
        print("3. Найти питомца")
        print("4. Показать всех питомцев")
        print("5. Сохранить в JSON")
        print("6. Выход")
        print("=" * 40)
        choice = input("Выберите действие: ").strip()

        try:
            if choice == "1":
                name = input("Имя: ").strip()
                species = input("Вид (например, кот, собака): ").strip()
                owner = input("Владелец: ").strip()

                age = None
                while age is None:
                    age_input = input("Возраст (целое число ≥ 0): ").strip()
                    try:
                        age = int(age_input)
                        if age < 0:
                            print("Возраст не может быть отрицательным.")
                            age = None
                    except ValueError:
                        print("Пожалуйста, введите целое число.")

                pet = Pet(name, species, age, owner)
                manager.add_pet(pet)
                print("Питомец успешно добавлен!")

            elif choice == "2":
                name = input("Имя питомца для удаления: ").strip()
                manager.remove_pet(name)
                print("Питомец удалён!")

            elif choice == "3":
                name = input("Имя питомца для поиска: ").strip()
                pet = manager.find_pet(name)
                print("Найден:", pet)

            elif choice == "4":
                pets = manager.list_pets()
                if pets:
                    print("\n Список питомцев:")
                    for i, pet in enumerate(pets, 1):
                        print(f"{i}. {pet}")
                else:
                    print("Нет зарегистрированных питомцев.")

            elif choice == "5":
                manager.save_to_json(json_file)
                print(f"Данные сохранены в {json_file}")

            elif choice == "6":
                manager.save_to_json(json_file)
                print("До свидания! Данные сохранены.")
                break

            else:
                print("Неверный выбор. Введите число от 1 до 6.")

        except (ValueError, InvalidAgeError, DuplicatePetError, PetNotFoundError) as e:
            print(f"Ошибка: {e}")
        except KeyboardInterrupt:
            print("\n\nПрограмма прервана пользователем.")
            break
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")


if __name__ == "__main__":
    main()
