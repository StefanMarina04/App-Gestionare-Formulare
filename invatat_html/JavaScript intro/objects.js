let player = {
    age: 20,
    name: "Stefan",
    isOnline: true,
    outfit : {
        color: "Blue",
        size: "L",
        value: 100,
        isClean: true 
    }
    };

console.log(player);
console.log(player.isOnline);
console.log(player["name"]);

player.isOnline = false;
console.log(player.isOnline);

player.health = 100;
console.log(player.health);

delete player.health;

console.log(player);
console.log(player.outfit.color);