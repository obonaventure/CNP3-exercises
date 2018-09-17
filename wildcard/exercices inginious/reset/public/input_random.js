// Retrieve random inputs
// The second argument is the base of the number the 'radix'
var a = parseInt(input["@random"][0]* 2000 + 1000);// * 5000 + 10000); 
var b = parseInt(input["@random"][1]* 10000 + 1000);
var c = parseInt(input["@random"][2]* 10000);

// Retrieve HTML tag we placed in the statement
// and replace them by the generated random value
document.getElementById("ipr1").innerHTML = a.toString();//16);
document.getElementById("ipr2").innerHTML = b.toString();
document.getElementById("ipr3").innerHTML = c.toString();
