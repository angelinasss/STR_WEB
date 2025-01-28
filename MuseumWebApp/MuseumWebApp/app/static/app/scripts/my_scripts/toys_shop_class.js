// Базовый класс
class Toy {
    constructor(name, price, ageRange) {
        this.name = name;
        this.price = price;
        this.ageRange = ageRange;
    }

    getName() {
        return this.name;
    }

    getPrice() {
        return this.price;
    }

    getAgeRange() {
        return this.ageRange;
    }

    setName(name) {
        this.name = name;
    }

    setPrice(price) {
        this.price = price;
    }

    setAgeRange(ageRange) {
        this.ageRange = ageRange;
    }
}

// Наследник
class AdvancedToy extends Toy {
    constructor(name, price, ageRange, category) {
        super(name, price, ageRange);
        this.category = category;
    }

    getCategory() {
        return this.category;
    }

    setCategory(category) {
        this.category = category;
    }
}

// Массив игрушек
let toys = [];

// Метод добавления игрушки через форму
function addToy() {
    const name = document.getElementById("name").value;
    const price = parseFloat(document.getElementById("price").value);
    const ageRange = document.getElementById("ageRange").value;
    const category = document.getElementById("category").value;

    const toy = new AdvancedToy(name, price, ageRange, category);
    toys.push(toy);
    displayToys();
}

// Метод вывода всех игрушек
function displayToys() {
    const toyList = document.getElementById("toyList");
    toyList.innerHTML = "";
    toys.forEach(toy => {
        const li = document.createElement("li");
        li.textContent = `${toy.getName()} - ${toy.getPrice()} RUB, ${toy.getAgeRange()} age, ${toy.getCategory()}`;
        toyList.appendChild(li);
    });
}

// Метод вывода наиболее дорогих игрушек
function displayExpensiveToys() {
    const maxPrice = Math.max(...toys.map(toy => toy.getPrice()));
    const expensiveToys = toys.filter(toy => maxPrice - toy.getPrice() <= 1);

    const result = document.getElementById("result");
    result.innerHTML = "The most expensive toys: ";
    result.innerHTML += expensiveToys.map(toy => toy.getName()).join(", ");
}