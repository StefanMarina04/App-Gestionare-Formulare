let player = {
    health: 100,
    fun: 0,
    eatApple: function() {
        console.log("Player ate an apple");
        this.health += 10;
        console.log(this.health);
    },
    eatCandy: function() {
        console.log("Player ate some candy");
        this.health -= 5;
        console.log(this.health);
        this.fun += 10;
        console.log(this.fun);
    },
    play: function() {
        console.log("Player is playing");
        this.fun += 20;
        console.log(this.fun);
    },
    print: function()
    {
        console.log(this);
    }
};

player.eatApple(); console.log(player);
player.eatCandy(); console.log(player);
player.play(); console.log(player);
player.print();