// Базовый класс
function Toy(name, price, ageRange) {
    this.name = name;
    this.price = price;
    this.ageRange = ageRange;
}

Toy.prototype.getName = function () {
    return this.name;
};

Toy.prototype.getPrice = function () {
    return this.price;
};

Toy.prototype.getAgeRange = function () {
    return this.ageRange;
};

Toy.prototype.setName = function (name) {
    this.name = name;
};

Toy.prototype.setPrice = function (price) {
    this.price = price;
};

Toy.prototype.setAgeRange = function (ageRange) {
    this.ageRange = ageRange;
};

// Наследник
function AdvancedToy(name, price, ageRange, category) {
    Toy.call(this, name, price, ageRange);
    this.category = category;
}

AdvancedToy.prototype = Object.create(Toy.prototype);
AdvancedToy.prototype.constructor = AdvancedToy;

AdvancedToy.prototype.getCategory = function () {
    return this.category;
};

AdvancedToy.prototype.setCategory = function (category) {
    this.category = category;
};

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