function sendSignal()
{
    console.log("SOS!");
}

let i = 5;

sendSignal();

while( i > 0 )
{
    sendSignal();
    i -= 1;
}

sendSignal();