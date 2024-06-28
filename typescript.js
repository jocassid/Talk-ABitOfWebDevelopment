var name1 = 'bob'; // type inferred
var name2 = 'alice'; // explicitly typed
var Person = /** @class */ (function () {
    function Person(firstName, lastName) {
        this.firstName = firstName;
        this.lastName = lastName;
    }
    Person.prototype.greet = function () {
        return "Hello ".concat(this.firstName, " ").concat(this.lastName);
    };
    return Person;
}());
