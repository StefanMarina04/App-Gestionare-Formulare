let fuel = 1000;
let distance = 0;

while(fuel > 0)
{
    console.log("Ship is moving");
    distance++;
    

    if(distance >= 100 && distance <= 150)
    {
        console.log("Engine off, ship can drift without using fuel");
        continue;
    }

    if(distance == 250)
    {
        console.log("Destination reached");
        break;
    }
    
    fuel--;
}

console.log(distance, fuel);