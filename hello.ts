interface User{
    name: string;
    id: number;
}

class UserAccount{
    name: string;
    id: number;

    constructor(name: string, id: number) {
        this.name = name;
        this.id = id;
    }
}


const user: User = {
    name: "Guido",
    id: 1
};

const userAccount: UserAccount = new UserAccount("Bob", id=2);

console.log(`user.name is ${user.name}`);
console.log(`userAccount.name is ${userAccount.name}`);